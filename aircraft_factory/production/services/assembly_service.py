from production.exceptions.custom_exception import BusinessException
from production.models import AssemblyItem, Assembly
from production.services.inventory_service import InventoryService
from production.services.manufactured_aircraft_service import ManufacturedAircraftService


class AssemblyService:
    def __init__(self, assembly=Assembly,
                 assembly_item=AssemblyItem,
                 inventory_service=InventoryService(),
                 manufactured_aircraft_service=ManufacturedAircraftService()):
        self.assembly = assembly
        self.assembly_item = assembly_item
        self.inventory_service = inventory_service
        self.manufactured_aircraft_service = manufactured_aircraft_service

    def start_assembly(self, aircraft_id, items, user_id, team):
        team_name = team.name
        self._check_permission(team_name)

        inventory_requirements = self._validate_items_and_get_requirements(aircraft_id, items)

        self._deduct_inventory_quantities(inventory_requirements)

        assembly = self._create_assembly_record(aircraft_id, user_id)

        self._link_items_to_assembly(assembly, inventory_requirements)

        self.manufactured_aircraft_service.add_manufactured_aircraft(assembly, assembly.aircraft)

        return assembly

    def _find_assembly_by_id(self, assembly_id):
        try:
            return self.assembly.objects.get(id=assembly_id)
        except Assembly.DoesNotExist:
            raise BusinessException(f"Assembly not found by id : {assembly_id}")

    def _validate_items_and_get_requirements(self, aircraft_id, items):
        part_requirements = []

        for item in items:
            part_id = item['part_id']
            required_quantity = item['quantity']

            inventory = self.inventory_service.find_inventory_by_aircraft_id_and_part_id(
                aircraft_id,
                part_id
            )

            if inventory.quantity < required_quantity:
                raise BusinessException(
                    f"Insufficient stock for {inventory.part.type}. Available: {inventory.quantity}"
                )

            if inventory.quantity == 0:
                raise BusinessException(
                    f"Your part {inventory.part.type} for {inventory.aircraft.type} is out of stock. Don't forget to add.")

            part_requirements.append((inventory, required_quantity))

        return part_requirements

    def _deduct_inventory_quantities(self, inventory_requirements):
        for inventory, quantity in inventory_requirements:
            inventory.quantity -= quantity
            inventory.save()

    def _create_assembly_record(self, aircraft_id, user_id):
        return self.assembly.objects.create(
            aircraft_id=aircraft_id,
            creator=user_id
        )

    def _link_items_to_assembly(self, assembly, inventory_requirements):
        for inventory, quantity in inventory_requirements:
            self.assembly_item.objects.create(
                assembly=assembly,
                item=inventory.part,
                quantity=quantity
            )

    def _check_permission(self, team_name):

        if team_name != "MONTAJ TAKIMI":
            raise BusinessException(f"Members of {team_name} can not create aircraft")
