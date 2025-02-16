from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from production.serializer import ManufacturedAircraftSerializer
from production.services.manufactured_aircraft_service import ManufacturedAircraftService


@api_view(['GET'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_manufactured_aircraft_view(request):
    user = request.user
    team_name = user.team.name

    service = ManufacturedAircraftService()
    aircraft_list = service.list_of_all_manufactured_aircraft(team_name)
    serializer = ManufacturedAircraftSerializer(aircraft_list, many=True)
    return Response(serializer.data)
