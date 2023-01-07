from django.contrib import admin
from .models import Exercise, Content, Text, BlankText,ExerciseSet

admin.site.register(ExerciseSet)
admin.site.register(Exercise)
admin.site.register(Content)
admin.site.register(Text)
admin.site.register(BlankText)

# Register your models here.
