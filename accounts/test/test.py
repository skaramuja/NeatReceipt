from django.test import TestCase
from accounts.models import Account, MyAccountManager


class AccountUserTestCase(TestCase):
    def setUp(self):
        self.user = MyAccountManager.create_user(username='testuser', email='test@gmail.com', password='password')

    def test_user_login(self):
        """	 """
        login = self.client.login(username='testuser', password='password')
