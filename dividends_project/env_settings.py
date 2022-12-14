from decouple import config


SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)

DATABASES = {
   'default': {
       'ENGINE': 'djongo',
       'NAME': 'stocks',
   }
}


