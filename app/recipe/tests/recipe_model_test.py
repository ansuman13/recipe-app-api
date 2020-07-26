from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user():
    return get_user_model().objects.create_user(
        email='ansuman@yopmail.com',
        password='kathmandu@123',
        name='Ansuman Singh'
    )


class RecipeAppTest(TestCase):
    """ Test for recipe app """

    def test_tag_str(self):
        """ Test the tag string representation """
        tag = models.Tag.objects.create(
            name='Kitchen',
            user=sample_user()
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """ Test the Ingredient model str representation """

        ingredient = models.Ingredient.objects.create(
            name='Peper',
            user=sample_user()
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_reciepe_str(self):
        """ Test the Reciepe Model for str representation """

        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Panner Tika curry masala',
            price=50.12,
            time_minutes=5
        )

        self.assertEqual(str(recipe), recipe.title)
