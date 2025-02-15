from django.contrib.auth.decorators import user_passes_test
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from production.exceptions.custom_exception import BusinessException
from production.serializer import TeamSerializer
from production.services.team_service import TeamService


def is_superuser(user):
    return user.is_authenticated and user.is_superuser


@api_view(['POST'])
@user_passes_test(is_superuser)
def create_view(request):
    data = request.data
    team_name = data.get('team_name')
    team_service = TeamService()
    team = team_service.create_team(team_name)

    serialized_team = TeamSerializer(team)
    return Response(serialized_team.data, status=status.HTTP_201_CREATED)


