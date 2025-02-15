import unittest
from django.test import TestCase
from unittest.mock import MagicMock, patch
from production.models import Part, Aircraft, Personnel, Team
from production.exceptions.custom_exception import BusinessException
from production.services.part_service import PartService


class DummyTeam:
    def __init__(self, team_name):
        self.name = team_name


class DummyUser:
    def __init__(self, team_name):
        self.team = DummyTeam(team_name)


class PartServiceTest(TestCase):

    def setUp(self):
        self.dummy_aircraft = Aircraft.objects.create(type="A320", quantity=1)

        team = Team.objects.create(name="MONTAJ TAKIMI")
        self.dummy_personnel = Personnel.objects.create(username="dummy_user", team=team)
        self.aircraft_service_mock = MagicMock()
        self.aircraft_service_mock.find_aircraft_by_id.return_value = self.dummy_aircraft
        self.part_service = PartService(aircraft_service=self.aircraft_service_mock)

    def test_init_without_aircraft_service_raises_exception(self):
        with self.assertRaises(BusinessException):
            PartService(aircraft_service=None)

    def test_create_part_success_created(self):
        dummy_user = DummyUser(team_name="A320")
        part_type = "A320-Part"
        stock = 10
        aircraft_id = self.dummy_aircraft.id
        airplane_type_of_part = "A320"

        # get_or_create metodu yeni bir nesne oluşturduğunu simüle ediyoruz.
        with patch('production.models.Part.objects.get_or_create') as get_or_create_mock:
            get_or_create_mock.return_value = (Part(), True)
            part, message = self.part_service.create_part(
                added_by=dummy_user,
                part_type=part_type,
                stock=stock,
                aircraft_id=aircraft_id,
                airplane_type_of_part=airplane_type_of_part
            )
            self.assertEqual(message, "Part created successfully...")
            get_or_create_mock.assert_called_once()

    def test_create_part_success_update(self):
        dummy_user = DummyUser(team_name="MONTAJ TAKIMI")
        part_type = "MONTAJ"
        stock = 5
        aircraft_id = self.dummy_aircraft.id
        airplane_type_of_part = "A320"
        existing_part = Part(
            stock=10,
            aircraft=self.dummy_aircraft,
            added_by=self.dummy_personnel,
            part_type=part_type,
            airplane_type_of_part=airplane_type_of_part
        )

        with patch('production.models.Part.objects.get_or_create') as get_or_create_mock:
            get_or_create_mock.return_value = (existing_part, False)
            existing_part.increase_stock = MagicMock()
            part, message = self.part_service.create_part(
                added_by=dummy_user,
                part_type=part_type,
                stock=stock,
                aircraft_id=aircraft_id,
                airplane_type_of_part=airplane_type_of_part
            )
            existing_part.increase_stock.assert_called_once_with(quantity=stock)
            self.assertEqual(message, "Part already exist , increasing stock...")
            get_or_create_mock.assert_called_once()

    def test_create_part_permission_denied(self):
        dummy_user = DummyUser(team_name="OTHER")
        part_type = "TAKIMI-Part"
        stock = 10
        aircraft_id = self.dummy_aircraft.id
        airplane_type_of_part = "A320"

        with self.assertRaises(BusinessException) as context:
            self.part_service.create_part(
                added_by=dummy_user,
                part_type=part_type,
                stock=stock,
                aircraft_id=aircraft_id,
                airplane_type_of_part=airplane_type_of_part
            )
        self.assertIn("You do not have permission", str(context.exception))

    def test_create_part_aircraft_not_found(self):
        dummy_user = DummyUser(team_name="TAKIMI")
        part_type = "TAKIMI-Part"
        stock = 10
        aircraft_id = 99  # var olmayan id
        airplane_type_of_part = "A320"
        self.aircraft_service_mock.find_aircraft_by_id.return_value = None

        with self.assertRaises(BusinessException) as context:
            self.part_service.create_part(
                added_by=dummy_user,
                part_type=part_type,
                stock=stock,
                aircraft_id=aircraft_id,
                airplane_type_of_part=airplane_type_of_part
            )
        self.assertIn("Aircraft not found", str(context.exception))

    def test_create_part_aircraft_type_mismatch(self):
        dummy_user = DummyUser(team_name="TAKIMI")
        part_type = "TAKIMI-Part"
        stock = 10
        aircraft_id = self.dummy_aircraft.id
        airplane_type_of_part = "B737"
        with self.assertRaises(BusinessException) as context:
            self.part_service.create_part(
                added_by=dummy_user,
                part_type=part_type,
                stock=stock,
                aircraft_id=aircraft_id,
                airplane_type_of_part=airplane_type_of_part
            )
        self.assertIn("does not belong to", str(context.exception))

    def test_find_part_by_id_success(self):
        part = Part.objects.create(
            part_type="TAKIMI-Part",
            stock=10,
            aircraft=self.dummy_aircraft,
            added_by=self.dummy_personnel
        )
        found_part = self.part_service.find_part_by_id(part.id)
        self.assertEqual(found_part.id, part.id)

    def test_find_part_by_id_not_found(self):
        with self.assertRaises(BusinessException) as context:
            self.part_service.find_part_by_id(9999)
        self.assertIn("Part could not found", str(context.exception))

    def test_increase_stock_of_part_success(self):
        part = Part.objects.create(
            part_type="TAKIMI-Part",
            stock=10,
            aircraft=self.dummy_aircraft,
            added_by=self.dummy_personnel
        )
        with patch('production.models.Part.increase_stock') as increase_stock_mock, \
                patch('production.models.Part.save') as save_mock:
            updated_part, message = self.part_service.increase_stock_of_part(part.id, 5)
            increase_stock_mock.assert_called_once_with(5)
            save_mock.assert_called_once()
            self.assertEqual(message, "Part quantity increased successfully")

    def test_increase_stock_of_part_not_found(self):
        """
        increase_stock_of_part metodu: Var olmayan parça için hata fırlatmalı.
        """
        with self.assertRaises(BusinessException) as context:
            self.part_service.increase_stock_of_part(9999, 5)
        self.assertIn("Part could not found", str(context.exception))

    def test_decrease_stock_of_part_success(self):
        """
        decrease_stock_of_part metodu: Yeterli stok olduğunda düşürme işlemi başarılı.
        """
        part = Part.objects.create(
            part_type="TAKIMI-Part",
            stock=10,
            aircraft=self.dummy_aircraft,
            added_by=self.dummy_personnel
        )
        with patch('production.models.Part.decrease_stock') as decrease_stock_mock, \
                patch('production.models.Part.save') as save_mock:
            updated_part, message = self.part_service.decrease_stock_of_part(part.id, 5)
            decrease_stock_mock.assert_called_once_with(5)
            save_mock.assert_called_once()
            self.assertEqual(message, "Part quantity decreased successfully...")

    def test_decrease_stock_of_part_not_found(self):
        """
        decrease_stock_of_part metodu: Var olmayan parça için hata fırlatmalı.
        """
        with self.assertRaises(BusinessException) as context:
            self.part_service.decrease_stock_of_part(9999, 5)
        self.assertIn("Part could not found", str(context.exception))

    def test_decrease_stock_of_part_insufficient_stock(self):
        """
        decrease_stock_of_part metodu: Yetersiz stok durumunda hata fırlatmalı.
        """
        part = Part.objects.create(
            part_type="TAKIMI-Part",
            stock=3,
            aircraft=self.dummy_aircraft,
            added_by=self.dummy_personnel
        )
        with self.assertRaises(BusinessException) as context:
            self.part_service.decrease_stock_of_part(part.id, 5)
        self.assertIn("don't have enough stock", str(context.exception))


if __name__ == '__main__':
    unittest.main()
