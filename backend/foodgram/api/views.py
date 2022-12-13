from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .filters import RecipeFilter, IngredientSearchFilter
from .models import Recipe, Favorite, Cart, Amount_ingredients
from .models import Ingredients, Tag
from .permissions import AuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import RecipesSerializer, CropRecipeSerializer
from .serializers import IngredientSerializer, TagSerializer

from api.pagination import LimitPageNumberPagination


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    permission_classes = (IsAdminOrReadOnly,)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.select_related()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related()
    serializer_class = RecipesSerializer
    pagination_class = LimitPageNumberPagination
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_obj(Favorite, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(Favorite, request.user, pk)
        return None

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_obj(Cart, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(Cart, request.user, pk)

        return None

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = user.cart.all()
        list = {}
        for item in shopping_cart:
            recipe = item.recipe
            ingredients = Amount_ingredients.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in list:
                    list[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    list[name]['amount'] = (
                        list[name]['amount'] + amount
                    )

        shopping_list = []
        for item in list:
            shopping_list.append(f'{item} - {list[item]["amount"]} '
                                 f'{list[item]["measurement_unit"]} \n')
        response = HttpResponse(shopping_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'

        return response

    def add_obj(self, model, user, pk):
        obj = model.objects.prefetch_related('user').filter(
            user=user, recipe__id=pk)
        if obj.exists():
            return Response({
                'errors': 'You already chosen this recipe.'
                }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = CropRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        obj = model.objects.filter(
            user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'The recipe does not exist.'
        }, status=status.HTTP_400_BAD_REQUEST)
