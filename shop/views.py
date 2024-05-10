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
    products = Product.objects.filter(available=True)
    slugs = [categories[i].slug for i in range(len(categories))]
    search_query = request.GET.get('search_field', None)
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__iregex=search_query))
    if category_slug in slugs:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)
    product_filter = ProductFilter(request.GET, queryset=products)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'filter': product_filter})


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
