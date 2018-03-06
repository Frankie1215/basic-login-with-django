"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path
from django.urls import path
from django.contrib.auth.decorators import login_required
import login.views

urlpatterns = [
    re_path(r'^$', login_required(login.views.success)),
    re_path(r'^login/$', login.views.login, name="login"),
    re_path(r'^signup/$', login.views.signup, name="signup"),
    re_path(r'^verify/$', login.views.verify, name="verify"),
    re_path(r'^success/$', login_required(login.views.success), name="success"),
    re_path(r'^logout/$', login_required(login.views.logout), name="logout"),

    # path('admin/', admin.site.urls),
]
