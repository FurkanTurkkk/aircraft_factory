from production.models import Part,Aircraft
from production.exceptions.custom_exception import BusinessException

class PartService:
    def __init__(self,part_model=Part,aircraft_model=Aircraft):
        self.part_model = part_model
        self.aircraft_model = aircraft_model
    
    def create_part(self,added_by,part_type,stock,aircraft_id,variant_value):

        try:
            aircraft = self.aircraft_model.objects.get(id=aircraft_id)
        except self.aircraft_model.DoesNotExist:
            raise BusinessException("Uçak bulunamadı!")

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

    
    def add_part(self,part_id,quantity):

        try:
            part = self.part_model.objects.get(id=part_id)
        except self.part_model.DoesNotExist:
            raise BusinessException("Parça bulunamadı!")
        
        part.increase_stock(quantity)

        return part

    def delete_part(self,part_id,quantity):

        try:
            part = self.part_model.objects.get(id=part_id)
        except self.part_model.DoesNotExist:
            raise BusinessException("Parça bulunamadı!")
        
        if quantity>part.stock:
            raise BusinessException("Stok sayısı sıfırın altına inemez ! ")
        
        part.decrease_stock(quantity)

        return part

    
       