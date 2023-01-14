from django.test import TestCase, Client
from .models import User
from django.urls import reverse
from django.contrib import auth

class TestExerAuhtModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john','john@elek.pl','johnhardpassowrd1')

    def test_user_model(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.username, 'john')
        self.assertEqual(user.email, 'john@elek.pl')

class TestExerAuthViews(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('john','john@elek.pl','johnhardpassowrd1')
    
    def test_login_and_logout_view(self):
        user = auth.get_user(self.c)
        self.assertEqual(user.is_authenticated, False)
        response = self.c.get(reverse("login"))
        self.assertEqual(response.status_code,200)
        response = self.c.post(reverse('login'),{'username':'john','password':'johnhardpassowrd1'})
        self.assertEqual(response.status_code,302)
        user = auth.get_user(self.c)
        self.assertEqual(user.is_authenticated, True)

        #Logout
        response = self.c.post(reverse("logout"))
        self.assertEqual(response.status_code,302)
        user = auth.get_user(self.c)
        self.assertEqual(user.is_authenticated, False)




        