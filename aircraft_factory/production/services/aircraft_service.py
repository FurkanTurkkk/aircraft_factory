from production.models import Aircraft, AssemblyRegistration
from production.exceptions.custom_exception import BusinessException


class AircraftService:

    def __init__(self,aircraft_repository=Aircraft,
                 assembly_registration = AssemblyRegistration,
                 part_service = None):
        self.aircraft_repository = aircraft_repository
        self.assembly_registration = assembly_registration
        self.part_service = part_service

    def find_aircraft_by_id(self,aircraft_id):
        try:
            aircraft = self.aircraft_repository.objects.get(id=aircraft_id)
        except self.aircraft_repository.DoesNotExist:
            raise BusinessException("Aircraft could not found by id !")
        return aircraft

    def assemble_aircraft(self,assembler,aircraft_id,parts):

        if assembler.team.name.upper() != "MONTAJ TAKIMI":
            raise BusinessException("Aircraft could not assemble aircraft")

        try:
            aircraft = self.aircraft_repository.objects.get(id=aircraft_id)
        except self.aircraft_repository.DoesNotExist:
            raise BusinessException("Aircraft could not found by id !")
        from production.services.part_service import PartService

        if not self.part_service:
            self.part_service = PartService()

        registration = self.assembly_registration.objects.create(aircraft=aircraft,assembler=assembler)

        for part_id in parts:
            try:
                part = self.part_service.find_part_by_id(part_id)
            except self.part_service.find_part_by_id(part_id).DoesNotExist:
                raise BusinessException(f"Part could not found by id !")
            if part.aircraft != aircraft:
                raise BusinessException(f"This part is not the aircraft {part_id}")
            registration.parts_used.add(part)
        self.aircraft_repository.save(aircraft)
        registration.save()
        return registration

    def create_aircraft(self, data):
        aircraft = Aircraft.objects.create(**data)
        return aircraft

    def get_all_aircraft(self):
        list_aircraft = self.aircraft_repository.objects.all()
        return list_aircraft