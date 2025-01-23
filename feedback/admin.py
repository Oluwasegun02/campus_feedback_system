from django.contrib import admin
from .models import Feedback, FeedbackCategory, FeedbackComment

@admin.register(FeedbackCategory)
class FeedbackCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'rating', 'submitted_at')
    search_fields = ('title', 'user__username', 'category__name')
    list_filter = ('category', 'rating')

@admin.register(FeedbackComment)
class FeedbackCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'feedback', 'user', 'comment', 'commented_at')
    search_fields = ('feedback__title', 'user__username', 'comment')
    list_filter = ('commented_at',)
