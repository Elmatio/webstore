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

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.filter(available=True)
    slugs = [categories[i].slug for i in range(len(categories))]
    search_query = request.GET.get('search_field', None)
    if category_slug in slugs:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)
    if search_query:
       products = products.filter(Q(name__icontains=search_query) |
                                  Q(description__iregex=search_query))

    if min_price:
        products = products.filter(price__gt=min_price)
        print(products, min_price)
    if max_price:
        products = products.filter(price__lt=max_price)
    product_filter = ProductFilter(request.GET, queryset=products)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'filter': products})



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