=====
BCMR
=====

BCMR or Bitcoin Cash Metadata Registry is a Django app for storing, accessing and managing CashToken BCMRs.

Quick start
-----------

1. Add the following to your requirements.txt::
    
    Pillow==9.4.0
    django-bcmr==x.x.x

2. Add "bcmr" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'bcmr',
    ]

3. Include the bcmr URLconf in your project urls.py like this::

    path('bcmr/', include('bcmr.urls')),

4. Add media config on settings.py::

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

5. (upon deployment) Add media location path on nginx configuration file::

    location /media/ {
        autoindex on;
        alias /<your_path_to the_media_folder>/;
    }

4. Start the development server and visit http://localhost:8000/admin/
   to access the DB (you'll need the Admin app enabled).

5. Visit http://localhost:8000/bcmr/ to check API endpoints for BCMRs and tokens.


REST API
-----------

Registries and tokens created by a user can only be modified/deleted by that user (owner).

All endpoints are restricted on its usage for prevention of users tampering other user's registries and tokens.
An auth token generated upon creation of either a registry or token helps impose this restriction.
This token is used as a header for identification if the user modifying BCMR data is the owner.

The endpoints are restricted as follows::

    GET = no header required
    POST = if header is supplied, created token/registry will belong to that auth token owner
         = if header is not supplied, a new auth token will be generated (new owner)
    PUT/PATCH = header required
    DELETE = header required
