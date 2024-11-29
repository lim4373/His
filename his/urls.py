from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('doctor/', views.doctor, name='doctor'),
    path('search-images/', views.search_images, name='search_images'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
]
