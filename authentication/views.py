from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from authentication.models import User
from authentication.renderers import UserRenderer
from authentication.serializers import PasswordResetEmailSerializer, RegisterSerializer, EmailVerifySerializer, LoginSerializer, SetNewPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken 
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

# Create your views here.
class RegisterView(GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        
        user = User.objects.get(email = user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')  #in urls.py

        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username+', Use link below to verify your mail \n'+absurl
        data = {
            'email_subject':'Verify your email',
            'email_body' : email_body,
            'to_email' : user.email
        }

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)

token_param_config = openapi.Parameter('token',
                                       in_=openapi.IN_QUERY,
                                       description='Description',
                                       type=openapi.TYPE_STRING)

class VerifyEmail(APIView):
    serializer_class = EmailVerifySerializer
   
    @swagger_auto_schema(manual_parameters=[token_param_config],)
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email':'Successfully Activated!'}, status=status.HTTP_200_OK)
        
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Token expired'}, status = status.HTTP_400_BAD_REQUEST)
        
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid Token'}, status = status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class=LoginSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PasswordResetEmailView(GenericAPIView):
    
    serializer_class = PasswordResetEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(request=request).domain
                relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token':token})  #in urls.py
                absurl = 'http://'+current_site + relativeLink
                email_body = 'Hi '+user.username+',\n Use link below to reset your password. \n'+absurl
                data = {
                    'email_subject':'Reset your password', 
                    'email_body' : email_body,
                    'to_email' : user.email
                }

                Util.send_email(data) 

        # serializer.is_valid(raise_exception=True)
        return Response({'success':'A link has been sent on your registered mail id to reset password'},
                        status = status.HTTP_200_OK)

class PasswordTokenCheckView(GenericAPIView):
    def get(self, request, uidb64, token):
    
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token is not valid, please request a new one'},
                            status=status.HTTP_401_UNAUTHORIZED)
        
            return Response({'success':True, 'message':'Credentials valid.', 'uidb64': uidb64, 'token':token},
                            status=status.HTTP_200_OK)
            
        except DjangoUnicodeDecodeError as identifier:
            return Response({'error':'Token is not valid, please request a new one'})
        
class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message':'Password Successfully reset!'},
                        status = status.HTTP_200_OK)