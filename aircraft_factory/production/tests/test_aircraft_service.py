import unittest
from unittest.mock import MagicMock, patch
from django.test import TestCase
from production.models import Aircraft, AssemblyRegistration, Personnel, Team, Part
from production.exceptions.custom_exception import BusinessException
from production.services.aircraft_service import AircraftService


class AircraftServiceTest(TestCase):
    def setUp(self):
        self.montaj_team = Team.objects.create(name="MONTAJ TAKIMI")
        self.non_montaj_team = Team.objects.create(name="KANAT TAKIMI")

        self.assembler = Personnel.objects.create(username="assembler", team=self.montaj_team)
        self.user = Personnel.objects.create(username="montaj_user", team=self.montaj_team)
        self.non_montaj_user = Personnel.objects.create(username="other_user", team=self.non_montaj_team)
        self.aircraft = Aircraft.objects.create(type="AKINCI", quantity=10)

        self.part = Part.objects.create(
            part_type="MONTAJ",
            airplane_type_of_part=self.aircraft.type,
            stock=100,
            aircraft=self.aircraft,
            added_by=self.assembler
        )
        self.dummy_part_service = MagicMock()
        self.dummy_part_service.find_part_by_id.return_value = self.part
        self.dummy_part_service.decrease_stock_of_part.return_value = (
        self.part, "Part quantity decreased successfully...")

        self.aircraft_service = AircraftService(
            aircraft=Aircraft,
            assembly_registration=AssemblyRegistration,
            part_service=self.dummy_part_service
        )

    def test_find_aircraft_by_id_success(self):
        found_aircraft = self.aircraft_service.find_aircraft_by_id(self.aircraft.id)
        self.assertEqual(found_aircraft.id, self.aircraft.id)

    def test_find_aircraft_by_id_not_found(self):
        with self.assertRaises(BusinessException) as context:
            self.aircraft_service.find_aircraft_by_id(9999)
        self.assertIn("Aircraft could not found by id", str(context.exception))

    def test_assemble_aircraft_success(self):
        parts_list = [{"part_id": self.part.id, "quantity": 5}]
        registration = self.aircraft_service.assemble_aircraft(self.assembler, self.aircraft.id, parts_list)

        self.assertEqual(registration.aircraft.id, self.aircraft.id)
        self.assertEqual(registration.assembler.id, self.assembler.id)

        self.assertIn(self.part, registration.parts_used.all())

        self.dummy_part_service.decrease_stock_of_part.assert_called_with(self.part.id, 5)

    def test_assemble_aircraft_invalid_assembler(self):
        with self.assertRaises(BusinessException) as context:
            self.aircraft_service.assemble_aircraft(self.non_montaj_user, self.aircraft.id, [])
        self.assertIn("Aircraft could not assemble by this assembler", str(context.exception))

    def test_create_aircraft_permission_denied(self):
        with self.assertRaises(BusinessException) as context:
            self.aircraft_service.create_aircraft(self.non_montaj_user, {"type": "AKINCI", "quantity": 5})
        self.assertIn("Sadece Montaj Takımı uçak oluşturabilir", str(context.exception))

    def test_create_aircraft_missing_type(self):
        with self.assertRaises(BusinessException) as context:
            self.aircraft_service.create_aircraft(self.user, {"quantity": 5})
        self.assertIn("Uçak tipi gereklidir", str(context.exception))

    def test_create_aircraft_update_existing(self):
        initial_quantity = self.aircraft.quantity
        updated_aircraft = self.aircraft_service.create_aircraft(self.user, {"type": "AKINCI", "quantity": 5})
        self.assertEqual(updated_aircraft.id, self.aircraft.id)
        self.assertEqual(updated_aircraft.quantity, initial_quantity + 5)

    def test_create_aircraft_new_creation(self):
        new_aircraft = self.aircraft_service.create_aircraft(self.user, {"type": "TB2", "quantity": 3})
        self.assertEqual(new_aircraft.type, "TB2")
        self.assertEqual(new_aircraft.quantity, 3)

    def test_get_all_aircraft_success(self):
        aircraft2 = Aircraft.objects.create(type="TB3", quantity=5)
        aircraft3 = Aircraft.objects.create(type="KIZILELMA", quantity=2)
        all_aircraft = self.aircraft_service.get_all_aircraft()
        ids = [ac.id for ac in all_aircraft]
        self.assertEqual(ids, sorted(ids))
        self.assertGreaterEqual(len(all_aircraft), 3)

    def test_get_all_aircraft_error(self):
        with patch('production.models.Aircraft.objects.all') as all_patch:
            all_patch.side_effect = Exception("Test exception")
            with self.assertRaises(BusinessException) as context:
                self.aircraft_service.get_all_aircraft()
            self.assertIn("Something went wrong", str(context.exception))


if __name__ == '__main__':
    import unittest

    unittest.main()
