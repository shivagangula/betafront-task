from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings



os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')
app = Celery('pokemon_tasks')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.timezone = 'UTC'
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

