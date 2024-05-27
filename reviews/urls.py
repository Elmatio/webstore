from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('<int:id>/reviews/', views.review_add,
         name='reviews')
]
