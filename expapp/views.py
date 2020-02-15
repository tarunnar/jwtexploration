from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from expapp.models import Employee
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BaseAuthentication, TokenAuthentication
from rest_framework import status
import json
from django.contrib import auth
from django.contrib.auth.models import User
from .models import MyUser
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

from serializers.EmployeeSerializer import EmployeeSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return JsonResponse(content)


class LoginView(APIView):

    def post(self, request):
        response = dict()
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if not username or not password:
            response["status"], response["message"] = [1, "provide username and password"]
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
        user = auth.authenticate(email=username, password=password)
        if user is not None:
            auth.login(request, user)
            token, created = Token.objects.get_or_create()
            response["status"], response["message"] = [1, "login successful"]
            response["token"] = token
            return JsonResponse(response, status=status.HTTP_200_OK)
        response["status"], response["message"] = [1, "User not found"]
        return JsonResponse(response, status=status.HTTP_404_NOT_FOUND)


class SignUpView(APIView):

    def post(self, request):
        response = dict()
        data = request.data
        keys = {"username": [1, "provide username"],
                "password": [1, "provide password"],
                "confirm_password": [1, "provide confirm password"]}
        for key in keys:
            if not data.get(key, None):
                response["status"], response["message"] = keys[key]
                return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)

        if data["password"] == data["confirm_password"]:
            try:
                user = User.objects.get(username=data["username"])
            except User.DoesNotExist:
                user = User.objects.create_user(username=data["username"], password=data["password"])
                token, created = Token.objects.get_or_create(user=user)
                response["status"], response["message"] = [1, "user created successfully"]
                response["token"] = token.key
                return JsonResponse(response, status=status.HTTP_201_CREATED)
            else:
                response["status"], response["message"] = [1, "Someone has already created account with this email"]
                return JsonResponse(response, status=status.HTTP_409_CONFLICT)
        response["status"], response["message"] = [1, "provide password and confirm password same"]
        return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeGenericListView(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                              mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    lookup_field = "id"

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)

