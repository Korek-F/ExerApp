from django.test import TestCase, Client
from .models import Category
from excercises.models import ExerciseSet
from exer_auth.models import User
from django.urls import reverse

class TestCategoriesModels(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('john','john@elek.pl','johnhardpassowrd1')
        self.exercise_set = ExerciseSet.objects.create(name="TestName", owner=self.user, description="TEST")
    
    def test_category_model(self):
        category = Category.objects.create(name="tests")
        self.assertEqual(category.name,"tests")
        self.assertEqual(category.popularity,0)
        self.assertEqual(category.number_of_sets,0)
        self.exercise_set.categories.add(category)
        self.assertEqual(category.number_of_sets,1)

class TestCategoriesViews(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('john','john@elek.pl','johnhardpassowrd1')
        self.exercise_set = ExerciseSet.objects.create(name="TestName", owner=self.user, description="TEST")
    
    def test_all_categories_view(self):
        response = self.c.get(reverse('all_categories'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "test_category_1")
        Category.objects.create(name="test_category_1")

        response = self.c.get(reverse('all_categories'))
        self.assertContains(response, "test_category_1")
    
    def test_category_detail_view(self):
        Category.objects.create(name="test_category_1")
        response = self.c.get(reverse('category_detail', kwargs={"name":"test_category_1"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_category_1")