from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from production.exceptions.custom_exception import BusinessException
from production.serializer import PersonnelSerializer
from production.services.personnel_service import PersonnelService


@api_view(['POST'])
@authentication_classes([])
def register_view(request):
    data = request.data
    username = data['username']
    password = data['password']
    email = data['email']
    team_id = data['team_id']

    try:
        service = PersonnelService()
        user = service.register(username, password, email, team_id)
        serializer = PersonnelSerializer(user)
        return Response(serializer.data)
    except BusinessException as e:
        return Response({'error': e.detail}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
@authentication_classes([])
def login_view(request):
    data = request.data
    username = data['username']
    password = data['password']

    try:
        service = PersonnelService()
        user, token = service.login(username, password, request)
        serializer = PersonnelSerializer(user)

        return Response({
            'user': serializer.data,
            'token': token,
        })
    except BusinessException as e:
        return Response({'error': e.detail}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
