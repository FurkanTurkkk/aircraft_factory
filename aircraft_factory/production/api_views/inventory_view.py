from django.views.decorators.csrf import csrf_exempt
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
    team_name = user.team.name
    part_type = request.query_params.get('part_type')

    service = InventoryService()
    part_list = service.list_inventory(part_type,team_name)
    serializer = InventorySerializer(part_list, many=True)
    return Response(serializer.data)
