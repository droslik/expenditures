import os
from celery import Celery
from expenditures import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expenditures.settings')
app = Celery('expenditures')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

