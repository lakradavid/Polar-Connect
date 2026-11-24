from django.urls import path
from . import views
app_name = 'repository'
urlpatterns = [
    path('',           views.resource_list,   name='list'),
    path('<int:pk>/',  views.resource_detail, name='detail'),
    path('upload/',    views.resource_upload, name='upload'),
]
