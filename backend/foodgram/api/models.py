from users.models import User
from django.db import models
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator


class Ingredients(models.Model):
    name = models.CharField(max_length=200, blank=True)
    measurement_unit = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient')
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.TextField(max_length=200, blank=True)
    color = ColorField(default='#FF0000')
    slug = models.SlugField(max_length=200, blank=False, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
    )
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='Amount_ingredients',
        related_name='recipies',
    )
    name = models.TextField(max_length=200, blank=True)
    image = models.ImageField(upload_to='recipes/', blank=True)
    text = models.TextField(max_length=200, blank=True)
    cooking_time = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(
            1,
            message='Minimum cooking time 1 minute'
            ),),
        blank=True
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Amount_ingredients(models.Model):
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(
            1,
            message='Minimum amount of ingridients 1'),),
        blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Amount ingredients'
        verbose_name_plural = 'Amount ingredients'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique ingredients recipe')
        ]
    
    def __str__(self):
        return self.amount


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='favourites'),
        ]

    def __str__(self):
        return self.user


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
    )

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='shopping_list'),
        ]

    def __str__(self):
        return self.user
