
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('loguot/', views.logout_view, name='logout'),
    path('question/create/', views.create_question_view, name='create_question'),
    path('question/<int:pk>/', views.question_detail_view, name='question_detail'),
    path('answer/<int:pk>/like/', views.like_answer_view, name='like_answer')
]
