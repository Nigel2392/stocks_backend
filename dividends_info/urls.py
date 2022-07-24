from django.urls import path

from . import views

app_name = 'dividends'
urlpatterns = [
    path('', views.index, name='index'),
    path('dividend_yield_change/<str:ticker>/<int:years_ago>/', views.get_dividend_yield_change_for_certain_years_ago_view, name='dividend_change'),
    path('current_yield/<str:ticker>/', views.current_dividend_yield_view, name='current_yield'),

]
