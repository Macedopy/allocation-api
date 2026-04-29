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
    Viewset to receive loads and trigger the allocation algorithm immediately.
    """
    def create(self, request):
        # Expecting a list of loads in 'cargas' key or the root
        loads_data = request.data.get('cargas') if isinstance(request.data, dict) else request.data
        
        if not loads_data or not isinstance(loads_data, list):
            return Response(
                {"error": "You must provide a list of loads in the 'cargas' field or as the root of the body."},
                status=status.HTTP_400_BAD_REQUEST
            )

        viewmodel = AllocationViewModel()
        result = viewmodel.get_allocation_plan(loads_data=loads_data)
        
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = AllocationPlanSerializer(result)
        return Response(serializer.data)

    def list(self, request):
        # Keep list for compatibility with DB if needed, but primarily use POST
        viewmodel = AllocationViewModel()
        result = viewmodel.get_allocation_plan()
        
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = AllocationPlanSerializer(result)
        return Response(serializer.data)
