from django import forms

from .models import Product, Review

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['author', 'product', 'created_at', 'updated_at', 'check_moderated']