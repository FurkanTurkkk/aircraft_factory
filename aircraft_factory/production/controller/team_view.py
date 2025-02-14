
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from production.exceptions.custom_exception import BusinessException
from production.serializer import TeamSerializer
from production.services.team_service import TeamService


@api_view(['POST'])
@authentication_classes([])  # Gerekli authentication sınıfları eklenebilir
def create_view(request):
    """
    Takım oluşturma view'ı.
    Beklenen JSON:
    {
        "name": "MONTAJ TAKIMI"
    }
    İş mantığı tamamen servis katmanında yönetilir.
    """
    # Serializer ile gelen verinin doğruluğu kontrol edilir.
    serializer = TeamSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Doğrulanmış veriden takım adını alırız.
    team_name = serializer.validated_data.get('name')
    team_service = TeamService()
    try:
        # Servis üzerinden takım oluşturulur; BusinessException durumunda custom_exception_handler devreye girer.
        team = team_service.create_team(team_name)
    except BusinessException as e:
        # Hata oluştuğunda exception handler tarafından yakalanması için exception fırlatıyoruz.
        raise e

    # Oluşturulan takım serializer ile dönüştürülür ve başarılı yanıt döner.
    serialized_team = TeamSerializer(team)
    return Response(serialized_team.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([])  # Gerekli authentication sınıfları eklenebilir
def get_view(request):
    """
    Takım getirme view'ı.
    Takım ID'si sorgu parametresi olarak beklenir.
    Örnek: /api/team?id=1
    """
    team_id = request.query_params.get('id')
    if not team_id:
        return Response({'error': 'Team id is required.'}, status=status.HTTP_400_BAD_REQUEST)

    team_service = TeamService()
    try:
        # Servis üzerinden takım ID'sine göre takım getirilir.
        team = team_service.find_team_by_id(team_id)
    except BusinessException as e:
        # Hata durumunda BusinessException fırlatılır.
        raise e

    serialized_team = TeamSerializer(team)
    return Response(serialized_team.data, status=status.HTTP_200_OK)

