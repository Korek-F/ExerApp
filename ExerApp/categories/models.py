from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    @property
    def number_of_sets(self):
        return self.exerciseset_set.all().count()

    