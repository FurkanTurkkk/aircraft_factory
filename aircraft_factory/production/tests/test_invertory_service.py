import unittest

from django.test import TestCase
from unittest.mock import MagicMock, patch
from production.services.inventory_service import InventoryService
from production.exceptions.custom_exception import BusinessException

class InventoryServiceTest(TestCase):
    def setUp(self):
        self.dummy_inventory_model = MagicMock()
        self.dummy_inventory_model.DoesNotExist = Exception
        self.inventory_service = InventoryService(inventory=self.dummy_inventory_model)
        self.dummy_inventory_instance = MagicMock()
        self.dummy_inventory_instance.quantity = 5

    def test_list_inventory_returns_filtered_queryset_when_permission_valid(self):
        dummy_queryset = MagicMock()
        self.dummy_inventory_model.objects.filter.return_value = dummy_queryset
        result = self.inventory_service.list_inventory("KANAT", "KANAT TAKIMI")
        self.assertEqual(result, dummy_queryset)
        self.dummy_inventory_model.objects.filter.assert_called_once_with(part_type="KANAT")

    def test_list_inventory_raises_business_exception_when_permission_invalid(self):
        with self.assertRaises(BusinessException) as context:
            self.inventory_service.list_inventory("KANAT", "YANLIŞ TAKIM")
        self.assertIn("Team of user YANLIŞ TAKIM not compatible with part KANAT", str(context.exception))

    @patch('production.services.inventory_service.transaction.atomic')
    def test_create_or_update_inventory_increments_quantity_and_returns_inventory(self, mock_atomic):
        mock_atomic.return_value.__enter__.return_value = None
        self.dummy_inventory_model.objects.select_for_update.return_value.get_or_create.return_value = (self.dummy_inventory_instance, True)
        result = self.inventory_service.create_or_update_inventory(1, "KANAT")
        self.assertEqual(self.dummy_inventory_instance.quantity, 6)
        self.dummy_inventory_instance.save.assert_called_once()
        self.assertEqual(result, self.dummy_inventory_instance)

    def test_find_inventory_by_aircraft_id_and_part_type_returns_inventory_when_found(self):
        self.dummy_inventory_model.objects.get.return_value = self.dummy_inventory_instance
        result = self.inventory_service.find_inventory_by_aircraft_id_and_part_id(1, "KANAT")
        self.assertEqual(result, self.dummy_inventory_instance)
        self.dummy_inventory_model.objects.get.assert_called_once_with(part_type="KANAT", aircraft_id=1)

    def test_find_inventory_by_aircraft_id_and_part_type_returns_message_when_not_found(self):
        self.dummy_inventory_model.objects.get.side_effect = self.dummy_inventory_model.DoesNotExist
        result = self.inventory_service.find_inventory_by_aircraft_id_and_part_id(1, "KANAT")
        self.assertEqual(result, "Inventory could not found")

if __name__ == '__main__':
    unittest.main()