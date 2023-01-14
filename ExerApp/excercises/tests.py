from django.test import TestCase, Client
from exer_auth.models import User
from .models import ExerciseSet, Exercise, Text, BlankText, Hint, ABCD, Content
from django.contrib.contenttypes.models import ContentType

class TestExercisesModel(TestCase):
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


