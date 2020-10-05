from django import forms

from recipes.models import Recipe


class CreateRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'image', 'description', 'cooking_time', 'tags')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'type': 'text',
                    'id': 'id_name',
                    'name': 'name',
                    'class': 'form__input'
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'type': 'file',
                    'id': 'id_file',
                    'name': 'file',
                    'class': 'form__file'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'name': 'description',
                    'id': 'id_description',
                    'rows': 8,
                    'class': 'form__textarea'
                }
            ),
            'cooking_time': forms.TextInput(
                attrs={
                    'type': 'text',
                    'name': 'time',
                    'id': 'id_time',
                    'class': 'form__input'
                }
            ),
            'tags': forms.CheckboxSelectMultiple()
        }
