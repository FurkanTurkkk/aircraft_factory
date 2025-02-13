
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from production.serializer import TeamSerializer
from production.services.team_service import TeamService


@api_view(['POST'])
@authentication_classes([])
def create_view(request):
    data = request.data
    name = data['name']

    team_service = TeamService()
    team = team_service.create_team(name)
    serializer = TeamSerializer(team)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
def get_view(request):
    team_service = TeamService()
    team_service.find_team_by_id(request.data.get('id'))