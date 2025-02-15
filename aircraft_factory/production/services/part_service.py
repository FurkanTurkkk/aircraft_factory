from django.db import transaction

from production.exceptions.custom_exception import BusinessException
from production.models import Part
from production.services.inventory_service import InventoryService


class PartService:
    def __init__(self, part=Part, inventory_service=InventoryService()):
        self.part = part
        self.inventory_service = inventory_service


    def create_part(self, type, aircraft_id, team_id, team_name, created_by):
        # TODO: self._check_permission(added_by, part_type)
        self._check_permission(type, team_name)
        part = self.part.objects.create(type=type, aircraft_id=aircraft_id, team_id=team_id, creator_id=created_by)
        self.inventory_service.create_or_update_inventory(aircraft_id,part.type)
        return part

    def find_part_by_id(self, part_id):
        try:
            return self.part.objects.get(id=part_id)
        except self.part.DoesNotExist:
            raise BusinessException(f"Part could not found by id: {part_id}")

    def delete_part_by_id(self, part_id):
        part = self.find_part_by_id(part_id)
        part.delete()

    def _check_permission(self, type, team_name):
        team_mapping = {
            'KANAT': 'KANAT TAKIMI',
            'GOVDE': 'GOVDE TAKIMI',
            'KUYRUK': 'KUYRUK TAKIMI',
            'AVIYONIK': 'AVIYONIK TAKIMI'
        }
        expected_team = team_mapping.get(type)
        if not expected_team or team_name != expected_team:
            raise BusinessException(f"Team of user {team_name} not compatible with part {type}")

