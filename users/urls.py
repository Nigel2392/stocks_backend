from django.urls import path

from . import views

app_name = 'dividends'
urlpatterns = [
    path('<str:user_id>', views.main_user_profile, name='user_profile_data'),
]
