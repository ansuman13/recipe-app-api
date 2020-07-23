from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from recipe.serializers import TagSerializer
from rest_framework.authentication import TokenAuthentication
from core.models import Tag

# Create your views here.

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).order_by('-name')
