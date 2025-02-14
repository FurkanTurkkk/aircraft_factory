from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from production.exceptions.custom_exception import BusinessException
from production.serializer import PartSerializer
from production.services.part_service import PartService


@api_view(['POST'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_part_view(request):
    data = request.data
    user = request.user
    try:
        service = PartService()
        part , message = service.create_part(
            added_by=user,
            part_type=data.get('part_type'),
            stock=data.get('stock'),
            aircraft_id=data.get('aircraft_id'),
            airplane_type_of_part=data.get('airplane_type_of_part'),
        )
        serializer = PartSerializer(part)
        return Response({
            "message": message,
            "part": serializer.data
        })
    except BusinessException as e:
        return Response({'error' : e.detail}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def increase_stock_of_part_view(request,part_id):
    data = request.data
    user = request.user
    quantity = int(request.query_params.get('quantity',0))
    try:
        service = PartService()
        part = service.increase_stock_of_part(part_id, quantity)
        serializer = PartSerializer(part)
        return Response(serializer.data)
    except BusinessException as e:
        return Response({'error' : e.detail}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def decrease_stock_of_part_view(request, part_id):
    """
        decrease stock of part by quantity:
        example of URL : /api/path/decrease/3/?quantity=2
    """
    quantity = int(request.query_params.get('quantity', 0))
    try:
        service = PartService()
        part = service.decrease_stock_of_part(part_id, quantity)
        serializer = PartSerializer(part)
        return Response(serializer.data)
    except BusinessException as e:
        return Response({'error' : e.detail}, status=status.HTTP_400_BAD_REQUEST)