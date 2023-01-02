from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(email='motmean73@gmail.com', password='TESTPASS')
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(email='Test@gmail.com', password='TESTPASSTEST',
                                                         name='test_user')

    def test_users_listed(self):
        """Test that users are listed on your page  """
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        print(res)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
