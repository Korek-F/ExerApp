from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.urls import reverse
from exer_auth.models import User
from categories.models import Category
import random
# Create your models here.


class ExerciseSet(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.TextField(max_length=1000)
    is_public = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, blank=True)


    @property
    def number_of_points(self):
        points = 0
        for i in self.exercise_set.all():
            points += i.number_of_points
        return points

    def __str__(self):
        return str(self.pk)+ " " +self.name

    def get_absolute_url(self):
        return reverse("excercise_set_learn_view", kwargs={"set_id": self.pk})
    

class Exercise(models.Model):
    exercise_set = models.ForeignKey("ExerciseSet", on_delete=models.CASCADE)
    def __str__(self):
        return str(self.pk)+ " " +self.exercise_set.name

    @property
    def number_of_points(self):
        points = 0
        for i in self.content_set.all():
            if i.item.content_type in ["blank_text",'abcd']:
                points+=1
        return points
    


class Content(models.Model):
    exercise = models.ForeignKey("Exercise",  on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
    limit_choices_to={'model__in':('text','blanktext', 'hint','abcd')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    def render(self):
        return render_to_string(
            f'excercises/content/{self.item.content_type}.html',
            {'item':self.item, 'content':self}
        )

    def __str__(self):
        return str(self.pk)+" "+ str(self.item)
    

class ItemBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
       


    

class Text(ItemBase):
    content = models.TextField()

    def is_correct(self, answer):
        return True 
    
    @property
    def correct_answer(self):
        return self.content
    
    @property
    def content_type(self):
        return "text"

    def __str__(self):
        return str(self.pk) +" "+self.content[:50]

class BlankText(ItemBase):
    correct = models.TextField()

    def __str__(self):
        return str(self.pk) +" "+self.correct[:50]

    def is_correct(self, answer):
        return self.correct.lower() == answer.lower()  
    
    @property
    def correct_answer(self):
        return self.correct
    
    @property
    def content_type(self):
        return "blank_text"

class Hint(ItemBase):
    content = models.TextField()

    def is_correct(self, answer):
        return True 
    @property
    def correct_answer(self):
        return self.content
    @property
    def content_type(self):
        return "hint"
    def __str__(self):
        return str(self.pk) +" "+self.content[:50]


class ABCD(ItemBase):
    # This field contais answers in following pattern
    # Good_answer//Bad_answer//bad_answer//...
    # Example
    # Question: The capitol of Poland is ____ 
    # Answers_field:    Warsaw//Cracow//Radom
    answers = models.CharField(max_length=255)

    def is_correct(self, answer):
        return self.answers.split("//")[0]==answer 

    @property
    def get_answers_to_render(self):
        answers = self.answers.split("//") 
        random.shuffle(answers)
        return answers

    @property
    def correct_answer(self):
        return self.answers.split("//")[0]

    @property
    def content_type(self):
        return "abcd"
    
    def __str__(self):
        return str(self.pk) +" "+self.answers[:50]