from django.test import TestCase, Client
from .models import Exam, ExamSession, SessionAnswer
from excercises.models import ExerciseSet, Exercise,Content,Text,ABCD
from django.contrib.contenttypes.models import ContentType
from exer_auth.models import User
from django.urls import reverse

class TestExamModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john','john@elek.pl','johnhardpassowrd1')
        self.exam = Exam(owner=self.user,name="Exam_t",description="Test desc")
        self.session = ExamSession(exam=self.exam,user_name="JohnyTest")

    def test_exam_model(self):
        exam = Exam(owner=self.user,name="Exam_t",description="Test desc")
        self.assertEqual(exam.name,"Exam_t")
        self.assertEqual(exam.description,"Test desc")
        self.assertEqual(exam.owner.username,"john")

    def test_exam_session_model(self):
        session = ExamSession(exam=self.exam,user_name="JohnyTest")
        self.assertEqual(session.exam, self.exam)
        self.assertEqual(session.user_name, "JohnyTest")
        self.assertEqual(session.is_finished,False)
        self.assertEqual(session.points,0)

class TestExamViews(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('john','john@elek.pl','johnhardpassowrd1')
        
        self.c.login(username='john',password='johnhardpassowrd1')

        self.exercise_set = ExerciseSet.objects.create(name="TestName", owner=self.user, description="TEST")
        self.exercise = Exercise.objects.create(exercise_set=self.exercise_set)
        content_item = Text.objects.create(content="TEST")
        cc = ContentType.objects.get_for_model(Text)
        Content.objects.create(exercise=self.exercise, content_type=cc,object_id=content_item.id)
        content_item = ABCD.objects.create(answers="warsaw//cracow//radom")
        cc = ContentType.objects.get_for_model(ABCD)
        Content.objects.create(exercise=self.exercise, content_type=cc,object_id=content_item.id)
    
    def test_create_exam_view(self):
        response = self.c.get(reverse('create_exam',kwargs={"id":1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create')


        response = self.c.post(reverse('create_exam',kwargs={"id":1}),{"name":"Quick test","description":"aaa"})
        self.assertEqual(response.status_code,200)