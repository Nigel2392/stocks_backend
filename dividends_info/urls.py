from django.urls import path

from . import views

app_name = 'dividends'
urlpatterns = [
    path('<str:ticker>', views.main_dividends_results, name='dividends_data'),

    path('current_price/<str:ticker>', views.current_price_view, name='current_price'),
    path('dividend_yield_change/<str:ticker>/<int:years_ago>/', views.get_dividend_yield_change_for_certain_years_ago_view, name='dividend_change'),
    path('current_yield/<str:ticker>/', views.current_dividend_yield_view, name='current_yield'),
    path('all_dividends/<str:ticker>/<int:years_back>/', views.dividends_over_last_certain_years, name='all_dividends_over_time'),
    path('recent_dividend_rate/<str:ticker>/', views.recent_yearly_dividend_rate, name='recent_dividend_rate'),


]
