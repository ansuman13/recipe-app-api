from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from recipe.serializers import TagSerializer, IngredientSerializer
from rest_framework.authentication import TokenAuthentication
from core.models import Tag, Ingredient


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        return Ingredient.objects.filter(
            user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
