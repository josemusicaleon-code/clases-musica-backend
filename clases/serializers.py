from rest_framework import serializers
from .models import Clase

class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = '__all__'
        read_only_fields = ('created_at',)

