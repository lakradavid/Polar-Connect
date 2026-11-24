from django.urls import path
from . import views
app_name = 'media_gallery'
urlpatterns = [
    path('',           views.gallery,       name='gallery'),
    path('<int:pk>/',  views.media_detail,  name='detail'),
    path('upload/',    views.media_upload,  name='upload'),
]
