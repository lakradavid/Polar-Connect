from django.urls import path
from . import views
app_name = 'expeditions'
urlpatterns = [
    path('',               views.expedition_list,   name='list'),
    path('<slug:slug>/',   views.expedition_detail, name='detail'),
]
