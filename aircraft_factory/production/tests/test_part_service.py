import unittest

from django.test import TestCase
from unittest.mock import MagicMock
from production.services.part_service import PartService
from production.exceptions.custom_exception import BusinessException

class PartServiceTest(TestCase):
    def setUp(self):
        self.dummy_inventory_service = MagicMock()
        self.dummy_part_model = MagicMock()
        self.dummy_part_model.DoesNotExist = Exception
        self.part_service = PartService(part=self.dummy_part_model, inventory_service=self.dummy_inventory_service)
        self.dummy_part = MagicMock()
        self.dummy_part.type = "KANAT"
        self.dummy_part.id = 1

    def test_create_part_returns_created_part_when_permission_valid(self):
        self.dummy_part_model.objects.create.return_value = self.dummy_part
        part = self.part_service.create_part("KANAT", 10, 20, "KANAT TAKIMI")
        self.assertEqual(part, self.dummy_part)
        self.dummy_inventory_service.create_or_update_inventory.assert_called_once_with(10, "KANAT")

    def test_create_part_raises_business_exception_when_permission_invalid(self):
        with self.assertRaises(BusinessException) as context:
            self.part_service.create_part("KANAT", 10, 20, "YANLIŞ TAKIM")
        self.assertIn("Team of user YANLIŞ TAKIM not compatible with part KANAT", str(context.exception))

    def test_find_part_by_id_returns_part_when_exists(self):
        self.dummy_part_model.objects.get.return_value = self.dummy_part
        part = self.part_service.find_part_by_id(1)
        self.assertEqual(part, self.dummy_part)
        self.dummy_part_model.objects.get.assert_called_once_with(id=1)

    def test_find_part_by_id_raises_business_exception_when_not_found(self):
        self.dummy_part_model.objects.get.side_effect = self.dummy_part_model.DoesNotExist
        with self.assertRaises(BusinessException) as context:
            self.part_service.find_part_by_id(99)
        self.assertIn("Part could not found by id: 99", str(context.exception))

    def test_delete_part_by_id_calls_delete_when_permission_valid(self):
        dummy_part_instance = MagicMock()
        dummy_part_instance.type = "KANAT"
        self.dummy_part_model.objects.get.return_value = dummy_part_instance
        self.part_service.delete_part_by_id(1, "KANAT TAKIMI")
        dummy_part_instance.delete.assert_called_once()

    def test_delete_part_by_id_raises_business_exception_when_permission_invalid(self):
        dummy_part_instance = MagicMock()
        dummy_part_instance.type = "KANAT"
        self.dummy_part_model.objects.get.return_value = dummy_part_instance
        with self.assertRaises(BusinessException) as context:
            self.part_service.delete_part_by_id(1, "YANLIŞ TAKIM")
        self.assertIn("Team of user YANLIŞ TAKIM not compatible with part KANAT", str(context.exception))
if __name__ == '__main__':
    unittest.main()
