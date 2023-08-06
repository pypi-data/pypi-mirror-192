from setuptools import setup, find_packages

setup(
    name='django-crud-apis',
    version='0.1',
    description='A library for generating CRUD APIs for Django models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/miladmirza75/django_crud_apis',
    author='Milad Mirza',
    author_email='miladmirza75@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Django>=2.2',
        'djangorestframework>=3.9',
        'django-filter>=2.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
