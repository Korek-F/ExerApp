from django.db import models
from exer_auth.models import User
from excercises.models import ExerciseSet, Content
from django.urls import reverse
from django.utils.text import slugify
import random
from django.utils import timezone

class Exam(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_set = models.ForeignKey(ExerciseSet, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    slug = models.SlugField(unique=True, blank=True)

    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)+str(random.randint(0,10000))
        super(Exam, self).save(*args, **kwargs)


    def get_absolute_url(self):      
        return reverse('exam', args=[str(self.slug)])
    
    
    def is_ended(self):
        if not self.end_at:
            return False
        return self.end_at<timezone.now()
    
    def is_started(self):
        if not self.start_at:
            return True
        return self.start_at<timezone.now()
        


class ExamSession(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    start_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(blank=True,null=True, default=None)
    is_finished = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user_name)+str(random.randint(0,10000))
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
        return f'{self.id} {self.exam_session.user_name} {self.user_answer}'
