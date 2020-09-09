import datetime

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTest(TestCase):

    def test_was_published_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        # using assertIs() we want to return False, but it return true
        self.assertIs(future_question.was_recently_published(), False)

    def test_was_published_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_recently_published(), False)

    def test_was_published_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_recently_published(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


# index view test

class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('p:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['lastest_question'], [])

    def test_past_question(self):
        create_question(question_text="Past question.", days=-1)
        response = self.client.get(reverse('p:index'))
        self.assertQuerysetEqual(
            response.context['lastest_question'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        create_question(question_text="Future question.", days=1)
        response = self.client.get(reverse('p:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(
            response.context['lastest_question'], [])

    def test_future_question_and_past_question(self):
        create_question(question_text="Past question", days=-1)
        create_question(question_text="Future question.", days=1)
        response = self.client.get(reverse('p:index'))
        self.assertQuerysetEqual(
            response.context['lastest_question'],
            ['<Question: Past question>']
        )

    def test_two_past_questions(self):
        create_question(question_text="Past question 1", days=-5)
        create_question(question_text="Past question 2", days=-1)
        response = self.client.get(reverse('p:index'))
        self.assertQuerysetEqual(
            response.context['lastest_question'],
            ['<Question: Past question 2>', '<Question: Past question 1>']
        )


# detail view test
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question', days=5)
        url = reverse('p:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('p:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


# result view test
class QuestionResultView(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future Question', days=1)
        url = reverse('p:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past Question', days=-1)
        url = reverse('p:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
