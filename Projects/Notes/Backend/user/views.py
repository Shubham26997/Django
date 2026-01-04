from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user.models import User
from user.serializer import UserSerializer, LoginSerializer, UserCreateSerializer

# Create your views here.
class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "register":
            return UserCreateSerializer
        return super().get_serializer_class()

    def login(self, request):
        req_data = request.data

        serailzer_data = LoginSerializer(data=req_data)
        if not serailzer_data.is_valid():
            return Response(
                {
                    "data": {},
                    "message": serailzer_data.errors
                }, status=status.HTTP_400_BAD_REQUEST
            )
        user_data = serailzer_data.validated_data # this will return the complete data including the one with write_only fields
        user_obj = authenticate(email=user_data.get('username'), password=user_data.get('password'))
        if not user_obj:
            return Response(
                {
                    "data": {},
                    "message": "Invalid User Credential"
                }, status=status.HTTP_401_UNAUTHORIZED
            )
        # print(user_obj)
        token, _ = Token.objects.get_or_create(user=user_obj)

        return Response(
            {
                "data": {
                    "token": token.key,
                    "user": self.get_serializer(user_obj).data
                },
                "message": "Login Success"
            }, status=status.HTTP_200_OK
        )

    def register(self, request):
        req_data = request.data
        serializer_data = self.get_serializer(data=req_data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(
                {
                    "data": serializer_data.data,
                    "message": "User created successfully"
                }, status=status.HTTP_201_CREATED
            )