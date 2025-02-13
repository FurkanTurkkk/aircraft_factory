from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_part_view(request):

    data = request.data
    user = request.user

    if user.team.name.upper() != data.get('part_type'):
        return Response({'error':'Bu takım için yetkiniz yok!'},status=403)
    
