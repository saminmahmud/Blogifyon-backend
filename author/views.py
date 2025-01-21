from django.shortcuts import render
from .models import Author, Review
from rest_framework import status
from rest_framework.response import Response
from .serializers import AuthorProfileSerializer, AuthorSerializer, ReviewSerializer, SendEmailToAuthorSerializer
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter

class ReviewView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [SearchFilter]
    search_fields = ['reviewed_author__user__username']

    
class AuthorProfileViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__id']



class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__username']

class send_email_to_author_view(APIView):
    def post(self, request):
        serializer = SendEmailToAuthorSerializer(data = self.request.data)
        if serializer.is_valid():
            author_id = serializer.validated_data['author_id']
            sender_id = serializer.validated_data['sender_id']
            content = serializer.validated_data['content']

            author = get_object_or_404(Author, id=author_id)
            sender = get_object_or_404(Author, id=sender_id)

            author_email = author.user.email
            sender_name = sender.user.username 
            sender_email = sender.user.email

            send_mail(
                subject=f'"{sender_name}" sent you an email.',
                message=f"Sender: {sender_email}\n\n{content}",
                from_email=sender_email,  
                recipient_list=[author_email],  
                fail_silently=False,
            )
            return Response({"status": "Email sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


