from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FeedbackCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(FeedbackCategory, on_delete=models.CASCADE, db_index=True)
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name}"
        # return self.title

class FeedbackComment(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.feedback.title} : {self.comment[:20]}..."
