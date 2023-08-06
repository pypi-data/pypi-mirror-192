======================
universal-model-django
======================

universal-model-django is a Django app to conduct web-based polls. For each question,
visitors can choose between a fixed number of answers.


Quick start
-----------

1. Add "universal-model-django" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'universaldjango',
    ]

2. dont Include the universaldjango URLconf in your project urls.py like this::

    path('polls/', include('universaldjango.urls')),

3. Run ``python manage.py migrate`` to create the universaldjango models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a universaldjango (you'll need the Admin app enabled).
