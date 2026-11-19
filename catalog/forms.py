from django import forms
from .models import Category, Tag

class ProductFilterForm(forms.Form):
    query = forms.CharField(
        required=False,
        strip=True,
        widget=forms.TextInput(attrs={"placeholder": "Search descriptions..."}),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="All",
        required=False,
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
