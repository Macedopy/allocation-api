from rest_framework import serializers
from ..models import Truck, Load

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

class LoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Load
        fields = '__all__'

class AllocationPlanSerializer(serializers.Serializer):
    resumo_geral = serializers.DictField()
    caminhoes = serializers.ListField(child=serializers.DictField())
    nao_alocados = serializers.ListField(child=serializers.DictField())
