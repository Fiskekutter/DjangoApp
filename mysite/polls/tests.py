from django.test import TestCase

# Create your tests here.
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question
from polls import fetcher
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd



class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        print("Test running for Question Model: test_was_published_recently_with_future_question")
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_old_question(self):
        print("Test running for Question Model: test_was_published_recently_with_old_question")
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        print("Test running for Question Model: test_was_published_recently_with_recent_question")
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
        
def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        print("Test running for Question Index View: test_no_questions")
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        print("Test running for Question Index View: test_past_questions")
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        print("Test running for Question Index View: test_future_questions")
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        print("Test running for Question Index View: test_future_question_and_past_question")
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        print("Test running for Question Index View: test_two_past_questions")
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        print("Test running for Question Detail View: test_future_question")
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        print("Test running for Question Detail View: test_past_question")
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
class test_api(TestCase):
    def test_fetch_single(self):
        x = fetcher.stock_api_data_collector_class()
        ticker = 'wer'
        url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}'
        yo = x.get_data(url)
        yo = yo[0]
        yo = yo[['Symbol']].to_dict()
        #print(yo)
        m = []
        s = 0
        yo = yo['Symbol']
        for i in yo:
            m.append(yo[s])
            s = s+1
            
        print(m)

    
        #print(yo['Symbol'])
        
    def test_fetch_historical(self):
        x = fetcher.stock_api_data_collector_class()
        #print(x.get_stock_history_all('aapl'))
    
    def test_tickers_sp500(self):
        x = fetcher.stock_api_data_collector_class()
        #print(x.ticker)
        
    def test_html_fetch(self):
        x = fetcher.stock_api_data_collector_class()
        #print(x.get_current_stock_price('aapl'))
    
    def test_html_scroller(self):
        x = fetcher.stock_api_data_collector_class()
        #print(x.html_scroller('aapl'))
    
    def test_download_historical_data(self):
        x = fetcher.stock_api_data_collector_class()
        #x.download_historical_data(ticker)
        #x.download_historical_data('aapl')
        #print("\\")