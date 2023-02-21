from django.test import TestCase
from .models import Exam, ExamSession, SessionAnswer
from exer_auth.models import User

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