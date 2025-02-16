from production.exceptions.custom_exception import BusinessException
from production.models import ManufacturedAircraft

class ManufacturedAircraftService:
    def __init__(self,manufactured_aircraft=ManufacturedAircraft):
        self.manufactured_aircraft = manufactured_aircraft


    def add_manufactured_aircraft(self, assembly, aircraft):
        manufactured_aircraft = self.manufactured_aircraft.objects.create(
            assembly=assembly,
            aircraft=aircraft
        )
        return manufactured_aircraft

    def list_of_all_manufactured_aircraft(self,team_name):
        self._check_permission(team_name)
        return self.manufactured_aircraft.objects.all()

    def _check_permission(self,team_name): # Only personnel of assembly users can see list of manufactured aircrafts.

        if team_name != "MONTAJ TAKIMI":
            raise BusinessException(f"Members of {team_name} can not list of manufactured aircraft")
