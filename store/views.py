from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product, Category, Wishlist

def product_list(request):
    query = request.GET.get('q')
    category_slug = request.GET.get('category')
    
    products = Product.objects.all()
    categories = Category.objects.all()

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'store/list.html', {
        'products': products,
        'categories': categories,
        'query': query
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', {'product': product})

