from django.test import TestCase
from production.models import Team
from production.exceptions.custom_exception import BusinessException
from production.services.team_service import TeamService

class TeamServiceTest(TestCase):
    def setUp(self):
        self.team_service = TeamService(team_model=Team)

    def test_find_team_by_name_success(self):
        team = Team.objects.create(name="KANAT TAKIMI")
        found_team = self.team_service.find_team_by_name("KANAT TAKIMI")
        self.assertEqual(found_team.id, team.id)

    def test_find_team_by_name_not_found(self):
        with self.assertRaises(BusinessException) as context:
            self.team_service.find_team_by_name("NONEXISTENT TEAM")
        self.assertIn("Team with name", str(context.exception))

    def test_find_team_by_id_success(self):
        team = Team.objects.create(name="GOVDE TAKIMI")
        found_team = self.team_service.find_team_by_id(team.id)
        self.assertEqual(found_team.name, team.name)

    def test_find_team_by_id_not_found(self):
        with self.assertRaises(BusinessException) as context:
            self.team_service.find_team_by_id(9999)
        self.assertIn("Team with id", str(context.exception))

    def test_create_team_success(self):
        team = self.team_service.create_team("KUYRUK TAKIMI")
        self.assertEqual(team.name, "KUYRUK TAKIMI")
        self.assertTrue(Team.objects.filter(name="KUYRUK TAKIMI").exists())

    def test_create_team_already_exists(self):
        Team.objects.create(name="AVIYONIK TAKIMI")
        with self.assertRaises(BusinessException) as context:
            self.team_service.create_team("AVIYONIK TAKIMI")
        self.assertIn("Team already exists", str(context.exception))

if __name__ == '__main__':
    import unittest
    unittest.main()

