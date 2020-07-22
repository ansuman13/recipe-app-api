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
