from django.contrib import admin
from .models import Exercise, Content, Text, BlankText,ExerciseSet, Hint, ABCD

admin.site.register(ExerciseSet)
admin.site.register(Exercise)
admin.site.register(Content)
admin.site.register(Text)
admin.site.register(BlankText)
admin.site.register(Hint)
admin.site.register(ABCD)

# Register your models here.
