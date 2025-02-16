import unittest
from django.test import TestCase
from unittest.mock import MagicMock
from production.exceptions.custom_exception import BusinessException
from production.models import Assembly
from production.services.assembly_service import AssemblyService

class DummyTeam:
    def __init__(self, name):
        self.name = name

class AssemblyServiceTest(TestCase):
    def setUp(self):
        self.dummy_assembly_model = MagicMock()
        self.dummy_assembly_model.DoesNotExist = Assembly.DoesNotExist
        self.dummy_assembly_item_model = MagicMock()
        self.dummy_inventory_service = MagicMock()
        self.dummy_manufactured_aircraft_service = MagicMock()
        self.assembly_service = AssemblyService(
            assembly=self.dummy_assembly_model,
            assembly_item=self.dummy_assembly_item_model,
            inventory_service=self.dummy_inventory_service,
            manufactured_aircraft_service=self.dummy_manufactured_aircraft_service
        )
        self.dummy_inventory = MagicMock()
        self.dummy_inventory.quantity = 10
        self.dummy_assembly_instance = MagicMock()
        self.dummy_assembly_instance.aircraft = MagicMock()

    def test_start_assembly_success(self):
        team = DummyTeam("MONTAJ TAKIMI")
        items = [{'part_type': 'KANAT', 'quantity': 3}]
        self.dummy_inventory_service.find_inventory_by_aircraft_id_and_part_type.return_value = self.dummy_inventory
        self.dummy_assembly_model.objects.create.return_value = self.dummy_assembly_instance
        assembly = self.assembly_service.start_assembly(1, items, 100, team)
        self.assertEqual(assembly, self.dummy_assembly_instance)
        self.assertEqual(self.dummy_inventory.quantity, 7)
        self.dummy_assembly_item_model.objects.create.assert_called_once_with(
            assembly=self.dummy_assembly_instance,
            item=self.dummy_inventory,
            quantity=3
        )

    def test_start_assembly_insufficient_stock(self):
        team = DummyTeam("MONTAJ TAKIMI")
        items = [{'part_type': 'KANAT', 'quantity': 15}]
        self.dummy_inventory.quantity = 10
        self.dummy_inventory_service.find_inventory_by_aircraft_id_and_part_type.return_value = self.dummy_inventory
        with self.assertRaises(BusinessException) as context:
            self.assembly_service.start_assembly(1, items, 100, team)
        self.assertIn("Insufficient stock for KANAT. Available: 10", str(context.exception))

    def test_start_assembly_permission_denied(self):
        team = DummyTeam("YANLIŞ TAKIM")
        items = [{'part_type': 'KANAT', 'quantity': 3}]
        with self.assertRaises(BusinessException) as context:
            self.assembly_service.start_assembly(1, items, 100, team)
        self.assertIn("Members of YANLIŞ TAKIM can not create aircraft", str(context.exception))


if __name__ == '__main__':
    unittest.main()