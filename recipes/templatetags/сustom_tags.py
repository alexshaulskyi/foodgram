from django import template

from recipes.models import Recipe, Favorite, ShoppingList, Subscription

register = template.Library()


@register.filter(name='obtain_parameters')
def obtain_parameters(value):
    return value.getlist('filters')


@register.filter(name='obtain_link')
def obtain_link(request, tag):
    new_request = request.GET.copy()

    if tag.name in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.name)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.name)

    return new_request.urlencode()


@register.filter(name='if_has_tag')
def if_has_tag(recipe_id, tag_id):
    return Recipe.objects.filter(id=recipe_id, tags__id=tag_id).exists()


@register.simple_tag(takes_context=True)
def presave_params(context, **kwargs):
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    return query.urlencode()


@register.filter(name='is_in_favs')
def is_in_favs(recipe, request):
    return Favorite.objects.filter(
            user=request.user, recipe=recipe
        ).exists()


@register.filter(name='is_in_shopping_list')
def is_in_shopping_list(recipe, request):
    return ShoppingList.objects.filter(
            user=request.user, recipe=recipe
        ).exists()


@register.filter(name='is_subscribed')
def is_subscribed(author, request):
    return Subscription.objects.filter(
            user=request.user, author=author
        ).exists()


@register.filter(name='count_recipes')
def count_recipes(author):
    amount = author.recipes.count()
    if amount <= 3:
        return
    return amount - 3


@register.filter(name='shopping_list_amount')
def shopping_list_amount(user):
    return Recipe.objects.filter(chosen__user=user).count()
