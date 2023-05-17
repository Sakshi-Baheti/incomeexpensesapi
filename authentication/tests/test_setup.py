from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetup(APITestCase):
   
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
   
        user_data = {
           'email' : "email@gmail.com",
           "username" : "email",
           "password" : "email@gmail.com"
        }
       
        return super().setUp()
   

    def tearDown(self):
        return super().tearDown()
  
