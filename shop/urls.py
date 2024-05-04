from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
    # path('login/', LoginView.as_view(),
    #      name='login'),
    # path('logout/', LogoutView.as_view(),
    #      name='logout'),
]