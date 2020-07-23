
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

class PublicTagApiTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_tags_api_public_access_fail(self):
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name='Ansuman Singh',
            email='ansuman@yopmail.com',
            password='ansuman123'
        )
        self.client.force_authenticate(self.user)

    
    def test_retrieve_tags(self):
        """ Test retrieving tags """
        
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Strawberry Folds')

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.data, serializer.data)