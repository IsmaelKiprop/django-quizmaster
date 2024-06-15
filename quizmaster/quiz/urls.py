# quiz/urls.py

from django.urls import path
from .views import signup, login_view, logout_view, quiz_list, quiz_detail, submit_quiz, quiz_results, dashboard, create_quiz, update_quiz, create_question, create_choice, update_question, update_choice, delete_question, delete_choice, delete_quiz

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', quiz_list, name='quiz_list'),
    path('quiz/<int:pk>/', quiz_detail, name='quiz_detail'),
    path('quiz/<int:pk>/submit/', submit_quiz, name='submit_quiz'),
    path('quiz/<int:pk>/results/', quiz_results, name='quiz_results'),
    path('dashboard/', dashboard, name='dashboard'),
    path('quiz/create/', create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_pk>/update/', update_quiz, name='update_quiz'),
    path('quiz/<int:quiz_pk>/create_question/', create_question, name='create_question'),
    path('question/<int:question_pk>/create_choice/', create_choice, name='create_choice'),
    path('question/<int:question_pk>/update/', update_question, name='update_question'),
    path('choice/<int:choice_pk>/update/', update_choice, name='update_choice'),
    path('question/<int:question_pk>/delete/', delete_question, name='delete_question'),
    path('choice/<int:choice_pk>/delete/', delete_choice, name='delete_choice'),
    path('quiz/<int:quiz_pk>/delete/', delete_quiz, name='delete_quiz'),
]
