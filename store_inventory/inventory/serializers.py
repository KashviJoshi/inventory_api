# serializers.py
from rest_framework import serializers
from .models import Cuboid

class CuboidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuboid
        fields = ['id', 'length', 'breadth', 'height', 'created_by', 'created_at', 'updated_at', 'area', 'volume']
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'area', 'volume']
