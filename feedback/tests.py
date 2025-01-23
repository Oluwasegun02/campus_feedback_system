from django.test import TestCase, Client
from django.urls import reverse
from feedback.models import Feedback, FeedbackCategory, FeedbackComment
from django.contrib.auth.models import User

class FeedbackSystemTests(TestCase):
    def setUp(self):
        # Create test data
        self.client = Client()
        self.category = FeedbackCategory.objects.create(name="Facilities")
        self.user = User.objects.create_user(username="testuser", password="password")
        self.feedback = Feedback.objects.create(
            title="Test Feedback",
            description="Test description",
            category=self.category,
            rating=4,
            user=self.user
        )
        self.comment_url = reverse("view_feedback", args=[self.feedback.id])

    def test_feedback_submission(self):
        # Test feedback submission form
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse("submit_feedback"), {
            "title": "New Feedback",
            "description": "New feedback description",
            "category": self.category.id,
            "rating": 5
        })
        self.assertEqual(response.status_code, 302)  # Redirect after submission
        self.assertEqual(Feedback.objects.count(), 2)  # One feedback added

    def test_feedback_filtering(self):
        # Test filtering feedback by category
        response = self.client.get(reverse("list_feedback") + f"?category={self.category.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Feedback")

    def test_comment_submission(self):
        # Test comment submission on feedback
        self.client.login(username="testuser", password="password")
        response = self.client.post(self.comment_url, {
            "comment": "This is a test comment."
        })
        self.assertEqual(response.status_code, 302)  # Redirect after submission
        self.assertEqual(FeedbackComment.objects.count(), 1)

    def test_form_validation(self):
        # Test form validation for empty fields
        self.client.login(username="testuser", password="password")
        response = self.client.post(reverse("submit_feedback"), {
            "title": "",
            "description": "",
            "category": self.category.id,
            "rating": ""
        })
        self.assertEqual(response.status_code, 200)  # Form re-renders on error
        self.assertContains(response, "This field is required.")

    def test_caching_behavior(self):
        # Test caching of feedback listing
        response_1 = self.client.get(reverse("list_feedback"))
        response_2 = self.client.get(reverse("list_feedback"))
        self.assertEqual(response_1.content, response_2.content)  # Cached response

    def test_page_load_times(self):
        # Verify page load times (basic performance check)
        response = self.client.get(reverse("list_feedback"))
        self.assertLess(response.elapsed.total_seconds(), 1, "Page load time is too high!")
