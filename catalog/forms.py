from django import forms
from .models import Category, Tag

class ProductFilterForm(forms.Form):
    """
    Search & Filter inputs for the /products page.
    """
    query = forms.CharField(
        required=False,
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
