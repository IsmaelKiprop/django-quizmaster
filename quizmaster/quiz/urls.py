from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:pk>/submit/', views.submit_quiz, name='submit_quiz'),
    path('results/<int:pk>/', views.quiz_results, name='quiz_results'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/create_quiz/', views.create_quiz, name='create_quiz'),
]
