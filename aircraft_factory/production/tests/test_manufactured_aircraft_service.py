import unittest

from django.test import TestCase
from unittest.mock import MagicMock
from production.services.manufactured_aircraft_service import ManufacturedAircraftService
from production.exceptions.custom_exception import BusinessException

class ManufacturedAircraftServiceTest(TestCase):
    def setUp(self):
        self.dummy_manufactured_aircraft_model = MagicMock()
        self.service = ManufacturedAircraftService(manufactured_aircraft=self.dummy_manufactured_aircraft_model)
        self.dummy_manufactured_aircraft_instance = MagicMock()

    def test_add_manufactured_aircraft_creates_and_returns_object(self):
        self.dummy_manufactured_aircraft_model.objects.create.return_value = self.dummy_manufactured_aircraft_instance
        assembly = "assembly1"
        aircraft = "aircraft1"
        result = self.service.add_manufactured_aircraft(assembly, aircraft)
        self.assertEqual(result, self.dummy_manufactured_aircraft_instance)
        self.dummy_manufactured_aircraft_model.objects.create.assert_called_once_with(assembly=assembly, aircraft=aircraft)

    def test_list_of_all_manufactured_aircraft_returns_all_objects_when_team_name_is_montaj_takimi(self):
        dummy_queryset = MagicMock()
        self.dummy_manufactured_aircraft_model.objects.all.return_value = dummy_queryset
        result = self.service.list_of_all_manufactured_aircraft("MONTAJ TAKIMI")
        self.assertEqual(result, dummy_queryset)

    def test_list_of_all_manufactured_aircraft_raises_business_exception_when_team_name_is_not_montaj_takimi(self):
        with self.assertRaises(BusinessException) as context:
            self.service.list_of_all_manufactured_aircraft("YANLIŞ TAKIM")
        self.assertIn("Members of YANLIŞ TAKIM can not list of manufactured aircraft", str(context.exception))

if __name__ == '__main__':
    unittest.main()