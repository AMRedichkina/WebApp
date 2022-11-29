from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Recipe
from .serializers import RecipesSerializer
from django_filters.rest_framework import DjangoFilterBackend


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author', 'tags')

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)