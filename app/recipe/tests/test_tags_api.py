from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Recipe

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTest(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """"Test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    """Test the authorized user tags API"""

    def setUp(self) -> None:
        payload = {'email': 'test@gmail.com',
                   'password': 'testtest',
                   'name': 'mehran motmaen',
                   }
        self.user = get_user_model().objects.create(**payload)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Desert')

        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        payload = {'email': 'tefsfsst@gmail.com',
                   'password': 'testtest',
                   'name': 'mehrfdsan fds',
                   }
        user2 = get_user_model().objects.create(**payload)
        Tag.objects.create(user=user2, name='Desert')
        Tag.objects.create(user=self.user, name='Vegan')
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], 'Vegan')

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(user=self.user, name=payload['name']).exists()
        self.assertTrue(exists)

    def test_craete_tag_invalid(self):
        """"Test creating a new tag with invalid payload  """

        payload = {'name': ""}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags_assigned_to_recipes(self):
        """Test filtering tags by those assigned to recipes"""
        tag1 = Tag.objects.create(user=self.user, name='Desert')
        tag2 = Tag.objects.create(user=self.user, name='Vegan')
        recipe = Recipe.objects.create(title='test', time_minutes=10, price=5.00, user=self.user)
        recipe.tags.add(tag1)
        res = self.client.get(TAGS_URL, {'assigned_only': 1})
        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_tags_assigned_unique(self):
        """Test filtering tags by assigned return unique items"""
        tag1 = Tag.objects.create(user=self.user, name='Desert')
        Tag.objects.create(user=self.user, name='Vegan')
        recipe1 = Recipe.objects.create(title='test', time_minutes=10, price=5.00, user=self.user)
        recipe1.tags.add(tag1)

        recipe2 = Recipe.objects.create(title='test 2', time_minutes=120, price=2.00, user=self.user)

        recipe2.tags.add(tag1)
        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
