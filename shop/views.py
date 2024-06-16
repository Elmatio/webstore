from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from account.models import CustomUser
from chat.models import Message
from reviews.models import Review
from .models import Category, Product
from cart.forms import AddProductForm
from .recommender import Recommender
from django.views.generic import ListView
from django.db.models import Q
from .filters import *
from django.core.paginator import Paginator


def product_list(request, category_slug=None):
    category = None
    category_main = None
    categories = Category.objects.all()
    products = Product.objects.all()
    page_obj = None

    if category_slug == 'about':
        return render(request, 'shop/navigation/about.html')
    elif category_slug == 'contacts':
        return render(request, 'shop/navigation/contacts.html')
    elif category_slug == 'delivery':
        return render(request, 'shop/navigation/delivery.html')
    elif category_slug == 'installment':
        return render(request, 'shop/navigation/installment.html')
    elif category_slug == 'add_product':
        return render(request,
                      'shop/navigation/add_product.html',
                      {'categories': categories})
    elif category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        category_main = Category.objects.filter(main=category.main)
        products = products.filter(category=category)


    # Фильтр по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    # Фильтры по цвету, производителю, материалу, длине, ширине и высоте
    colors = request.GET.getlist('color[]')
    if colors:
        products = products.filter(description__icontains='|'.join(colors))

    manufacturers = request.GET.getlist('manufacturer[]')
    if manufacturers:
        products = products.filter(description__icontains='|'.join(manufacturers))

    materials = request.GET.getlist('material[]')
    if materials:
        products = products.filter(description__icontains='|'.join(materials))

    lengths = request.GET.getlist('length[]')
    if lengths:
        products = products.filter(description__icontains='|'.join(["Длина (см): " + length for length in lengths]))

    widths = request.GET.getlist('width[]')
    if widths:
        products = products.filter(description__icontains='|'.join(["Ширина (см): " + width for width in widths]))

    heights = request.GET.getlist('height[]')
    if heights:
        products = products.filter(description__icontains='|'.join(["Высота (см): " + height for height in heights]))

    search = request.GET.get('search_field')
    if search:
        products = products.filter(name__iregex=search)

    offset = int(request.GET.get('offset', 0))
    limit = 20  # Количество товаров для подгрузки за один раз
    products = products[offset:offset + limit]

    messages = []
    message = []
    if request.user.is_authenticated:
        user = request.user
        messages_user = Message.objects.filter(user__id=user.id)
        admin = CustomUser.objects.get(username='ahmat')
        messages_admin = Message.objects.filter(user=admin, user_to=user)
        message = admin
        messages = sorted(list(messages_user) + list(messages_admin), key=lambda x: (x.date, x.time))

    category_furniture = Category.objects.filter(main='Мебель')
    category_tile = Category.objects.filter(main='Плитка керамическая')
    category_flooring = Category.objects.filter(main='Напольные покрытия')
    category_wallpaper = Category.objects.filter(main='Обои')
    category_interior = Category.objects.filter(main='Интерьер')
    category_plumbing = Category.objects.filter(main='Сантехника')
    category_paintwork = Category.objects.filter(main='Лакокраска')
    category_instrument = Category.objects.filter(main='Инструмент')
    category_coverings = Category.objects.filter(main='Настенные покрытия')
    category_lumber = Category.objects.filter(main='Пиломатериалы, столярные изделия')
    category_lamps = Category.objects.filter(main='Светильники')
    category_build = Category.objects.filter(main='Строительные материалы')
    category_mixes = Category.objects.filter(main='Сухие смеси')
    category_doors = Category.objects.filter(main='Двери')
    category_electrical = Category.objects.filter(main='Электротовары')

    if category:
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page', 1)
        products = paginator.page(page_number)
        page_obj = paginator.get_page(page_number)


    reviews = Review.objects.all()
    context = {
        'category_main': category_main,
        'category_furniture': category_furniture,
        'category_tile': category_tile,
        'category_flooring': category_flooring,
        'category_wallpaper': category_wallpaper,
        'category_interior': category_interior,
        'category_plumbing': category_plumbing,
        'category_paintwork': category_paintwork,
        'category_instrument': category_instrument,
        'category_coverings': category_coverings,
        'category_lumber': category_lumber,
        'category_lamps': category_lamps,
        'category_build': category_build,
        'category_mixes': category_mixes,
        'category_doors': category_doors,
        'category_electrical': category_electrical,
        'category': category,
        'categories': categories,
        'filter': products,
        'colors': colors_list,
        'manufacturers': manufacturers_list,
        'materials': materials_list,
        'lengths': lengths_list,
        'widths': widths_list,
        'heights': heights_list,
        'messages': messages,
        'message': message,
        'reviews': reviews,
        'page_obj': page_obj,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'shop/product/list_partial.html', context)

    return render(request, 'shop/product/list.html', context)


def load_more_products(request):
    offset = int(request.GET.get('offset', 0))
    limit = 20  # Количество товаров для подгрузки за один раз
    products = Product.objects.all()[offset:offset + limit]
    data = [{'id': product.id, 'name': product.name, 'price': product.price, 'discount': product.discount, 'image': product.image.url if product.image else '', 'rating': product.rating} for product in products]
    return JsonResponse(data, safe=False)


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product = AddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    reviews = Review.objects.filter(product__id=id)
    if reviews.exists():
        marks = reviews.values('mark')
        mark = sum([i['mark'] for i in marks]) // marks.count() * '★'
    else:
        mark = 'Нет отзывов'
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product': cart_product,
                   'recommended_products': recommended_products,
                   'reviews': reviews,
                   'mark': mark})
