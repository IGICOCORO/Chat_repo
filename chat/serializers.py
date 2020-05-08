from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from .views import *

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         # The default result (access/refresh tokens)
#         data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
#         # Custom data you want to include
#         data.update({"user": self.user.username})
#         data.update({"id": self.user.id})
#         # and everything else you want to send in the response
#         return data
