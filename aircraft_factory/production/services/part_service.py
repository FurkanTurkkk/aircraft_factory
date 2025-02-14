from django.db import transaction

from production.models import Part
from production.exceptions.custom_exception import BusinessException

class PartService:
    def __init__(self,part_model=Part,aircraft_service=None):
        if aircraft_service is None:
            raise BusinessException("aircraft_service is required")
        self.part_model = part_model
        self.aircraft_service = aircraft_service

    @transaction.atomic
    def create_part(self, added_by, part_type, stock, aircraft_id, airplane_type_of_part):
        self._check_permission(added_by, part_type)
        aircraft = self._get_aircraft_by_aircraft_id(aircraft_id)
        self._validate_aircraft_type(aircraft, airplane_type_of_part,part_type)
        return self._create_or_update_part(added_by, part_type, stock, aircraft, airplane_type_of_part)

    def find_part_by_id(self, part_id):
        try:
            return self.part_model.objects.get(id=part_id)
        except self.part_model.DoesNotExist:
            raise BusinessException("Part could not found by id!")

    def increase_stock_of_part(self, part_id, quantity):
        try:
            part = self.part_model.objects.get(id=part_id)
        except self.part_model.DoesNotExist:
            raise BusinessException("Part could not found by id!")
        part.increase_stock(quantity)
        part.save()
        return part, "Part quantity increased successfully"

    def decrease_stock_of_part(self, part_id, quantity):
        try:
            part = self.part_model.objects.get(id=part_id)
        except self.part_model.DoesNotExist:
            raise BusinessException("Part could not found by id!")

        if quantity > part.stock:
            raise BusinessException("This part don't have enough stock!")

        part.decrease_stock(quantity)
        part.save()
        return part, "Part quantity decreased successfully..."

    def _check_permission(self,added_by,part_type):
        team_name = added_by.team.name.replace(' TAKIMI', '').upper()
        if team_name not in part_type.upper():
            raise BusinessException("You do not have permission to create this part ! ")

    def _get_aircraft_by_aircraft_id(self,aircraft_id):
        aircraft = self.aircraft_service.find_aircraft_by_id(aircraft_id)
        if not aircraft:
            raise BusinessException("Aircraft not found !")
        return aircraft

    def _validate_aircraft_type(self,aircraft,airplane_type_of_part,part_type):
        if airplane_type_of_part != aircraft.type:
            raise BusinessException(
                f"This {part_type} of type {airplane_type_of_part} does not belong to {aircraft.type} !"
            )

    def _create_or_update_part(self,added_by,part_type,stock,aircraft,airplane_type_of_part):
        part, created = self.part_model.objects.get_or_create(
            part_type=part_type,
            airplane_type_of_part=airplane_type_of_part,
            defaults={
                'stock': stock,
                'aircraft': aircraft,
                'added_by': added_by
            })
        if not created:
            part.increase_stock(quantity=stock)
            part.save()
            message = "Part already exist , increasing stock..."
        else:
            message = "Part created successfully..."
        return part,message
