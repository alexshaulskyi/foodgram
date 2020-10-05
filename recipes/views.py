import json
from typing import Dict

from django.shortcuts import render, get_object_or_404
from django.views.generic import (View, FormView, UpdateView,
                                  DetailView, DeleteView)
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from slugify import Slugify, CYRILLIC

from recipes.forms import CreateRecipeForm
from recipes.models import (
    Ingredient, Recipe, RecipeIngredientAmount,
    Favorite, ShoppingList, MeasurementsChoices
    )
from users.models import User
from recipes.custom_views import CustomListView, get_ings_amount


class Index(CustomListView):

    model = Recipe
    templates = {
        'auth': 'index_authenticated.html',
        'anonymous': 'index_anonymous.html'
    }

    def get(self, request):

        if self.get_filters():
            initial_queryset = self.model.objects.filter(
                tags__name__in=self.get_filters()
            ).distinct()
        else:
            initial_queryset = self.model.objects.all().distinct()

        object_list = self.paginate_it(initial_queryset, 9)

        context = {
            'object_list': object_list,
            'tags': self.get_tags()
        }

        return render(request, self.get_template(), context)


class CreateRecipe(FormView):

    template_name = 'create_recipe.html'
    form_class = CreateRecipeForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):

        ing_amount: Dict[str, int] = get_ings_amount(self.request)

        if not ing_amount:
            form = self.form_class(instance=form.instance)
            context = {'form': form, 'ing_error': True}
            return render(self.request, self.template_name, context)

        form.instance.author = self.request.user
        slugify = Slugify(pretranslate=CYRILLIC, to_lower=True)
        form.instance.slug = slugify(form.instance.name)
        recipe = form.save()

        ing_queryset = Ingredient.objects.filter(name__in=ing_amount.keys())
        for obj in ing_queryset:
            RecipeIngredientAmount.objects.create(
                ingredient=obj,
                recipe=recipe,
                amount=ing_amount[obj.name]
            )
            recipe.ingredients.add(obj)
        return super().form_valid(form)


class ProcessIngredients(View):

    def get(self, request):

        data = []

        string = request.GET.get('query')

        if ':' in string:
            elements = string.split(',')
            name, measurement = elements
            if Ingredient.objects.filter(name=name).exists():
                data.append({"title": 'Ингредиент с таким именем уже есть'})
                return JsonResponse(data, safe=False)
            if not measurement.strip(':') in MeasurementsChoices.values:
                data.append({"title": 'Недопустимые единицы измерения'})
                return JsonResponse(data, safe=False)
            Ingredient.objects.create(
                name=name,
                measurement=measurement.strip(':')
            )
        else:
            name = string

        error = 'Такого ингредиента нет, добавьте его, следуя инструкции'

        queryset = Ingredient.objects.filter(name__startswith=name)

        if not queryset:
            data.append({"title": error})
        else:
            for item in queryset:
                data.append({
                    "title": item.name,
                    "dimension": item.measurement
                })

        return JsonResponse(data, safe=False)


class ChangeRecipe(UpdateView):

    template_name = 'change_recipe.html'
    form_class = CreateRecipeForm
    success_url = reverse_lazy('index')
    model = Recipe

    def form_valid(self, form):

        new_ings: Dict[str, int] = get_ings_amount(self.request)

        if not new_ings:
            form = self.form_class(instance=form.instance)
            context = {'form': form, 'ing_error': True}
            return render(self.request, self.template_name, context)

        for obj in form.instance.ingredients.all():
            if obj.name not in new_ings.keys():
                form.instance.ingredients.remove(obj)
                RecipeIngredientAmount.objects.filter(
                    ingredient=obj,
                    recipe=form.instance
                ).delete()
            else:
                RecipeIngredientAmount.objects.filter(
                    ingredient=obj,
                    recipe=form.instance
                ).update(
                    amount=new_ings[obj.name]
                )
                del new_ings[obj.name]

        new_queryset = Ingredient.objects.filter(name__in=new_ings.keys())
        for obj in new_queryset:
            RecipeIngredientAmount.objects.create(
                ingredient=obj,
                recipe=form.instance,
                amount=new_ings[obj.name]
            )
            form.instance.ingredients.add(obj)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.object.slug
        return context


