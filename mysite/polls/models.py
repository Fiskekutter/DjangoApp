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
    
    
    
#class Stock(models.Model):
#    #ticker = models.CharField(max_length=64) same as symbol
#    exchange = models.CharField(max_length=64)
#    symbol = models.CharField(max_length=64)
#    name = models.CharField(max_length=200)
#    price = models.DecimalField()
#    last_updated = models.DateTimeField('Last Updated')

#class Stock_History(models.Models):
#    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
#    opening_price = models.DecimalField(max_digits=200)
#    closing_price = models.DecimalField(max_digits=200)