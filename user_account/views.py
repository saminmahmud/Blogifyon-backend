from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserAccountSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth import get_user_model, authenticate, login, logout
User = get_user_model()


class UserAccountViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    

class UserRegistrationApiView(APIView):
    authentication_classes = [] 
    permission_classes = [] 
    serializer_class = UserRegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            # print(user)
            token = default_token_generator.make_token(user)
            # print("token ", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # print("uid ", uid)
            confirm_link = f'http://127.0.0.1:8000/accounts/activate/{uid}/{token}'
            email_subject = 'Confirm Your Email'
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            return Response({"message": "Check your mail for confirmation"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # return HttpResponseRedirect(reverse('login'))
        return HttpResponseRedirect('http://localhost:5173/')
        # return HttpResponseRedirect('http://127.0.0.1:5500/login.html')
        # return Response({'message' : "Your account activation done. Now login."}, status=status.HTTP_200_OK)
    else:
        return HttpResponse("<h1>Invalid activation link.</h1>", status=406)
        # return HttpResponseRedirect('http://127.0.0.1:5500/signup.html')
        # return Response({'error' : "Invalid Credential"}, status.HTTP_406_NOT_ACCEPTABLE)


class UserLoginApiView(APIView):
    authentication_classes = []  # No authentication required
    permission_classes = []  # No permission required
    
    def post(self, request):
        serializer = UserLoginSerializer(data = self.request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(email= email, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                # print(token)
                # print(_)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id}, status=status.HTTP_200_OK)
            else:
                return Response({'error' : "Invalid Credential"}, status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLogoutView(APIView):

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            token = token.replace('Token ', '')
            try:
                token_obj = Token.objects.get(key=token)
                token_obj.delete()
            except Token.DoesNotExist:
                pass 

        logout(request)
        return JsonResponse({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    
