from django.urls import path
from . import views
app_name = 'community'
urlpatterns = [
    path('',                           views.forum_home,       name='forum'),
    path('forum/<slug:slug>/',         views.forum_detail,     name='forum_detail'),
    path('discussion/<int:pk>/',       views.discussion_detail,name='discussion'),
    path('discussion/new/',            views.new_discussion,   name='new_discussion'),
]
