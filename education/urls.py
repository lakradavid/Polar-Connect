from django.urls import path
from . import views
app_name = 'education'
urlpatterns = [
    path('',                           views.modules_list,    name='modules'),
    path('category/<slug:slug>/',      views.category_detail, name='category'),
    path('module/<slug:slug>/',        views.module_detail,   name='module'),
    path('quizzes/',                   views.quiz_list,       name='quizzes'),
    path('quiz/<int:pk>/',             views.quiz_take,       name='quiz_take'),
    path('quiz/<int:pk>/result/',      views.quiz_result,     name='quiz_result'),
]
