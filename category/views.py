from django.shortcuts import render
from .serializers import CategorySerializer
from .models import Category
from rest_framework import viewsets

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


