import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse

# Create your tests here.

def create_question(question_text, days):
    """
    create a question with the pub_time = (now + days)
    positive for future, negative for past time
    """
    now = timezone.now()
    return Question.objects.create(question_text=question_text, pub_time=now+datetime.timedelta(days=days))

class QuestionModelTests(TestCase):
    def test_was_published_today_with_future_time(self):
        """
        was_published_today_function whose pub_time is future time 
        should return False
        """
        future_time = timezone.now() + datetime.timedelta(days=30)
        question_future = Question(pub_time=future_time)
        self.assertIs(question_future.was_published_today(), False)

    def test_was_published_today_with_old_time(self):
        old_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        question_old = Question(pub_time=old_time)
        self.assertIs(question_old.was_published_today(), False)

    def test_was_published_today_with_today(self):
        recent_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        question_today= Question(pub_time=recent_time)
        self.assertIs(question_today.was_published_today(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        response =  self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context["question_latest"], [])

    def test_past_question(self):
        question = create_question("past question", days=-30)
        response =  self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["question_latest"], [question])

    def test_future_question(self):
        create_question("future question", days=30)
        response =  self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context["question_latest"], [])

    def test_past_future_question(self):
        question = create_question("past question", days=-30)
        create_question("future question", days=30)
        response =  self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["question_latest"], [question])

    def test_two_past_question(self):
        question1 = create_question("past question1", days=-30)
        question2 = create_question("past question2", days=-5)
        response =  self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["question_latest"], [question2, question1])

class QuestionDetailViewTests(TestCase):
    def test_past_question(self):
        question = create_question(question_text="Past question", days=-5)
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)

    def test_future_question(self):
        question = create_question(question_text="future question", days=5)
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

