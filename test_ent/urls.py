from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('home',views.home, name='home'),
    path('db',views.db, name='db'),
    path('add',views.add, name='add'),
    path('search_complete',views.search_complete, name='search_complete'),
    path('insert_complete',views.insert_complete, name='insert_complete'),
    path('update_complete',views.update_complete, name='update_complete'),
    path('about',views.about, name='about'),
    path('products',views.products, name='products'),
    path('contact',views.contact, name='contact'),
]