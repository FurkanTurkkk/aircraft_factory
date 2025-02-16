from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from production.serializer import InventorySerializer
from production.services.inventory_service import InventoryService

@api_view(['GET'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_quantity_and_part_of_inventory(request):
    user = request.user
    team = user.team

    service = InventoryService()
    part_list = service.list_inventory(team)
    serializer = InventorySerializer(part_list, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def increase_quantity(request):

    part_id = request.data.get("part_id")
    quantity = request.data.get("quantity", 1)

    if not part_id:
        return Response({"error": "part_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    service = InventoryService()
    updated_part = service.increase_quantity(part_id, quantity)

    if updated_part:
        serializer = InventorySerializer(updated_part)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"error": "Part not found or could not be updated"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def decrease_quantity(request):
    part_id = request.data.get("part_id")
    quantity = request.data.get("quantity", 1)

    if not part_id:
        return Response({"error": "part_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    service = InventoryService()
    try:
        updated_part = service.decrease_quantity(part_id, quantity)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # If quantity = 0 raise Business Exception in service layer.

    if updated_part:
        serializer = InventorySerializer(updated_part)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"error": "Part not found or could not be updated"}, status=status.HTTP_400_BAD_REQUEST)