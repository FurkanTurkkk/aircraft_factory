from production.exceptions.custom_exception import BusinessException
from production.models import Aircraft


class AircraftService:

    def __init__(self, aircraft=Aircraft):
        self.aircraft = aircraft

    def create_aircraft(self, aircraft_type):
        if self.aircraft.objects.filter(type=aircraft_type).exists():
            raise BusinessException("Aircraft already exists.")
        aircraft = self.aircraft.objects.create(type=aircraft_type)

        return aircraft

    def get_all_aircraft(self):
        aircraft_list = self.aircraft.objects.all()
        return aircraft_list
