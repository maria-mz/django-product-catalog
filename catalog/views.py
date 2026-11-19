from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import Product

def products_view(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('q', '').strip()

    products = Product.objects.all()
    if query:
        products = products.filter(description__icontains=query)

    context = {
        'products': products,
        'search_query': query
    }
    return render(request, 'catalog/products.html', context)
