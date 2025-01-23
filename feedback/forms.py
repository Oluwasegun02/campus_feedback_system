from django import forms
from .models import Feedback
from .models import FeedbackComment

class FeedbackCommentForm(forms.ModelForm):
    class Meta:
        model = FeedbackComment
        fields = ['comment']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['title', 'description', 'category', 'rating']
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #         'class': 'w-full border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-300',
        #         'placeholder': 'Enter your feedback title',
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': 'w-full border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-300',
        #         'placeholder': 'Describe your feedback...',
        #         'rows': 4,
        #     }),
        #     'category': forms.Select(attrs={
        #         'class': 'w-full border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-300',
        #     }),
        #     'rating': forms.NumberInput(attrs={
        #         'class': 'w-full border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-300',
        #         'placeholder': 'Rate from 1 to 5',
        #     }),
        # }


