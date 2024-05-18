from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import AddProductForm
from .recommender import Recommender
from django.views.generic import ListView
from django.db.models import Q
from .filters import ProductFilter


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Фильтр по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    context = {
        'category': category,
        'categories': categories,
        'filter': products,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'shop/product/list_partial.html', context)

    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product = AddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product': cart_product,
                   'recommended_products': recommended_products})