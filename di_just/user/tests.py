# Python
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from user.models import Profile
from user.token import account_activation_token

User = get_user_model()

class RegisterUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

class ActivateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = account_activation_token.make_token(self.user)
        self.activate_url = reverse('activate', kwargs={'uid': self.user.pk, 'token': self.token})

    def test_activate_user(self):
        response = self.client.put(self.activate_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.profile.is_verified)

class LoginAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.profile.is_verified = True
        self.user.profile.save()
        self.login_url = reverse('login')
        self.login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

    def test_login_user(self):
        response = self.client.post(self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Python
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from user.models import Profile

User = get_user_model()

class ProfileUpdateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.update_url = reverse('profile-update', kwargs={'pk': self.user.profile.pk})
        self.update_data = {
            'bio': 'This is a test bio',
            'age': 25
        }

    def test_update_profile(self):
        response = self.client.put(self.update_url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'This is a test bio')
        self.assertEqual(self.user.profile.age, 25)

# Add similar test classes for ProfilePictureUpdateAPI, ProfileInfoAPI, ProfileGetInfo, UserInfoAPI, ProfileListAPI

class FollowUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword1')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        self.client.force_authenticate(user=self.user1)
        self.follow_url = reverse('follow', kwargs={'pk': self.user2.profile.pk})

    def test_follow_user(self):
        response = self.client.put(self.follow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.profile.refresh_from_db()
        self.assertIn(self.user2.profile, self.user1.profile.follows.all())

class UnfollowUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword1')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        self.user1.profile.follows.add(self.user2.profile)
        self.client.force_authenticate(user=self.user1)
        self.unfollow_url = reverse('unfollow', kwargs={'pk': self.user2.profile.pk})

    def test_unfollow_user(self):
        response = self.client.put(self.unfollow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.profile.refresh_from_db()
        self.assertNotIn(self.user2.profile, self.user1.profile.follows.all())