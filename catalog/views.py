from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import Product
from .forms import ProductFilterForm


def products_view(request: HttpRequest) -> HttpResponse:
    """
    Display the catalog's products, handling searching and filtering.
    """
    form = ProductFilterForm(request.GET)

    # Preload category and tags in memory to avoid N+1 queries when rendering
    # product lines
    products = Product.objects.select_related("category").prefetch_related("tags")

    if form.is_valid():
        query = form.cleaned_data['query']
        category = form.cleaned_data['category']
        tags = form.cleaned_data['tags']

        if query:
            products = products.filter(description__icontains=query)
        if category:
            products = products.filter(category=category)
        for tag in tags:
            products = products.filter(tags=tag)

    context = {
        'products': products,
        'form': form
    }
    return render(request, 'catalog/products.html', context)
