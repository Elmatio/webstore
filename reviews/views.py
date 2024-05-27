from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from reviews.forms import CommentForm
from reviews.models import Review
from shop.models import Product


# Create your views here.
@login_required
def review_add(request, id):
    review = []
    print(id)
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        text = request.POST.get('text')
        review, created = Review.objects.get_or_create(user=request.user,
                                              product=product,
                                              text=text)

        print(review)
        review.save()
    return redirect('shop:product_detail', product.id, product.slug)
