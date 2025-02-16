from production.services.team_service import TeamService
import unittest
from django.test import TestCase
from production.models import Team
from production.exceptions.custom_exception import BusinessException



class TeamServiceTest(TestCase):
    def setUp(self):
        self.team_service = TeamService(team_model=Team)
        self.existing_team = Team.objects.create(name="ExistingTeam")

    def test_find_team_by_name_returns_correct_team_object_when_team_exists(self):
        found_team = self.team_service.find_team_by_name("ExistingTeam")
        self.assertEqual(found_team.id, self.existing_team.id)
        self.assertEqual(found_team.name, "ExistingTeam")

    def test_find_team_by_name_raises_business_exception_when_team_does_not_exist(self):
        with self.assertRaises(BusinessException) as context:
            self.team_service.find_team_by_name("NonExistentTeam")
        self.assertIn("Team with name 'NonExistentTeam' does not exist.", str(context.exception))

    def test_find_team_by_id_returns_correct_team_object_when_team_exists(self):
        found_team = self.team_service.find_team_by_id(self.existing_team.id)
        self.assertEqual(found_team.name, "ExistingTeam")

    def test_find_team_by_id_raises_business_exception_when_team_does_not_exist(self):
        non_existent_id = self.existing_team.id + 1
        with self.assertRaises(BusinessException) as context:
            self.team_service.find_team_by_id(non_existent_id)
        self.assertIn(f"Team with id '{non_existent_id}' does not exist.", str(context.exception))

    def test_create_team_creates_and_returns_new_team_object_when_team_does_not_already_exist(self):
        new_team = self.team_service.create_team("NewTeam")
        self.assertIsNotNone(new_team.id)
        self.assertEqual(new_team.name, "NewTeam")
        team_from_db = Team.objects.get(name="NewTeam")
        self.assertEqual(new_team.id, team_from_db.id)

    def test_create_team_raises_business_exception_when_team_already_exists(self):
        with self.assertRaises(BusinessException) as context:
            self.team_service.create_team("ExistingTeam")
        self.assertIn("Team already exists.", str(context.exception))

if __name__ == '__main__':
    unittest.main()