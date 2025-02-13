from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from production.exceptions.custom_exception import BusinessException
from production.serializer import PartSerializer
from production.services.part_service import PartService


@api_view(['POST'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_part_view(request):
    """
       Parça ekleme:
       Beklenen POST verisi:
       {
           "parca_tipi": "KANAT",
           "miktar": 5,
           "ucak_id": 1
       }
       """
    data = request.data
    user = request.user
    #SERVİS KISMINA AKTARILACAK HER ŞEY VE DAHA DÜZGÜN VE CLEAN CODE OLUŞTURULACAK.
    #CREATE YAPMAK İSTERKEN EĞER VERİTABANINDA PART TİPİ VE VARYANT TİPİ AYNI OLAN VARSA YA HATA FIRLAT YA DA STOCK ARTTIR

    team_name_without_suffix = user.team.name.replace(' TAKIMI', '').upper()
    if team_name_without_suffix not in data.get('part_type').upper():
        return Response({'You do not have permission to create this part'}, status=status.HTTP_403_FORBIDDEN)

    try:
        service = PartService()
        part = service.create_part(
            added_by=user,
            part_type=data.get('part_type'),
            stock=data.get('stock'),
            aircraft_id=data.get('aircraft_id'),
            variant_value=data.get('variant_type'),
        )
        serializer = PartSerializer(part)
        return Response(serializer.data)
    except BusinessException as e:
        return Response({'error' : e.detail}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_part_view(request,part_id):
    """
        Parça silme (stok azaltma):
        URL örneği: /api/parca/sil/3/?miktar=2
        """
    quantity = int(request.query_params.get('quantity', 0))
    try:
        service = PartService()
        part = service.delete_part(part_id, quantity)
        serializer = PartSerializer(part)
        return Response(serializer.data)
    except BusinessException as e:
        return Response({'error' : e.detail}, status=status.HTTP_400_BAD_REQUEST)