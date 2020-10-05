from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View

from recipes.models import Tag


class CustomListView(View):

    model = None
    templates = {}

    def get_template(self):
        any_template = self.templates.get('any')
        if any_template is not None:
            return any_template
        if self.request.user.is_authenticated:
            return self.templates['auth']
        return self.templates['anonymous']

    def get_tags(self):
        return Tag.objects.all()

    def paginate_it(self, queryset, quantity):
        paginator = Paginator(queryset, quantity)

        page = self.request.GET.get('page')

        try:
            object_list = paginator.get_page(page)
        except (PageNotAnInteger, EmptyPage):
            object_list = paginator.get_page(1)
        return object_list

    def get_filters(self):

        return self.request.GET.getlist('filters')


def get_ings_amount(request_object):

    ingredients = [
        request_object.POST.get(name)
        for name in request_object.POST.keys()
        if 'nameIngredient' in name
    ]
    amount = [
        request_object.POST.get(name)
        for name in request_object.POST.keys()
        if 'valueIngredient' in name
    ]

    return dict(zip(ingredients, amount))
