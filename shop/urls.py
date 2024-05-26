from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list,
         name='product_list'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
    path('about/', views.product_list,
         name='about'),
    path('contacts/', views.product_list,
         name='contacts'),
    path('delivery/', views.product_list,
         name='delivery'),
    path('installment/', views.product_list,
         name='installment'),
]
