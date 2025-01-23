from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import FeedbackForm, FeedbackCommentForm
from .models import Feedback, FeedbackComment, FeedbackCategory
from django.db.models import Count, Avg
from django.core.cache import cache


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'feedback/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('submit_feedback')
    else:
        form = AuthenticationForm()
    return render(request, 'feedback/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib import messages

@login_required(login_url='login')
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Your feedback has been submitted successfully!')
            return redirect('submit_feedback')
        else:
            return redirect('list_feedback')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/submit_feedback.html', {'form': form})

@login_required(login_url='login')
def view_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    comments = feedback.comments.all()

    if request.method == 'POST':
        form = FeedbackCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.feedback = feedback
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('view_feedback', feedback_id=feedback.id)
        
    else:
        form = FeedbackCommentForm()

    return render(request, 'feedback/view_feedback.html', {
        'feedback': feedback,
        'comments': comments,
        'form': form
    })


def list_feedback(request):
    category_id = request.GET.get('category')
    cache_key = f'feedback_list_{category_id or "all"}'
    feedbacks = cache.get(cache_key)

    if not feedbacks:
        if category_id:
            feedbacks = Feedback.objects.filter(category_id=category_id)
        else:
            feedbacks = Feedback.objects.all()
            
        cache.set(cache_key, feedbacks, timeout=300)  # Cache for 5 minutes
            
    
    categories = FeedbackCategory.objects.all()
    return render(request, 'feedback/list_feedback.html', {
        'feedbacks': feedbacks,
        'categories': categories
    })

@login_required(login_url='login')
def feedback_analytics(request):
    categories = FeedbackCategory.objects.annotate(
        total_feedback=Count('feedback'),
        avg_rating=Avg('feedback__rating')
    )

    return render(request, 'feedback/analytics.html', {'categories': categories})

