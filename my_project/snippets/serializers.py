from django.contrib.auth.models import User
from rest_framework import serializers

from snippets.models import Snippet, UserDetails

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos']

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    email = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    class Meta:
        model = UserDetails
        fields = ['username', 'email','password', 'phone_number', 'address']

    def validate_email(self, data):
        try:
            print("data", data)
            User.objects.get(email=data)
            raise serializers.ValidationError("email already exist. Please try another one.")
        except User.DoesNotExist:
            return data
        except User.MultipleObjectsReturned:
            print("data", data)
            raise serializers.ValidationError("email already exist. Please try another one.")

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        return data


