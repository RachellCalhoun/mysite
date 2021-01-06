from settings import *

DEBUG = False
ALLOWED_HOSTS = ['www.rachellcalhoun.com']

SECRET_KEY = os.environ.get('SECRET_KEY', None)