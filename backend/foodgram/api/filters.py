# from django_filters import rest_framework as filters

# from .models import Recipe

# class RecipeFilter(filters.FilterSet):
#     author = filters.CharFilter(
#         field_name='autor',
#         lookup_expr='icontains'
#     )
#     tags = filters.CharFilter(
#         field_name='category__slug',
#         lookup_expr='icontains'
#     )

#     class Meta:
#         model = Recipe
#         fields = ['author', 'tags']