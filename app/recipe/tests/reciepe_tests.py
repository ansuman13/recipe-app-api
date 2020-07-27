from core.models import Recipe, Tag, Ingredient
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer
from rest_framework import status
from rest_framework.test import APIClient

RECIPE_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **kwargs):
    default = {
        'title': 'Mushroom Cream Soup',
        'time_minutes': 5,
        'price': 50.10
    }
    default.update(kwargs)
    default.update(default)

    return Recipe.objects.create(user=user, **default)


def detail_url(id):
    return reverse('recipe:recipe-detail', args=[id])


class PublicRecipeApiTest(TestCase):
    """ Test public api for recipe views """

    def setUp(self):
        self.client = APIClient()

    def test_public_recipe_api_fail(self):
        """ test authorization for recipe api"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


def sample_tag(user, name):
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, **kwargs):
    default = {
        'name': 'Cinnamon'
    }
    default.update(kwargs)
    return Ingredient.objects.create(user=user, **default)


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

    def test_view_recipe_detail(self):
        """ Test viewing a recipe detail """
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user, name='Kitchen'))
        recipe.ingredients.add(sample_ingredient(user=self.user))
        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_create_success(self):
        payload = {
            'title': 'Huma Quershi Taste Curry',
            'price': 100.50,
            'time_minutes': 20,
        }
        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])

        for key in payload:
            self.assertEqual(getattr(recipe, key), payload[key])

    def test_recipe_create_with_tags(self):
        """ test for recipe for create with tags """

        tag1 = sample_tag(user=self.user, name='foodie')
        tag2 = sample_tag(user=self.user, name='mocha')
        payload = {
            'title': 'human beings eaten alive',
            'price': 20.00,
            'time_minutes': 100,
            'tags': [tag1.id, tag2.id]
        }

        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_recipe_create_with_ingredients(self):
        """ test for recipe create with ingredients """

        ingredient1 = sample_ingredient(user=self.user, name='Panner')
        ingredient2 = sample_ingredient(user=self.user, name='Corrainder')
        payload = {
            'title': 'Panner curry',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 30,
            'price': 230
        }
        res = self.client.post(RECIPE_URL, payload)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)

    def test_recipe_update_partial(self):
        """ Test for partial update of recipe"""
        recipe = sample_recipe(self.user)
        tag1 = sample_tag(self.user, name='Tag1')
        recipe.tags.add(tag1)
        recipe_edit = {
            'title': 'Panner Corma'
        }
        url = detail_url(recipe.id)
        res = self.client.patch(url, recipe_edit)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], recipe_edit['title'])

    def test_recipe_ful_update(self):
        """ Test for recipe detail api full update"""
        recipe = sample_recipe(self.user)
        tag1 = sample_tag(self.user, name='Dahi')
        recipe.tags.add(tag1)
        res = self.client.put(detail_url(recipe.id), {
            'title': 'Sahi Panner',
            'price': 80,
            'time_minutes': 5,
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], 'Sahi Panner')

