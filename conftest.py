"""
Pytest configuration for convocacao project.
"""
import os
import django
from django.conf import settings
from django.test.utils import get_runner

# Configure Django settings for testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# def pytest_configure():
#     """Configure pytest with Django settings."""
#     settings.configure(
#         DEBUG=True,
#         DATABASES={
#             'default': {
#                 'ENGINE': 'django.db.backends.sqlite3',
#                 'NAME': ':memory:',
#             }
#         },
#         INSTALLED_APPS=[
#             'django.contrib.auth',
#             'django.contrib.contenttypes',
#             'django.contrib.sessions',
#             'rest_framework',
#             'auditlog',
#             'convocacoes',
#         ],
#         USE_TZ=True,
#         SECRET_KEY='test-secret-key',
#     )
