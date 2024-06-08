from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'account'


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('login/success/', views.success_login, name='success_login'),
    path('login/invalid/', views.invalid_login, name='invalid_login'),
    path('login/block/', views.block_login, name='block_login'),
]