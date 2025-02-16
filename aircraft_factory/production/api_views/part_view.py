from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from production.serializer import PartSerializer
from production.services.part_service import PartService


# This view only for admin..

@api_view(['POST'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_part_view(request):
    data = request.data
    user = request.user

    type = data['type']
    aircraft_id = data['aircraft_id']
    team_id = user.team.id
    team_name = user.team.name  # For permission

    service = PartService()
    part = service.create_part(type, aircraft_id, team_id, team_name)

    serializer = PartSerializer(part)
    return Response(serializer.data)


@api_view(['DELETE'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_part_view(request, id):
    user_team = request.user.team.name
    service = PartService()
    service.delete_part_by_id(id, user_team)

    return Response(status=status.HTTP_204_NO_CONTENT)
