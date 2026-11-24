from django.urls import path
from . import views
app_name = 'research'
urlpatterns = [
    path('',           views.research_list,   name='list'),
    path('<int:pk>/',  views.research_detail, name='detail'),
    path('upload/',    views.research_upload, name='upload'),
    path('<int:pk>/approve/', views.approve_paper, name='approve'),
]
