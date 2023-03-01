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
 
    
class Ticker(models.Model):
    symbol = models.CharField(max_length=30)
    def __str__(self):
        return self.symbol
 
   
class Stock(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    companyname = models.CharField(max_length=200, default="")
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    last_updated = models.DateTimeField('Last Updated')
    def __init__(self) -> None:
        self.last_updated = timezone.now()
    def update_date(self):
        self.last_updated = timezone.now()
    def __str__(self):
        return f"{self.companyname}: {str(self.price)}"


class Stock_History(models.Model):
    #stock = models.ForeignKey(Stock, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField('date recorded')
    opening_price = models.DecimalField(max_digits=20, decimal_places=1, default=0)
    closing_price = models.DecimalField(max_digits=20, decimal_places=1, default=0)
    def __init__(self) -> None:
        self.date = timezone.now()
        
    def __str__(self):
        return "Yep"