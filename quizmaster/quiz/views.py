from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Quiz, Question, Choice, Submission, User
from django.utils import timezone
import json

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('quiz_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('quiz_list')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz, 'questions': questions})

@login_required
def submit_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = Question.objects.filter(quiz=quiz)
    if request.method == 'POST':
        score = 0
        time_taken = int(request.POST.get('time_taken'))
        for question in questions:
            choice_id = request.POST.get(str(question.id))
            choice = Choice.objects.get(id=choice_id)
            if choice.is_correct:
                score += 1
        submission = Submission(user=request.user, quiz=quiz, score=score, time_taken=time_taken)
        submission.save()
        return redirect('quiz_results', pk=submission.id)
    return render(request, 'quizzes/submit_quiz.html', {'quiz': quiz, 'questions': questions, 'time_limit': quiz.time_limit * 60})

def quiz_results(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    return render(request, 'quizzes/quiz_results.html', {'submission': submission})

@login_required
def dashboard(request):
    if not request.user.is_admin:
        return redirect('quiz_list')
    
    quizzes = Quiz.objects.filter(creator=request.user)
    submissions = Submission.objects.filter(quiz__in=quizzes)
    
    context = {
        'quizzes': quizzes,
        'submissions': submissions,
    }
    return render(request, 'quizzes/dashboard.html', context)

@login_required
def create_quiz(request):
    if not request.user.is_admin:
        return redirect('quiz_list')

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        time_limit = int(request.POST['time_limit'])
        quiz = Quiz(title=title, description=description, time_limit=time_limit, creator=request.user)
        quiz.save()
        return redirect('dashboard')
    return render(request, 'quizzes/create_quiz.html')
