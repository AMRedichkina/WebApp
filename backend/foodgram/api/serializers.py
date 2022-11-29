from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Recipe

class RecipesSerializer(serializers.Serializer):

    class Meta:
        fields = '__all__'
        model = Recipe

class CropRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')