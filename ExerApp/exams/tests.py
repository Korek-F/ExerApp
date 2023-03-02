from django.test import TestCase, Client,TransactionTestCase
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

class TestExamViews(TransactionTestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('john','john@elek.pl','johnhardpassowrd1')
        
        self.c.login(username='john',password='johnhardpassowrd1')

        #Create exercise set with content 
        self.exercise_set = ExerciseSet.objects.create(name="TestName", owner=self.user, description="TEST")
        self.exercise = Exercise.objects.create(exercise_set=self.exercise_set)
        content_item = Text.objects.create(content="TEST")
        cc = ContentType.objects.get_for_model(Text)
        Content.objects.create(exercise=self.exercise, content_type=cc,object_id=content_item.id)
        content_item = ABCD.objects.create(answers="warsaw//cracow//radom")
        cc = ContentType.objects.get_for_model(ABCD)
        Content.objects.create(exercise=self.exercise, content_type=cc,object_id=content_item.id)
    
    def test_create_exam_session_views(self):
        #create session get
        response = self.c.get(reverse('create_exam',kwargs={"id":1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create')
    
        #create session post
        response = self.c.post(reverse('create_exam',kwargs={"id":1}),{"name":"Quick test","description":"aaa"})
        self.assertContains(response, 'Link to exam')
        self.assertEqual(response.status_code,200)
        exam = Exam.objects.first()
        self.assertEqual(exam.name,"Quick test")

        #session start get 
        response = self.c.get(reverse('exam',kwargs={"slug":exam.slug}))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, exam.name)
        
        #session start post
        response = self.c.post(reverse('exam',kwargs={"slug":exam.slug}),{"user_name":"JohnyBravo"})
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "Start Session")

        session = ExamSession.objects.get(id=1)
        self.assertEqual(session.user_name,"JohnyBravo")

        #session get 
        response = self.c.get(reverse('session',kwargs={"slug":session.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cracow")

        #session post
        response = self.c.post(reverse('session',kwargs={"slug":session.slug}),{"answer_abcd_1":"warsaw"})
        answer = SessionAnswer.objects.get(id=1)

        session = ExamSession.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(answer.exam_session.is_finished, session.is_finished)
        self.assertEqual(session.is_finished, True)
        self.assertIsNotNone(session.end_at)
        self.assertEqual(answer.user_answer, "warsaw")
        self.assertContains(response, "Session finished")

        #session results get
        response = self.c.get(reverse('session_results',kwargs={"slug":session.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The session is finished")
        self.assertContains(response, "Correct: 100.0%")

        #Exam list view
        response = self.c.get(reverse('exam_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quick test")
        self.assertContains(response, "1/1")
        
        #exam details view
        response = self.c.get(reverse('exam_owner_view',kwargs={'slug':exam.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "JohnyBravo")
        self.assertContains(response, "The session is finished")
        self.assertContains(response, "Points: ")

        #session details view
        response = self.c.get(reverse('session_detail_view',kwargs={'slug':session.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Answers")
        self.assertContains(response, "warsaw")
    