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
from django.urls import path, include

from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls

from .views import (
    ExampleSecretView, HomeView, RegistrationCompleteView, RegistrationView,
)


from django.contrib import admin
from two_factor.admin import AdminSiteOTPRequired

from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from rest_framework import mixins
from rest_framework import routers
from blog.serializers import UserSerializer,OrderHeaderSerializer
from blog.views import UserViewSet,OrderHeaderViewSet
from blog.models import OrderHeader,AdjustmentLine



admin.site.__class__ = AdminSiteOTPRequired

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrderHeaderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderHeader
        fields = ['url', 'orduniq', 'ordnumber', 'customer','orderdate','expirydate','pod']

# ViewSets define the view behavior.
class OrderHeaderViewSet(viewsets.ModelViewSet):
    queryset = OrderHeader.objects.all()
    serializer_class = OrderHeaderSerializer

class AdjustmentLineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AdjustmentLine
        fields = ['reserved_sku', 'reserved_desc', 'reserved_quant','optima_sku', 'optima_desc', 'optima_quant','in_transit_quant','transfer_quant']

# ViewSets define the view behavior.
class AdjustmentLineViewSet(viewsets.ModelViewSet):
    queryset = AdjustmentLine.objects.all()
    serializer_class = AdjustmentLineSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'orderheaders', OrderHeaderViewSet)
router.register(r'adjustmentline', AdjustmentLineViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
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

from rest_framework.authtoken import views

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
