import random
import hashlib

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from snippets.models import Snippet, UserDetails
from snippets.serializers import SnippetSerializer, RegisterSerializer, LoginSerializer


# Create your views here.

@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def generate_activation_key():
    return "asdasdsadsdfdf7657658765"

class RegistrationAPI(viewsets.ViewSet):
    model = UserDetails
    queryset = UserDetails.objects.all()
    serializer_class = RegisterSerializer
    authentication_classes = []

    def register(self, request, **kwargs):
        res = {'status': False, 'results': [{'msg': 'Not a valid credential!'}]}

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            print("serializer not valid")
            user = User.objects.create_user(username=serializer.data['username'],
                                     email=serializer.data['email'],
                                     is_active=True)
            user.set_password(serializer.data.get('password'))
            user.save()
            user_detail = UserDetails.objects.create(user=user, phone_number=serializer.data.get('phone_number', 0),
                                                     address=serializer.data.get("address"))
            user_detail.activation_key = generate_activation_key()
            user_detail.is_activated = True
            user_detail.save()
            res = {"status": True, "results": [{"msg": "User is successfully registered"}]}
            return Response(res)
        else:
            print(serializer.errors, "serializer is not valid")
            return Response(res)

    def retrieve(self, request, *args, **kwargs):
        return Response(self.serializer_class().data)

class LoginAPI(viewsets.ModelViewSet):
    """
    Purpose: APIs used to perform the authentication purpose such as login, regitration
    Description:
        GET:
            Get will be for authenticate user login
    """
    model = User
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def retrive(self, request, **kwargs):
        login_serializer = LoginSerializer(data=request.data)
        pass

    def authenticate_user(self, request, **kwargs):
        data = request.data or request.GET
        login_serializer = LoginSerializer(data=request.data)
        if login_serializer.is_valid():
            username = login_serializer.data['username']
            password = login_serializer.data['password']
            username = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user:
                return Response({'status': True, 'results': [{"msg": "User is Authenticated successfully"}]})
        else:
            return Response({'status': False, 'results': [{"msg": 'Not Valid Credentials, Please Try Again'}]})

    def forgot_password(self, request, **kwargs):
        return Response({"status": True})
