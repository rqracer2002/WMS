"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.contrib.auth import views
from two_factor.urls import urlpatterns as tf_urls



from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls

from .views import (
    ExampleSecretView, HomeView, RegistrationCompleteView, RegistrationView,
)


from django.contrib import admin
from two_factor.admin import AdminSiteOTPRequired

admin.site.__class__ = AdminSiteOTPRequired

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('blog.urls')),
    # url(r'^account/login/$', views.LoginView.as_view(), name='login'),
    url(r'^account/logout/$', views.LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),
    path('', include(tf_urls)),
    path(
        '',
        HomeView.as_view(),
        name='home',
    ),
    path(
        'account/logout/',
        LogoutView.as_view(),
        name='logout',
    ),
    path(
        'secret/',
        ExampleSecretView.as_view(),
        name='secret',
    ),
    path(
        'account/register/',
        RegistrationView.as_view(),
        name='registration',
    ),
    path(
        'account/register/done/',
        RegistrationCompleteView.as_view(),
        name='registration_complete',
    ),
    path('', include(tf_twilio_urls)),
    path('', include('user_sessions.urls', 'user_sessions')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