class RecipeDetail(DetailView):

    model = Recipe

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return 'recipe_page.html'
        return 'recipe_page_anonymous.html'


class AuthorDetail(CustomListView):

    model = Recipe
    templates = {'any': 'author.html'}

    def get(self, request, username):

        author = get_object_or_404(User, username=username)

        if self.get_filters():
            initial_queryset = self.model.objects.filter(
                tags__name__in=self.get_filters(),
                author=author
            ).distinct()
        else:
            initial_queryset = self.model.objects.filter(
                author=author
            ).distinct()

        object_list = self.paginate_it(initial_queryset, 9)

        context = {
            'object_list': object_list,
            'tags': self.get_tags(),
            'author': author
        }

        return render(request, self.get_template(), context)


class Favorites(CustomListView):

    model = Recipe
    templates = {'any': 'favorites.html'}

    def get(self, request):

        if self.get_filters():
            initial_queryset = self.model.objects.filter(
                tags__name__in=self.get_filters(),
                selected__user=request.user
            ).distinct()
        else:
            initial_queryset = self.model.objects.filter(
                selected__user=request.user
            ).distinct()
        object_list = self.paginate_it(initial_queryset, 9)

        context = {
            'object_list': object_list,
            'tags': self.get_tags()
        }

        return render(request, self.get_template(), context)

    def post(self, request):

        request_data = json.loads(request.body)

        recipe = get_object_or_404(self.model, id=request_data['id'])

        obj, created = Favorite.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )

        if not created:

            obj.delete()

        return JsonResponse({'success': True})


class ShoppingListView(CustomListView):

    model = Recipe
    templates = {'any': 'shopping_list.html'}

    def get(self, request):

        object_list = Recipe.objects.filter(
            chosen__user=request.user
        )

        context = {
            'object_list': object_list
        }

        return render(request, self.get_template(), context)

    def post(self, request):

        request_data = json.loads(request.body)

        recipe = get_object_or_404(self.model, id=request_data['id'])

        obj, created = ShoppingList.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )

        if not created:

            obj.delete()

        return JsonResponse({'success': True})


class GetShoppingList(View):

    def get(self, request):

        object_list = Recipe.objects.filter(chosen__user=request.user)

        pdfmetrics.registerFont(
            TTFont(
                'OS', '/code/static/OpenSans-Regular.ttf'
                )
            )

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="To_buy.pdf"'

        p = canvas.Canvas(response)

        p.setFont('OS', 16)

        pos_x = 50
        pos_y = 700

        p.drawString(50, 800, f'Ваш список покупок, {request.user.first_name}')

        ings_added = {}

        for recipe in object_list:
            for obj in recipe.get_amount.all():
                if obj.ingredient.name in ings_added:
                    ings_added[obj.ingredient.name][0] += obj.amount
                else:
                    name = obj.ingredient.name
                    amount = obj.amount
                    measurement = obj.ingredient.measurement

                    ings_added.update(
                        {name: [amount, measurement]}
                    )

        for obj in ings_added:

            p.drawString(
                pos_x, pos_y,
                f'{obj} ({ings_added[obj][1]}) - {ings_added[obj][0]}'
            )
            pos_y -= 25

        p.showPage()
        p.save()
        return response


class Subscriptions(CustomListView):

    model = User
    templates = {'any': 'subscription.html'}

    def get(self, request):

        queryset = self.model.objects.filter(followed__user=request.user)

        object_list = self.paginate_it(queryset, 5)

        context = {'object_list': object_list}

        return render(request, self.get_template(), context)

    def post(self, request):

        request_data = json.loads(request.body)

        author = get_object_or_404(User, id=request_data['id'])

        if author != request.user:
            obj, created = ShoppingList.objects.get_or_create(
                user=request.user,
                recipe=author
            )
            if not created:
                obj.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class DeleteRecipe(DeleteView):

    model = Recipe
    success_url = reverse_lazy('index')
