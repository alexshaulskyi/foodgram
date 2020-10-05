from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import SignUpForm


class SignUp(CreateView):

    template_name = 'reg.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):

        raw_password = form.instance.password
        form.instance.set_password(raw_password)

        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):

        username = self.request.POST.get('username', '')
        first_name = self.request.POST.get('first_name', '')
        email = self.request.POST.get('email', '')

        context = self.get_context_data(**kwargs)
        context.update(
            {
                'form': form,
                'first_name': first_name,
                'username': username,
                'email': email
            }
        )

        return self.render_to_response(context)
