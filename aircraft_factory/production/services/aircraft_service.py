from production.models import Aircraft
from production.exceptions.custom_exception import BusinessException

class AircraftService:

    def __init__(self,aircraft_repository=Aircraft):
        self.aircraft_repository = aircraft_repository

    def find_aircraft_by_id(self,aircraft_id):
        try:
            aircraft = self.aircraft_repository.objects.get(id=aircraft_id)
        except self.aircraft_repository.DoesNotExist:
            raise BusinessException("Aircraft could not found by id !")

        return aircraft