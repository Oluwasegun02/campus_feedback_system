from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.list_feedback, name='list_feedback'),
    path('feedback/<int:feedback_id>/', views.view_feedback, name='view_feedback'),
    path('feedbacks/', views.submit_feedback, name='submit_feedback'),
    path('analytics/', views.feedback_analytics, name='feedback_analytics'),
]
