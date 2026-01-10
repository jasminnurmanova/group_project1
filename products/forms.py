from django import forms
from .models import Product


class NewProductForm(forms.ModelForm):
    images = forms.FileField(required=False)

    class Meta:
        model = Product
        fields = (
            'title',
            'description',
            'price',
            'category',
        )

    def save (self, request, commit=True):
        product = self.instance
        product.author = request.user
        super().save(commit)
        return product


class ProductForm(forms.ModelForm):
    images = forms.FileField(required=False)

    class Meta:
        model = Product
        fields = (
            'title',
            'description',
            'price',
            'category',
        )