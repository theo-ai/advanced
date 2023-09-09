from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('db/', views.db, name='db'),
    path('search_client/', views.search_client, name='search_client'),
    #there is no need for that
    #path('search_complete/', views.search_complete, name='search_complete'),
    path('display_client/<int:client_id>/', views.display_client, name='display_client'),
    path('insert_client/', views.insert_client, name='insert_client'),
    #there is no need for that
    #path('insert_complete/', views.insert_complete, name='insert_complete'),
    path('update_client/<int:client_id>/', views.update_client, name='update_client'),
    path('update_client_complete/<int:client_id>/', views.update_client_complete, name='update_client_complete'),
    path('search_calendar/', views.search_calendar, name='search_calendar'),
    path('display_calendar/<int:calendar_id>/', views.display_calendar, name='display_calendar'),
    path('insert_calendar/<int:client_id>/', views.insert_calendar, name='insert_calendar'),
    path('insert_calendar_complete/<int:client_id>/', views.insert_calendar_complete, name='insert_calendar_complete'),
    path('update_calendar/<int:calendar_id>/', views.update_calendar, name='update_calendar'),
    path('update_calendar_complete/<int:calendar_id>/', views.update_calendar_complete, name='update_calendar_complete'),
]
