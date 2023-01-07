# Generated by Django 4.1.4 on 2023-01-02 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('excercises', '0003_content_excercises__content_746caf_idx'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='content',
            name='excercises__content_746caf_idx',
        ),
        migrations.AlterIndexTogether(
            name='content',
            index_together={('content_type', 'object_id')},
        ),
    ]
