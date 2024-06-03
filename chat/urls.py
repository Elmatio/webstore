from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('message/<int:id>/', views.message, name='message'),
    path('chat/', views.chat_list, name='chat_list'),
    path('chat_detail/<int:id>/', views.chat_detail, name='chat_detail'),
]