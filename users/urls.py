from django.urls import path

from . import views

app_name = 'dividends'
urlpatterns = [
    path('<str:user_id>', views.get_user_profile, name='get_user_profile'),
]
