from rest_framework.generics import GenericAPIView
from .serializers import UserRegistrationSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_generated_otp_to_mail
from .models import OneTimePassword
from django.http import HttpResponse
from django.shortcuts import render
from .permissions import CanAddEventsPermission
from rest_framework.decorators import api_view, permission_classes
from events.serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated

class RegisterUserView(GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data

            send_generated_otp_to_mail(user_data['email'], request)

            return Response(
                {
                    'data': user_data,
                    'message': 'thank for signing up, passcode is sent to your email'
                },
                status= status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyUserEmailView(GenericAPIView):
    def post(self, request):
         try:
           passcode = request.data.get('otp')
           user_pass_obj = OneTimePassword.objects.get(otp=passcode)
           user= user_pass_obj.user
           if not user.is_verified:
              user.is_verified= True
              user.save()
              return Response({
                 'message': 'account verified successfully',
              }, status = status.HTTP_200_OK)
              return Response({
                 "message": "passcode is invalid or user is already verified"
              }, status = status.HTTP_204_NO_CONTENT)

         except OneTimePassword.DoesNotExist as e:
              return Response({"message":"passcode not provided"}, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data= request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status = status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([CanAddEventsPermission])
def create_event(request):
    if request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response()

class TestAuthenticateRequest(GenericAPIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        data = {
            'msg': "welcome"
        }

        return Response(data, status=status.HTTP_200_OK)


