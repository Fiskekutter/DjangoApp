from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('stock/', views.StockView.as_view(), name='stock'),
    path('stock/stockdetails/<str:sp500_tickers>', views.StockDetails.as_view(), name='stockdetails'),
    path('stock/<str:name>/test', views.stockdetails, name='test'),
    path('stock/search', views.search, name='stocksearch')
]