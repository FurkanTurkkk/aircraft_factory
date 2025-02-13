from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from production.services.team_service import TeamService
from production.exceptions.custom_exception import BusinessException
from production.serializer import AircraftSerializer
from production.services.aircraft_service import AircraftService


@api_view(['GET'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_of_aircraft_view(request):
    """
       Sadece Montaj Takımı personeli uçakları listeleyebilir.
       """
    user = request.user
    if user.team.name.upper() != "MONTAJ TAKIMI":
        return Response({'error':'You can not list of aircrafts without team.'}, status=status.HTTP_403_FORBIDDEN)

    service = AircraftService()
    aircraft_list = service.get_all_aircraft()
    serializer = AircraftSerializer(aircraft_list, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_aircraft_view(request):
    user = request.user
    team_service = TeamService()
    team = team_service.find_team_by_id(user.team.id)
    if team.name != "MONTAJ TAKIMI":
        return Response({'error': 'You do not have permission to create an aircraft.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = AircraftSerializer(data=request.data)
    if serializer.is_valid():
        aircraft_service = AircraftService()
        aircraft = aircraft_service.create_aircraft(serializer.validated_data)
        serialized_aircraft = AircraftSerializer(aircraft)
        return Response(serialized_aircraft.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def assembly_view(request):
    """
       Montaj işlemi: Montaj Takımı personeli uçağı monte edip kullanılan parçaları kaydeder.
       Beklenen POST verisi:
       {
           "ucak_id": 1,
           "kullanilan_parcalar": [3, 5, 7]
       }
       """
    user = request.user
    if user.team.name.upper() != "MONTAJ TAKIMI":
        return Response({'error':'You can not assembly with team.'}, status=status.HTTP_403_FORBIDDEN)

    data = request.data
    airplane_id = data.get('airplane_id')
    used_parts = data.get('parts_used')
    try:
        service = AircraftService()
        registration = service.assemble_aircraft(user,airplane_id, used_parts)
        serializer = AircraftSerializer(registration)
        return Response(serializer.data)
    except BusinessException as e:
        return Response({'error': e.detail},status=status.HTTP_400_BAD_REQUEST)