# from __future__ import absolute_import, unicode_literals

# import os

# from celery import Celery
# from django.apps import apps
# from django.conf import settings

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.develop")
# app = Celery("DigitalOffice")
# app.config_from_object("django.conf:settings", namespace="CELERY")

# app.config_from_object(settings)
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])