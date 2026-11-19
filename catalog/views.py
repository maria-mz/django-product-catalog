from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import Product
from .forms import ProductFilterForm

def products_view(request: HttpRequest) -> HttpResponse:
    form = ProductFilterForm(request.GET)

    products = Product.objects.all()

    if form.is_valid():
        query = form.cleaned_data["query"]
        category = form.cleaned_data['category']

        if query:
            products = products.filter(description__icontains=query)
        if category:
            products = products.filter(category=category)

    context = {
        'products': products,
        'form': form
    }
    return render(request, 'catalog/products.html', context)
