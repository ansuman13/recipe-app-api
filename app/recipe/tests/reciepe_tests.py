from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **payload):
    default = {
        'title': 'Mushroom Cream Soup',
        'time_minutes': 5,
        'price': 50.10
    }
    default.update(payload)

    return Recipe.objects.create(user=user, **default)


class PublicRecipeApiTest(TestCase):
    """ Test public api for recipe views """

    def setUp(self):
        self.client = APIClient()

    def test_public_recipe_api_fail(self):
        """ test authorization for recipe api"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='ansuman@yopmail.com',
            password='ansuman123',
            name='Ansuman Singh'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe(self):
        """ Test retrieving list of recipes """

        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipe = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipe, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_limited_to_user(self):

        user2 = get_user_model().objects.create_user(
            name='Ansuman',
            email='another@ansuman.com',
            password='ansuman123'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipe = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipe, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
