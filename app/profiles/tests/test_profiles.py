import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from profiles.api.serializers import (AvatarSerializer, ProfileSerializer,
                                      ProfileStatusSerializer)
from profiles.models import Profile, ProfileStatus
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

REGISTER_URL = '/api/rest-auth/regisration/'
PROFILES_URL = reverse("profile-list")
PROFILE_DETAIL_URL = reverse("profile-detail", kwargs={"pk": 1})


class RegistrationTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_register(self):
        """ test is user register """
        data = {
            'username': 'mitzy1012',
            'email': 'mitsz@gmail.com',
            'password1': 'testpass1@',
            'password2': 'testpass1@'
        }
        response = self.client.post(REGISTER_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('key', response.data)


class ProfileTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="davinci", password="Sometnewpass123%")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        """ authenticate set up"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_authenticated_user_profile_list(self):
        """ test authenticated user can reveiece profile_list data"""
        response = self.client.get(PROFILES_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_profile_list(self):
        """ test unauthenticated user cannot reveiece profile_list data"""
        self.client.force_authenticate(user=None)
        response = self.client.get(PROFILES_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_profile_detail(self):
        """ test authenticated user can reveiece profile_detail data"""
        response = self.client.get(PROFILE_DETAIL_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], "davinci")

    def test_unauthenticated_user_profile_detail(self):
        """ test unauthenticated user cannot reveiece profile_detail data"""
        self.client.force_authenticate(user=None)
        response = self.client.get(PROFILE_DETAIL_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_by_owner(self):
        """test if user can update"""
        response = self.client.put(PROFILE_DETAIL_URL, {
            "city": 'Florence', 'bio': 'Ren Genius'})
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {
                         'id': 1, 'user': 'davinci', 'bio': 'Ren Genius', 'city': 'Florence',
                         'avatar': None})
        # self.assertIn('user', response.data)

    def test_update_user_by_other_user(self):
        """test if random user cant update"""
        random_user = User.objects.create_user(
            username='randome', password='randompass23^')
        self.client.force_authenticate(user=random_user)

        response = self.client.put(PROFILE_DETAIL_URL, {
            "city": 'Florence', 'bio': 'Ren Genius'})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn('florence', response.data)
