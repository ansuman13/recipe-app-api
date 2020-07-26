from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Tag, Ingredient
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')
INGREDIENT_URL = reverse('recipe:ingredient-list')


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

    def test_tags_limited_to_user(self):
        """ Test tags limited to user """

        user2 = get_user_model().objects.create_user(
            email='ansuman12@yopmail.com',
            password='ansuman@123'
        )
        Tag.objects.create(user=user2, name='HoneyMoon')
        tag2 = Tag.objects.create(user=self.user, name='NakedMoon')

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag2.name)

    def test_create_tag_successful(self):
        """ Test create tag successful """

        payload = {'name': 'ZebroCross'}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_invalid_tag_fail(self):
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PublicIngredientTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_ingredient_api_public_test(self):
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='ansuman@yopmail.com',
            password='ansuman123',
            name='ansuman singh'
        )
        self.client.force_authenticate(self.user)

    def test_ingredient_create_success(self):
        payload = {'name': 'Vinegar'}
        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Ingredient.objects.filter(
            name=payload.get('name'),
            user=self.user
        ).exists()
        self.assertTrue(exists)

    def test_invalid_ingredient_create_fail(self):
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
