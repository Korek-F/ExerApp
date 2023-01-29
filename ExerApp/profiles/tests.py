from django.test import TestCase, Client
from django.urls import reverse
from exer_auth.models import User
from excercises.models import ExerciseSet
# Create your tests here.
class TestProfilesViews(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('john','john@elek.pl')
        self.user.set_password('johnhardpassowrd1')
        self.user.save()
        ExerciseSet.objects.create(name="set2-23414-ex", description="TEST", is_public=True, owner=self.user)
    
    def test_user_profile_page(self):
        response = self.c.get(reverse('profile_detail', kwargs={"pk":1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'john')
        self.assertContains(response, 'set2-23414-ex')