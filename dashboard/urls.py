from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('',               views.dashboard_index,  name='index'),
    path('admin/',         views.admin_dashboard,  name='admin'),
    path('notifications/', views.notifications,    name='notifications'),
    path('bookmarks/',     views.bookmarks,         name='bookmarks'),
]
