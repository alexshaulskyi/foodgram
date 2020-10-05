from django.db import models

from users.models import User


class MeasurementsChoices(models.TextChoices):
    kilogramms = 'кг.'
    gramms = 'г.'
    pieces = 'шт.'
    tea_spoon = 'ч.л.'
    table_spoon = 'ст.л.'
    milliliters = 'мл.'
    litters = 'л.'
    taste = 'по вкусу'


class Tag(models.Model):
    name = models.CharField(max_length=20)
    style = models.CharField(max_length=20)
    template_name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )
    measurement = models.CharField(
        max_length=15,
        choices=MeasurementsChoices.choices,
        blank=False,
        null=False
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='recipes',
        blank=False,
        null=False
    )
    name = models.CharField(max_length=50, blank=False, null=False)
    tags = models.ManyToManyField(Tag, related_name='recipes', blank=False)
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        blank=True
    )
    image = models.ImageField(blank=False)
    description = models.TextField(blank=False, null=False)
    cooking_time = models.CharField(max_length=4, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=False, null=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        blank=False
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='get_amount',
        blank=False
    )
    amount = models.CharField(max_length=3, blank=False, null=False)

    def __str__(self):
        return f'{self.ingredient.name} - {self.recipe.name}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='selecting',
        blank=False
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='selected',
        blank=False
    )

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='choosing',
        blank=False
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='chosen',
        blank=False
    )

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed',
        blank=False
    )

    def __str__(self):
        return f'{self.user.username} - {self.user.username}'
