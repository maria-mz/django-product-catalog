from django import forms
from .models import Category

class ProductFilterForm(forms.Form):
    query = forms.CharField(
        required=False,
        strip=True,
        widget=forms.TextInput(attrs={"placeholder": "Share descriptions..."}),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="All",
        required=False,
    )
