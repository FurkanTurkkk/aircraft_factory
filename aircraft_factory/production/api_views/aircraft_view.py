from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from production.exceptions.custom_exception import BusinessException
from production.serializer import AircraftSerializer
from production.services.aircraft_service import AircraftService


def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@api_view(['GET'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_of_aircraft_view():
    service = AircraftService()
    aircraft_list = service.get_all_aircraft()
    serializer = AircraftSerializer(aircraft_list, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@user_passes_test(is_superuser)
def create_aircraft_view(request):
    data = request.data
    aircraft_type = data['aircraft_type']
    service = AircraftService()
    service.create_aircraft(aircraft_type)
    serializer = AircraftSerializer(aircraft_type)
    return Response(serializer.data)
