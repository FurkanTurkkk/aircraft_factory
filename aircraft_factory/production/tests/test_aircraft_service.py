import unittest

from django.test import TestCase
from unittest.mock import MagicMock
from production.exceptions.custom_exception import BusinessException
from production.services.aircraft_service import AircraftService

class AircraftServiceTest(TestCase):
    def setUp(self):
        self.dummy_aircraft_model = MagicMock()
        self.aircraft_service = AircraftService(aircraft=self.dummy_aircraft_model)
        self.dummy_aircraft_instance = MagicMock()

    def test_create_aircraft_success(self):
        self.dummy_aircraft_model.objects.filter.return_value.exists.return_value = False
        self.dummy_aircraft_model.objects.create.return_value = self.dummy_aircraft_instance
        aircraft = self.aircraft_service.create_aircraft("AKINCI")
        self.assertEqual(aircraft, self.dummy_aircraft_instance)
        self.dummy_aircraft_model.objects.filter.assert_called_once_with(type="AKINCI")
        self.dummy_aircraft_model.objects.create.assert_called_once_with(type="AKINCI")

    def test_create_aircraft_raises_exception_when_aircraft_exists(self):
        self.dummy_aircraft_model.objects.filter.return_value.exists.return_value = True
        with self.assertRaises(BusinessException) as context:
            self.aircraft_service.create_aircraft("AKINCI")
        self.assertIn("Aircraft already exists.", str(context.exception))

    def test_get_all_aircraft_returns_list(self):
        dummy_queryset = MagicMock()
        self.dummy_aircraft_model.objects.all.return_value = dummy_queryset
        result = self.aircraft_service.get_all_aircraft()
        self.assertEqual(result, dummy_queryset)

if __name__ == '__main__':
    unittest.main()
