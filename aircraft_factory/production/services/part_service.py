from django.db import transaction

from production.models import Part
from production.exceptions.custom_exception import BusinessException

class PartService:
    def __init__(self,part_model=Part,aircraft_service=None):
        self.part_model = part_model
        self.aircraft_service = aircraft_service

    @transaction.atomic
    def create_part(self,added_by,part_type,stock,aircraft_id,variant_value):
        from production.services.aircraft_service import AircraftService

        if not self.aircraft_service:
            self.aircraft_service = AircraftService()

        aircraft = self.aircraft_service.find_aircraft_by_id(aircraft_id)

        if aircraft is None:
            raise BusinessException("Aircraft not found")

        if variant_value != aircraft.type:
            raise BusinessException(
                f"Girilen {part_type} varyantı '{variant_value}' uçağın türü '{aircraft.type}' ile uyuşmuyor ! "
            )

        part = self.part_model.objects.create(
            part_type = part_type,
            variant_type = variant_value,
            stock = stock,
            aircraft = aircraft,
            added_by = added_by
        )

        return part


    def find_part_by_id(self, part_id):
        part = Part.objects.get(id=part_id)
        return part
    
    def add_part(self,part_id,quantity):

        try:
            part = self.part_model.objects.get(id=part_id)
        except self.part_model.DoesNotExist:
            raise BusinessException("Parça bulunamadı!")
        
        part.increase_stock(quantity)
        part.save()
        return part

    def delete_part(self,part_id,quantity):

        try:
            part = self.part_model.objects.get(id=part_id)
        except self.part_model.DoesNotExist:
            raise BusinessException("Parça bulunamadı!")
        
        if quantity>part.stock:
            raise BusinessException("Stokta yeterli miktar bulunmamaktadır !")
        
        part.decrease_stock(quantity)
        part.save()
        return part
    
    

    
       