from django import forms
from django.core.exceptions import ValidationError

from .models import Product, Review

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['author', 'product', 'created_at', 'updated_at', 'check_moderated']

    def clean_grade(self):
        print(self.cleaned_data.get('grade'))
        if self.cleaned_data.get('grade') < 1 or self.cleaned_data.get('grade') > 5:
            raise ValidationError(f'Нужно ввести оценку в диапазоне от 1 до 5')
        return self.cleaned_data.get('grade')

class ReviewCheckForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = []
        labels = {'check_moderated': 'Модерирование'}