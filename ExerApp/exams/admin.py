from django.contrib import admin
from .models import SessionAnswer,ExamSession,Exam
# Register your models here.
admin.site.register(SessionAnswer)
admin.site.register(ExamSession)
admin.site.register(Exam)