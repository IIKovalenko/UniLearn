from django.test import TestCase

from account.models import UserProfile


class AutoLoginTestCase(TestCase):
    def create_and_login_user(self):
        login, password, email = 'test_user', 'pwd', 'test@user.com'
        try:
            self.user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            self.user = UserProfile.objects.create_user(login, email, password)
        self.client.login(username=login, password=password)

    def setUp(self):
        self.create_and_login_user()
