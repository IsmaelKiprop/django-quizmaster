from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .models import Quiz, Question, Answer

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('quiz_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        questions = quiz.question_set.all()
        score = 0
        for question in questions:
            selected_answer = request.POST.get(str(question.id))
            if selected_answer:
                selected_answer = int(selected_answer)
                correct_answer = question.answer_set.filter(is_correct=True).first()
                if selected_answer == correct_answer.id:
                    score += 1
        return render(request, 'quiz_result.html', {'quiz': quiz, 'score': score})
    return render(request, 'quiz_detail.html', {'quiz': quiz})