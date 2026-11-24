from django.urls import path
from . import views
app_name = 'stations'
urlpatterns = [
    path('',          views.stations_list, name='list'),
    path('map/',      views.polar_map,     name='map'),
    path('<slug:slug>/', views.station_detail, name='detail'),
]
