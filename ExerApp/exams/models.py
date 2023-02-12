from django.db import models
from exer_auth.models import User
from excercises.models import ExerciseSet, Content
from django.urls import reverse
from django.utils.text import slugify


class Exam(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_set = models.ForeignKey(ExerciseSet, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Exam, self).save(*args, **kwargs)


    def get_absolute_url(self):      
        return reverse('exam', args=[str(self.slug)])


class ExamSession(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    start_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(blank=True,null=True, default=None)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user_name)
        super(ExamSession, self).save(*args, **kwargs)

    def __str__(self):
        return self.user_name
    
    def get_absolute_url(self):      
        return reverse('session', args=[str(self.slug)])

    
class SessionAnswer(models.Model):
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE)
    item = models.ForeignKey(Content, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.user_answer
