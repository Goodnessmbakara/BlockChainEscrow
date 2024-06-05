import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets, generics,permissions
from rest_framework.permissions import AllowAny


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (UserSerializer, GoogleSocialAuthSerializer,
    RegisterSerializer,
    EmailVerificationSerializer, LoginSerializer, LogoutSerializer, ChangePasswordSerializer
)
from .models import CustomUser
from .renderers import UserRenderer
from .utils import Util




class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class GoogleLoginView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        print("whats upppppppppppppppppppppppppppppppppppp")
        print(user)

        if user.is_authenticated:
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)


class GoogleSocialAuthView(APIView):
    serializer_class = GoogleSocialAuthSerializer 
    
    def post(self, request):  
    
        """
        Post with 'auth_token'
        
        Send an id token as received from google to get user information
        """
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status = status.HTTP_200_OK)

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])
        token = Util.generate_jwt_token(user.id)
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        scheme = settings.APP_SCHEME
        absurl =  scheme+"//"+current_site+relativeLink+"?token="+str(token)
        name = user.email
        if user.username:
            name = user.username
        email_body = 'Hi '+ name+ \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class ResendVerificationEmailView(generics.GenericAPIView):
    """
        ResendVerificationEmailView class handles resending verification emails.
    """
    serializer_class = RegisterSerializer

    def post(self, request):
       data = request.data
       email = data['email']

       try:
            user = CustomUser.objects.get(email=email)

            if user.is_verified:
               return Response({'msg':'User is already verified'})
           
            token = Util.generate_jwt_token(user.id)
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            scheme = request.scheme
            absurl =  scheme+"//"+current_site+relativeLink+"?token="+str(token)
            name = user.email
            if user.username:
                name = user.username
            email_body = 'Hi '+ name+ \
                ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}

            Util.send_email(data=data)

            return Response({'msg':'The verification email has been sent'}, status=status.HTTP_201_CREATED)
       except User.DoesNotExist:
           return Response({'msg':'No such user, register first'})
   
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.object.set_password(serializer.validated_data['new_password'])
            self.object.save()
            return Response({"detail": "Password has been updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)