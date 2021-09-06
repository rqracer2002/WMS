from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    # def __init__(self, *args, **kwargs):
    #     many = kwargs.pop('many', True)
    #     super(UserSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
