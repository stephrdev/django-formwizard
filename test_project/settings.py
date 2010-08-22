DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'local_database.db',
        'TEST_NAME': ':memory:',
    }
}

SECRET_KEY = '9(-c^&tzdv(d-*x$cefm2pddz=0!_*8iu*i8fh+krpa!5ebk)+'

ROOT_URLCONF = 'test_project.urls'

TEMPLATE_DIRS = (
    'templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'formwizard',
    'testapp',
    'testapp2',
)

#TEST_RUNNER = 'django-test-coverage.runner.run_tests'