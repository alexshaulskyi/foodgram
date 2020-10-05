from django.contrib import admin

from recipes.models import (Ingredient, Recipe, RecipeIngredientAmount,
                            Tag, Favorite, ShoppingList, Subscription)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement')
    search_fields = ('name',)
    empty_value_display = 'empty'


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    search_fields = ('name', )
    list_filter = ('name', 'author')
    empty_value_display = 'empty'


class RecipeIngredientAmountAdmin(admin.ModelAdmin):
    model = RecipeIngredientAmount
    search_fields = ('amount',)
    list_filter = ('amount',)
    empty_value_display = 'empty'


class TagAdmin(admin.ModelAdmin):
    model = Tag


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = 'empty'


class ShoppingListAdmin(admin.ModelAdmin):
    model = ShoppingList
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = 'empty'


class SubscriptionAmind(admin.ModelAdmin):
    model = Subscription
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = 'empty'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredientAmount, RecipeIngredientAmountAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Subscription, SubscriptionAmind)
