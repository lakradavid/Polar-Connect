from django.urls import path
from . import views
app_name = 'news'
urlpatterns = [
    path('',                    views.news_list,      name='list'),
    path('article/<slug:slug>/',views.news_detail,    name='detail'),
    path('events/',             views.events_list,    name='events'),
    path('events/<slug:slug>/', views.event_detail,   name='event_detail'),
    path('create/',             views.news_create,    name='create'),
]
