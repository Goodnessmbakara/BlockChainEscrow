import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets, generics,permissions
from rest_framework.permissions import AllowAny



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (UserSerializer, GoogleSocialAuthSerializer,
    RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, 
    EmailVerificationSerializer, LoginSerializer, LogoutSerializer
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

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)



class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)