from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    
 
class Tickers(models.Model):
    sp500_tickers = models.CharField(max_length=30)
    def __str__(self):
        return self.sp500_tickers
    
class Stock(models.Model):
    #ticker = models.CharField(max_length=64) same as symbol
    exchange = models.CharField(max_length=64)
    symbol = models.CharField(max_length=64)
    company_name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=1, max_digits=20)
    last_updated = models.DateTimeField('Last Updated')
    def __str__(self):
        return self.name

class Stock_History(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField('date recorded')
    opening_price = models.DecimalField(max_digits=20, decimal_places=1)
    closing_price = models.DecimalField(max_digits=20, decimal_places=1)
    def __init__(self):
        self.date = timezone.now()
    def __str__(self):
        return self.stock.name