from django.urls import path

from . import views

app_name = 'dividends'
urlpatterns = [
    path('<str:ticker>/<int:dividends_years_back>', views.main_dividends_results, name='dividends_data'),

    # path('all_dividends/<str:ticker>/<int:years_back>/', views.dividends_over_last_certain_years, name='all_dividends_over_time'),

]
