from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, serializers
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from production.exceptions.custom_exception import BusinessException
from production.serializer import AssemblyRequestSerializer
from production.services.assembly_service import AssemblyService


@api_view(['POST'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def start_assembly_process(request):
    try:
        serializer = AssemblyRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        personnel = request.user

        with transaction.atomic():
            service = AssemblyService()
            assembly = service.start_assembly(
                aircraft_id= serializer.validated_data['aircraft_id'],
                items = serializer.validated_data['items'],
                user_id = personnel,
                team = request.user.team
            )
            return Response(
                {
                    "message" : "Assembly process started.",
                    "assembly_id": assembly.id
                },
                status=status.HTTP_201_CREATED
            )
    except serializers.ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
    except BusinessException as e:
        return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
