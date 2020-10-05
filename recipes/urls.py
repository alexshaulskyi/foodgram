from django.urls import path
from django.contrib.auth.decorators import login_required

from recipes.views import (Index, CreateRecipe, ProcessIngredients,
                           ChangeRecipe, RecipeDetail, AuthorDetail,
                           Favorites, ShoppingListView, GetShoppingList,
                           Subscriptions, DeleteRecipe)


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('ingredients/', login_required(ProcessIngredients.as_view()), name='process_ingredients'),
    path('create_recipe/', login_required(CreateRecipe.as_view()), name='create_recipe'),
    path('change_recipe/<slug:slug>/', login_required(ChangeRecipe.as_view()), name='change_recipe'),
    path('author/<str:username>/', AuthorDetail.as_view(), name='detail_author'),
    path('recipe/<slug:slug>/', RecipeDetail.as_view(), name='detail_recipe'),
    path('favorites/', login_required(Favorites.as_view()), name='favorites'),
    path('shopping_list/', login_required(ShoppingListView.as_view()), name='shopping_list'),
    path('get_shopping_list/', login_required(GetShoppingList.as_view()), name='get_shopping_list'),
    path('subscriptions/', login_required(Subscriptions.as_view()), name='subscriptions'),
    path('recipe/delete/<slug:slug>', login_required(DeleteRecipe.as_view()), name='delete_recipe')
]
