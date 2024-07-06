# views.py
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Cuboid
from .serializers import CuboidSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Store Inventory API. Use /api/ to access the API endpoints.")

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

class CuboidViewSet(viewsets.ModelViewSet):
    queryset = Cuboid.objects.all()
    serializer_class = CuboidSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['length', 'breadth', 'height', 'created_by', 'created_at']
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated, IsStaff]
        elif self.action == 'update' or self.action == 'partial_update':
            self.permission_classes = [permissions.IsAuthenticated, IsStaff]
        elif self.action == 'destroy':
            self.permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
