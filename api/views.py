from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Truck, Load
from .serializers import TruckSerializer, LoadSerializer, AllocationPlanSerializer
from ..viewmodels import AllocationViewModel

class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

class LoadViewSet(viewsets.ModelViewSet):
    queryset = Load.objects.all()
    serializer_class = LoadSerializer

class AllocationViewSet(viewsets.ViewSet):
    """
    Viewset to trigger the allocation algorithm.
    """
    def list(self, request):
        viewmodel = AllocationViewModel()
        result = viewmodel.get_allocation_plan()
        
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = AllocationPlanSerializer(result)
        return Response(serializer.data)
