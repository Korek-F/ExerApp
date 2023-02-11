from django.db import models
from exer_auth.models import User
from excercises.models import ExerciseSet, ContentType
from django.urls import reverse

class Exam(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_set = models.ForeignKey(ExerciseSet, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):      
        return reverse('exam', args=[str(self.slug)])


class ExamSession(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    start_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(blank=True,null=True, default=None)
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return self.user_name

    
class SessionAnswer(models.Model):
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE)
    item = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.user_answer
