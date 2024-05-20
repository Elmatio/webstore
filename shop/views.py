from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import AddProductForm
from .recommender import Recommender
from django.views.generic import ListView
from django.db.models import Q
from .filters import *


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
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    # Фильтры по цвету, производителю, материалу, длине, ширине и высоте
    colors = request.GET.getlist('color[]')
    products_colors = []
    if colors:
        print(1)
        for i in products:
            for j in colors:
                if j.lower() in i.description.lower():
                    products_colors.append(i.name)
        products = products.filter(name__in=products_colors)

    manufacturers = request.GET.getlist('manufacturer[]')
    products_manufacturers = []
    if manufacturers:
        for i in products:
            for j in manufacturers:
                if j in i.description:
                    products_manufacturers.append(i.name)
        products = products.filter(name__in=products_manufacturers)

    materials = request.GET.getlist('material[]')
    products_materials = []
    if materials:
        for i in products:
            for j in materials:
                if j in i.description:
                    products_materials.append(i.name)
        products = products.filter(name__in=products_materials)

    lengths = request.GET.getlist('length[]')
    products_lengths = []
    if lengths:
        for i in products:
            for j in lengths:
                if "Длина (см): " + j in i.description:
                    products_lengths.append(i.name)
        products = products.filter(name__in=products_lengths)

    widths = request.GET.getlist('width[]')
    products_widths = []
    if widths:
        for i in products:
            for j in widths:
                if "Ширина (см): " + j in i.description:
                    products_widths.append(i.name)
        products = products.filter(name__in=products_widths)

    heights = request.GET.getlist('height[]')
    products_heights = []
    if heights:
        for i in products:
            for j in heights:
                if "Высота (см): " + j in i.description:
                    products_heights.append(i.name)
        products = products.filter(name__in=products_heights)

    context = {
        'category': category,
        'categories': categories,
        'filter': products,
        'colors': colors_list,
        'manufacturers': manufacturers_list,
        'materials': materials_list,
        'lengths': lengths_list,
        'widths': widths_list,
        'heights': heights_list,
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