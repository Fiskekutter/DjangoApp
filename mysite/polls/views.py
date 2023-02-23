from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.urls import reverse
from .models import Question, Choice, Stock, Stock_History, Ticker
from django.views import generic
from django.utils import timezone
from polls import fetcher
from requests import exceptions
from urllib import error


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
class StockView(generic.ListView):
    model = Ticker
    template_name = 'polls/stock.html'
    context_object_name = "all_tickers"
    def __init__(self):
        if Ticker.objects.exists() == False:
            fetch = fetcher.stock_api_data_collector_class()
            for item in fetch.ticker:
                x = Ticker(sp500_tickers=item)
                x.save()           
    
    def get_queryset(self):
        fetch = fetcher.stock_api_data_collector_class()
        items = Ticker.objects.all()
        #for item in items[:5]:
            #item.price = fetch.get_current_stock_price(item.sp500_tickers)
            #item.save()
        return Ticker.objects.all()

class StockDetails(generic.ListView):
    model = Ticker
    template_name = 'polls/stockdetails.html'
    context_object_name = "symbols"

    def get_queryset(self):
        self.symbol = get_object_or_404(Ticker, sp500_tickers=self.kwargs['sp500_tickers'])
        symbol = Ticker.objects.get(symbol=self.symbol)
        stock = Stock.objects.get(Ticker=symbol)
        fetch = fetcher.stock_api_data_collector_class()
        try:
            stock.price = fetch.get_current_stock_price(symbol.symbol)
        except(error.URLError):
            raise Http404("Price update failed")
        else:
            stock.save()
        return Ticker.objects.filter(sp500_tickers=self.symbol)
        
def stockdetails(request, name):
    ticker = get_object_or_404(Ticker, sp500_tickers=name)
    return HttpResponseRedirect(reverse('polls:stockdetails', args=(ticker.sp500_tickers,)))

def search(request, name):
    try:
        tick = Ticker.objects.filter(sp500_tickers=request.GET.get('search'))
    except(Ticker.DoesNotExist):
        fetch = fetcher.stock_api_data_collector_class()
        stock_info = fetch.get_stock_data
        
    ticker = get_object_or_404(Ticker, sp500_tickers=name)
    return HttpResponseRedirect(reverse('polls:stockdetails', args=(ticker.sp500_tickers,)))