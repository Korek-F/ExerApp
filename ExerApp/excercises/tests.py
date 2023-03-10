from django.test import TestCase, Client
from exer_auth.models import User
from .models import ExerciseSet, Exercise, Text, BlankText, Hint, ABCD, Content
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
import json

class TestExercisesModels(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('john','john@elek.pl','johnhardpassowrd1')
        self.exercise_set = ExerciseSet.objects.create(name="TestName", owner=self.user, description="TEST")
        self.exercise = Exercise.objects.create(exercise_set=self.exercise_set)
    
    def test_exerciseset_model(self):
        exercise_set = ExerciseSet(name="TestName", owner=self.user)
        self.assertEqual(exercise_set.name, 'TestName')
        self.assertEqual(exercise_set.owner, self.user)

    def test_exercise_model(self):
        exercise = Exercise(exercise_set=self.exercise_set)
        self.assertEqual(exercise.exercise_set, self.exercise_set)
    
    def test_contents_models(self):
        content_item = Text.objects.create(content="TEST")
        cc = ContentType.objects.get_for_model(Text)
        Content.objects.create(exercise=self.exercise, content_type=cc,object_id=content_item.id)

        text_content = Content.objects.get(id=1)
        self.assertEqual(text_content.item.content, "TEST")
        self.assertEqual(text_content.item.is_correct("SS"), True)
        self.assertEqual(text_content.item.correct_answer, "TEST")
        self.assertEqual(text_content.item.content_type, "text")


        content_item = BlankText.objects.create(correct="Warsaw")
        cc = ContentType.objects.get_for_model(BlankText)
        Content.objects.create(exercise=self.exercise, content_type=cc,object_id=content_item.id)

        text_content = Content.objects.get(id=2)
        self.assertEqual(text_content.item.correct, "Warsaw")
        self.assertEqual(text_content.item.is_correct("Cracow"), False)
        self.assertEqual(text_content.item.is_correct("Warsaw"), True)
        self.assertEqual(text_content.item.correct_answer, "Warsaw")
        self.assertEqual(text_content.item.content_type, "blank_text")


        content_item = Hint.objects.create(content="hintt")
        cc = ContentType.objects.get_for_model(Hint)
        Content.objects.create(exercise=self.exercise, content_type=cc,object_id=content_item.id)

        text_content = Content.objects.get(id=3)
        self.assertEqual(text_content.item.content, "hintt")
        self.assertEqual(text_content.item.is_correct("Warsaw"), True)
        self.assertEqual(text_content.item.correct_answer, "hintt")
        self.assertEqual(text_content.item.content_type, "hint")


        content_item = ABCD.objects.create(answers="warsaw//cracow//radom")
        cc = ContentType.objects.get_for_model(ABCD)
        Content.objects.create(exercise=self.exercise, content_type=cc,object_id=content_item.id)

        text_content = Content.objects.get(id=4)
        self.assertEqual(text_content.item.answers, "warsaw//cracow//radom")
        self.assertEqual(text_content.item.is_correct("warsaw"), True)
        self.assertEqual(text_content.item.is_correct("elk"), False)
        self.assertEqual(text_content.item.correct_answer, "warsaw")
        self.assertEqual(text_content.item.content_type, "abcd")

        self.assertEqual(self.exercise.number_of_points,2)

class TestExercisesViews(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('john','john@elek.pl')
        self.user.set_password('johnhardpassowrd1')
        self.user.save()

        self.c.login(username='john',password='johnhardpassowrd1')
        ExerciseSet.objects.create(name="set1-ex-abc", description="TEST",
        is_public=True, owner=self.user)
        ExerciseSet.objects.create(name="set2", description="TEST", is_public=True, owner=self.user)
    
    def test_all_exercises_sets_view(self):
        response = self.c.get(reverse('exercises'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'set1-ex-abc')
        self.assertContains(response, 'set2')
        

    def test_exercise_set_edit__learn_check_view(self):
        #edit
        response = self.c.get(reverse('excercise_set_edit_view',kwargs={"set_id":1}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "set1-ex-abc")
        self.assertNotContains(response, "set2")

        response = self.c.post(reverse('excercise_set_edit_view',kwargs={"set_id":1}),{"content-Text-1-1":"start"})
        self.assertEqual(response.status_code, 200)
        exercise = ExerciseSet.objects.get(id=1).exercise_set.first()
        item_content = exercise.content_set.first().item.content
        self.assertEqual(item_content, "start")

        response = self.c.post(reverse('excercise_set_edit_view',kwargs={"set_id":1}),{"content-Text-2-1":"start","content-Blank-2-2":"end22","content-ABCD-2-3":"aa//bb//cc"})
        self.assertEqual(response.status_code,200)
        
        exercise = ExerciseSet.objects.get(id=1).exercise_set.all()[1]
        item_content1 = exercise.content_set.all()[0].item.content
        item_content2 = exercise.content_set.all()[1].item.correct
        item_content3 = exercise.content_set.all()[2].item.answers
        self.assertEqual([item_content1, item_content2, item_content3], ["start","end22","aa//bb//cc"])
        self.assertEqual(exercise.number_of_points,2)

        response = self.c.get(reverse('excercise_set_edit_view',kwargs={"set_id":1}))
        self.assertContains(response,"start")
        self.assertContains(response,"end22")

        #learn
        response = self.c.get(reverse('excercise_set_learn_view',kwargs={"set_id":1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"Learn")
        self.assertContains(response,"start")
        self.assertNotContains(response,"end22")

        #check
        response = self.c.post(reverse('excercise_set_check_view', kwargs={"set_id":1}),{"answer_blanktext_2":["end22"]})
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "Correct: 50.0%")
    
    def test_delete_exercise_view(self):
        exercise_set = ExerciseSet.objects.get(id=1)
        exercise = Exercise.objects.create(exercise_set=exercise_set)
        
        self.assertEqual(exercise_set.exercise_set.first(),exercise)
        response = self.c.post(reverse("excercise_delete_view", kwargs={"set_id":1}),{"delete_id":exercise.id})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(exercise_set.exercise_set.first(),exercise)

    def test_create_exercise_set_view(self):
        response = self.c.get(reverse("excercise_set_create_view"))
        self.assertEqual(response.status_code,200)
        response = self.c.post(reverse('excercise_set_create_view'),{'name':'john_test','description':"TESTTEST"})
        self.assertEqual(response.status_code,200)
        ex_set = ExerciseSet.objects.get(id=3)
        self.assertEqual(ex_set.name, 'john_test')


        


        