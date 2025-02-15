from production.exceptions.custom_exception import BusinessException
from production.models import AssemblyItem, Assembly
from production.services.inventory_service import InventoryService


class AssemblyService:
    def __init__(self, assembly = Assembly,
                 assembly_item = AssemblyItem,
                 inventory_service = InventoryService()):
        self.assembly = assembly
        self.assembly_item = assembly_item
        self.inventory_service = inventory_service

    def start_assembly(self, aircraft_id, items, user_id, team):
        team_name = team.name
        self._check_permission(team_name)

        inventory_requirements = self._validate_items_and_get_requirements(aircraft_id, items)

        self._deduct_inventory_quantities(inventory_requirements)

        assembly = self._create_assembly_record(aircraft_id, user_id)

        self._link_items_to_assembly(assembly, inventory_requirements)

        return assembly

    def _validate_items_and_get_requirements(self, aircraft_id, items):
        inventory_requirements = []

        for item in items:
            part_type = item['part_type']
            required_quantity = item['quantity']

            inventory = self.inventory_service.find_inventory_by_aircraft_id_and_part_type(
                aircraft_id,
                part_type
            )

            if inventory.quantity < required_quantity:
                raise BusinessException(
                    f"Insufficient stock for {part_type}. Available: {inventory.quantity}"
                )

            inventory_requirements.append((inventory, required_quantity))

        return inventory_requirements

    def _deduct_inventory_quantities(self, inventory_requirements):
        for inventory, quantity in inventory_requirements:
            inventory.quantity -= quantity
            inventory.save()

    def _create_assembly_record(self, aircraft_id, user_id):
        return self.assembly.objects.create(
            aircraft_id=aircraft_id,
            created_by=user_id
        )

    def _link_items_to_assembly(self, assembly, inventory_requirements):
        for inventory, quantity in inventory_requirements:
            self.assembly_item.objects.create(
                assembly=assembly,
                item=inventory,
                quantity=quantity
            )


    def _check_permission(self,team_name):

        if team_name != "MONTAJ TAKIMI":
            raise BusinessException(f"Members of {team_name} can not create aircraft")

