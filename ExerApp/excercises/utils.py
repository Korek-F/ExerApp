from .models import Content, Text,BlankText,ABCD,Hint
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.core.paginator import  EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site


def create_content(current_ex,i, request):
    content_type = i.split("-")[1]
    item = request.POST[i].strip()
    if content_type=="Text":
        content_item = Text.objects.create(content=item)
        cc = ContentType.objects.get_for_model(Text)
    elif content_type=="Blank":
        content_item = BlankText.objects.create(correct=item)
        cc = ContentType.objects.get_for_model(BlankText)
    elif content_type=="ABCD":
        content_item = ABCD.objects.create(answers=item)
        cc = ContentType.objects.get_for_model(ABCD)
    else:
        content_item = Hint.objects.create(content=item)
        cc = ContentType.objects.get_for_model(Hint)

    Content.objects.create(exercise=current_ex, content_type=cc,object_id=content_item.id)


def render_checked_exercise(exercise,correct_items,wrong_items):
    checked_exercise=[]
    for content in exercise.content_set.all():  
        if content.item.content_type not in ['text', 'hint']:
            if not content.item in correct_items:
                try: answer = wrong_items[content.item]
                except: answer=""
                if answer == '': answer="___" 
                checked_exercise.append(render_to_string('excercises/checked_exercises/wrong.html',{"correct":content.item.correct_answer,
                "answer":answer}
                ))

            else:
                checked_exercise.append(render_to_string('excercises/checked_exercises/correct.html',{"content":content.item.correct_answer}))
        else:
            checked_exercise.append(content.item.correct_answer)
    return checked_exercise

def check_ansewers(request):
    correct_items = []
    wrong_items = {}
    
    for i in request.POST:
        if i.startswith(('answer_blank','answer_abcd')):
            obj_id = int(i.split("_")[2])
            obj = get_object_or_404(Content, pk=obj_id).item
            answer = request.POST[i].strip()
            if obj.is_correct(answer):
                correct_items.append(obj)
            else:
                wrong_items[obj]=answer
    return correct_items, wrong_items


def  get_page_obj(page_num, paginator):
   
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

def get_page_url(request, name):
    current_site = get_current_site(request).domain
    relativeLink = reverse(name)
    return 'http://'+current_site+relativeLink