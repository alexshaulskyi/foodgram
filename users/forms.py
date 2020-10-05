from django import forms

from django.contrib.auth.password_validation import validate_password

from users.models import User


class SignUpForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[validate_password]
        )

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password')
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'type': 'text',
                    'name': 'first_name',
                    'id': 'id_first_name',
                    'class': 'form__input'
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'type': 'text',
                    'name': 'username',
                    'id': 'id_username',
                    'class': 'form__input',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'type': 'email',
                    'name': 'email',
                    'id': 'id_email',
                    'class': 'form__input'
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'type': 'password',
                    'name': 'password',
                    'id': 'id_password',
                    'class': 'form__input'
                }
            )
        }
