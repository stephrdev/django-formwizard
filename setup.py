from setuptools import setup, find_packages
 
setup(
    name='django-formwizard',
    version='0.1',
    description='A FormWizard for Django with multiple storage backends',
    author='Stephan Jaekel',
    author_email='steph@rdev.info',
    url='http://bitbucket.org/stephrdev/django-formwizard/src/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
)
