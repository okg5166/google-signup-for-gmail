import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'google_signup_for_gmail.settings')
application = get_wsgi_application() 