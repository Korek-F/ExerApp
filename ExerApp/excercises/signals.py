from django.db.models.signals import m2m_changed
from .models import ExerciseSet
from django.core.exceptions import ValidationError


def categories_changed(sender, **kwargs):
    if kwargs['instance'].categories.count()>5:
        raise ValidationError("You can't add more than 5 categories!")

m2m_changed.connect(categories_changed, sender=ExerciseSet.categories.through)
