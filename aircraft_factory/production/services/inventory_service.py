from django.db import transaction
from production.exceptions.custom_exception import BusinessException
from production.models import Inventory


class InventoryService:
    def __init__(self,inventory = Inventory):
        self.inventory = inventory

    def list_inventory(self,part_type,team_name):
        self._check_permission(part_type,team_name)
        return self.inventory.objects.filter(part_type=part_type)

    def create_or_update_inventory(self, aircraft_id, part_type):
        with transaction.atomic():
            inventory, created = self.inventory.objects.select_for_update().get_or_create(
                aircraft_id=aircraft_id,
                part_type=part_type
            )
            inventory.quantity += 1
            inventory.save()
        return inventory

    def find_inventory_by_aircraft_id_and_part_type(self, aircraft_id, part_type):
        try:
            inventory = self.inventory.objects.get(part_type=part_type, aircraft_id=aircraft_id)
            return inventory
        except self.inventory.DoesNotExist:
            return "Inventory could not found"

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
