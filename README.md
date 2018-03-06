# basic-login-with-django
Base on Django 2.0 to build simple login site.  Account verify mail send via Gmail API with Oauth 2.0

## Requirements
* Python 3.4 or above

## Installation

Create and source virtualenv
```
virtualenv venv
source ./venv/bin/activate
```

You can install packages one by one, or use requirements to do
```
pip3 install -r ./requirements
```

Create and setup personal setting.

Run migrate and collectstatic with setting, or set DJANGO_SETTINGS_MODULE environment
```
python3 manage.py migrate --settings=mysite.settings.frankie
python3 manage.py collectstatic --settings=mysite.settings.frankie
```

Get Gmail credential with Oauth 2.0.  Refer below url to create credential.
https://developers.google.com/api-client-library/python/guide/aaa_oauth