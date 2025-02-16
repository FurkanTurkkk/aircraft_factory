import unittest

from django.test import TestCase
from unittest.mock import MagicMock, patch
from production.models import Personnel, Team
from production.exceptions.custom_exception import BusinessException
from production.services.personnel_service import PersonnelService
from production.services.team_service import TeamService


class PersonnelServiceTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="TestTeam")
        self.personnel_service = PersonnelService(personnel_model=Personnel, team_service=TeamService())

    def test_register_creates_and_returns_personnel_user_with_valid_team_id_and_sets_password_hash(self):
        new_user = self.personnel_service.register("testuser", "testpass", "test@example.com", self.team.id)
        self.assertEqual(new_user.username, "testuser")
        self.assertEqual(new_user.email, "test@example.com")
        self.assertEqual(new_user.team.id, self.team.id)
        self.assertTrue(new_user.password)
        self.assertNotEqual(new_user.password, "testpass")

    @patch('production.services.personnel_service.RefreshToken')
    @patch('production.services.personnel_service.login')
    @patch('production.services.personnel_service.authenticate')
    def test_login_returns_personnel_user_and_access_token_when_credentials_are_valid(self, mock_authenticate,
                                                                                      mock_login, mock_RefreshToken):
        dummy_user = MagicMock()
        dummy_user.id = 1
        mock_authenticate.return_value = dummy_user
        dummy_refresh = MagicMock()
        dummy_refresh.access_token = "dummy_token"
        mock_RefreshToken.for_user.return_value = dummy_refresh
        dummy_request = MagicMock()
        user, token = self.personnel_service.login("testuser", "testpass", dummy_request)
        self.assertEqual(user, dummy_user)
        self.assertEqual(token, "dummy_token")
        mock_authenticate.assert_called_once_with(username="testuser", password="testpass")
        mock_login.assert_called_once_with(dummy_request, dummy_user)
        mock_RefreshToken.for_user.assert_called_once_with(dummy_user)

    @patch('production.services.personnel_service.authenticate')
    def test_login_raises_business_exception_when_credentials_are_invalid(self, mock_authenticate):
        mock_authenticate.return_value = None
        dummy_request = MagicMock()
        with self.assertRaises(BusinessException) as context:
            self.personnel_service.login("wronguser", "wrongpass", dummy_request)
        self.assertIn("Invalid username or password", str(context.exception))
        mock_authenticate.assert_called_once_with(username="wronguser", password="wrongpass")


if __name__ == '__main__':
    unittest.main()
