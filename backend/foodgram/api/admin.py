from django.contrib import admin
from .models import Ingredients, Recipe, Tag, Amount_ingredients
from .models import Favorite, Cart



class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites')
    list_filter = ('author', 'name', 'tags')

    def count_favorites(self, obj):
        return obj.favorites.count()


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


class AmAmount_ingredients(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')

admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredients, IngredientAdmin)
admin.site.register(Amount_ingredients)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Cart)
admin.site.register(Favorite)
