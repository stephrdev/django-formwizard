import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-formwizard',
    version='1.0',
    description='A FormWizard for Django with multiple storage backends',
    long_description=read("README.rst"),
    author='Stephan Jaekel',
    author_email='steph@rdev.info',
    url='http://github.com/stephrdev/django-formwizard/',
    packages=find_packages(exclude=['test_project', 'test_project.*']),
    package_data = {
        'formwizard': [
            'templates/*/*.html',
            'tests/wizardtests/templates/*.html'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
)
