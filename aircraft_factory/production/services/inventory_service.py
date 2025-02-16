from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from production.exceptions.custom_exception import BusinessException
from production.models import Inventory
from production.services.part_service import PartService


class InventoryService:
    def __init__(self, inventory=Inventory):
        self.inventory = inventory
        self.part_service = PartService()

    def list_inventory(self, team):
        parts = self.part_service.find_parts_by_team(team.id)
        return self.inventory.objects.filter(part__in=parts).order_by('id')

    def increase_quantity(self, part_id, quantity):
        try:
            inventory_item = Inventory.objects.get(part_id=part_id)
            inventory_item.quantity += int(quantity)
            inventory_item.save()
            return inventory_item
        except ObjectDoesNotExist:
            return None
        except ValueError:
            return None

    def decrease_quantity(self, part_id, quantity):
        try:
            inventory_item = Inventory.objects.get(part_id=part_id)
            new_quantity = inventory_item.quantity - int(quantity)

            if new_quantity < 0:
                raise BusinessException("Stock can not be negative.")
            elif new_quantity == 0:
                raise BusinessException(f"Your part {inventory_item.part.type} for {inventory_item.aircraft.type} is out of stock. Don't forget to add.")

            inventory_item.quantity = new_quantity
            inventory_item.save()
            return inventory_item
        except ObjectDoesNotExist:
            return None
        except ValueError:
            return None

    def create_or_update_inventory(self, aircraft_id, part_id):
        with transaction.atomic():
            inventory, created = self.inventory.objects.select_for_update().get_or_create(
                aircraft_id=aircraft_id,
                part=part_id
            )
            inventory.quantity += 1
            inventory.save()
        return inventory

    def find_inventory_by_aircraft_id_and_part_id(self, aircraft_id, part_id):
        inventory = self.inventory.objects.get(part=part_id, aircraft=aircraft_id)
        return inventory
