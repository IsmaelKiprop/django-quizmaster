# quiz/views.py
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LoginForm, QuizForm, QuestionForm, ChoiceForm
from .models import Quiz, Question, Choice, Submission, User

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('quiz_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {user.username}!')
                return redirect('quiz_list')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

@login_required
def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz, 'questions': questions})


@login_required
def create_quiz(request):
    if not request.user.is_admin:
        return redirect('quiz_list')

    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.creator = request.user
            quiz.save()
            return redirect('dashboard')
    else:
        form = QuizForm()
    
    return render(request, 'quizzes/create_quiz.html', {'form': form})

@login_required
def update_quiz(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, creator=request.user)
    
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = QuizForm(instance=quiz)
    
    return render(request, 'quizzes/update_quiz.html', {'form': form, 'quiz': quiz})

@login_required
def create_question(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, creator=request.user)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('create_choice', question_pk=question.pk)
    else:
        form = QuestionForm()
    
    return render(request, 'quizzes/create_question.html', {'form': form, 'quiz': quiz})

@login_required
def create_choice(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk, quiz__creator=request.user)
    
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('create_choice', question_pk=question.pk)
    else:
        form = ChoiceForm()
    
    return render(request, 'quizzes/create_choice.html', {'form': form, 'question': question})

@login_required
def update_question(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk, quiz__creator=request.user)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('create_choice', question_pk=question.pk)
    else:
        form = QuestionForm(instance=question)
    
    return render(request, 'quizzes/update_question.html', {'form': form, 'question': question})

@login_required
def update_choice(request, choice_pk):
    choice = get_object_or_404(Choice, pk=choice_pk, question__quiz__creator=request.user)
    
    if request.method == 'POST':
        form = ChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            return redirect('create_choice', question_pk=choice.question.pk)
    else:
        form = ChoiceForm(instance=choice)
    
    return render(request, 'quizzes/update_choice.html', {'form': form, 'choice': choice})

@login_required
def delete_question(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk, quiz__creator=request.user)
    
    if request.method == 'POST':
        question.delete()
        return redirect('dashboard')
    
    return render(request, 'quizzes/delete_question_confirm.html', {'question': question})

@login_required
def delete_choice(request, choice_pk):
    choice = get_object_or_404(Choice, pk=choice_pk, question__quiz__creator=request.user)
    
    if request.method == 'POST':
        choice.delete()
        return redirect('create_choice', question_pk=choice.question.pk)
    
    return render(request, 'quizzes/delete_choice_confirm.html', {'choice': choice})

@login_required
def delete_quiz(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, creator=request.user)
    
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Quiz deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'quizzes/delete_quiz_confirm.html', {'quiz': quiz})

@login_required
def submit_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = Question.objects.filter(quiz=quiz)
    
    if request.method == 'POST':
        if not questions.exists():
            messages.error(request, "This quiz has no questions.")
            return redirect('quiz_detail', pk=quiz.pk)
        
        score = 0
        time_taken = int(request.POST.get('time_taken'))
        feedback = []

        for question in questions:
            choice_id = request.POST.get(str(question.id))
            if choice_id:
                choice = Choice.objects.get(id=choice_id)
                if choice.is_correct:
                    score += 1
                    feedback.append(f"Question: {question.text} - Correct!")
                else:
                    correct_choice = question.choices.get(is_correct=True)
                    feedback.append(f"Question: {question.text} - Incorrect. Correct answer: {correct_choice.text}")

        score_percentage = int((score / len(questions)) * 100)
        submission = Submission(user=request.user, quiz=quiz, score=score_percentage, time_taken=time_taken)
        submission.save()

        return render(request, 'quizzes/quiz_results.html', {'submission': submission, 'feedback': feedback})

    return render(request, 'quizzes/submit_quiz.html', {'quiz': quiz, 'questions': questions, 'time_limit': quiz.time_limit * 60})


@login_required
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
        print(request.POST)  # Print POST data for debugging
        title = request.POST.get('title')
        description = request.POST.get('description')
        time_limit = request.POST.get('time_limit')
        
        if title and description and time_limit:
            try:
                time_limit = int(time_limit)
                quiz = Quiz(title=title, description=description, time_limit=time_limit, creator=request.user)
                quiz.save()
                return redirect('dashboard')
            except ValueError:
                # Handle the case where time_limit is not an integer
                pass

    return render(request, 'quizzes/create_quiz.html')
