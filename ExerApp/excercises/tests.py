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
        self.exercise_set = ExerciseSet.objects.create(name="TestName", owner=self.user)
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

class TestExercisesViews(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('john','john@elek.pl','johnhardpassowrd1')
        ExerciseSet.objects.create(name="set1-ex-abc", owner=self.user)
        ExerciseSet.objects.create(name="set2", owner=self.user)
    
    def test_all_exercises_sets_view(self):
        response = self.c.get(reverse('exercises'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'set1-ex-abc')
        self.assertContains(response, 'set2')
        

