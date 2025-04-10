from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm, QuestionForm, AnswerForm
from .models import Question, Answer, AnswerLike

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserSignupForm()
        return render(request, 'signup.html', {'form': form})
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')



def home_view(request):
    questions = Question.objects.all().order_by('-created_at')
    print(questions)
    return render(request, 'home.html', {'questions': questions})


def create_question_view(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()
        return render(request, 'create_question.html', {'form': form})
        

def question_detail_view(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    answer_data = []
    for answer in answers:
        like_count = answer.like.count()
        is_liked = False
        if request.user.is_authenticated:
            is_liked = AnswerLike.objects.filter(answer=answer, user=request.user).exists()
        answer_data.append({'instance': answer, 'like_count': like_count, 'is_liked': is_liked})


    form = AnswerForm()
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = AnswerForm()
        return render(request, 'question_detail.html', {'question': question, 'answer_data': answer_data, 'form': form})
    

def like_answer_view(request, pk):
    answer = get_object_or_404(Answer, pk=pk)

    if request.method == 'POST':
        AnswerLike.objects.get_or_create(answer=answer, user=request.user)

    return redirect('question_detail', pk=answer.question.pk)


