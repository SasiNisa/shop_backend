""" from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

    def get_permissions(self):
        # Only admin can create/update/delete
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        # Anyone can list/retrieve
        return [AllowAny()]


 """

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-created_at')

        # Filter by 'featured' query parameter
        featured = self.request.query_params.get('featured')
        if featured == 'true':
            queryset = queryset.filter(is_featured=True)

        # Filter by 'new' query parameter (optional: limit latest N)
        new = self.request.query_params.get('new')
        if new == 'true':
            queryset = queryset.filter(is_new=True)        #.order_by('-created_at')[:8]

        return queryset
