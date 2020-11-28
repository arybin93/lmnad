# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from project import celeryconfig

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.server')

app = Celery('project')

app.config_from_object(celeryconfig)

app.autodiscover_tasks()
