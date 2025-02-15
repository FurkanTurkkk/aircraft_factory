from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from production.services.personnel_service import PersonnelService
from production.services.team_service import TeamService
from production.exceptions.custom_exception import BusinessException

User = get_user_model()

class PersonnelServiceTest(TestCase):
    def setUp(self):
        self.team_service = TeamService()
        self.personnel_service = PersonnelService(service_team=self.team_service)
        self.team = self.team_service.create_team("MONTAJ TAKIMI")
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'testuser@example.com',
            'team_id': self.team.id
        }
        self.request_factory = RequestFactory()

    def test_register_valid_team(self):
        user = self.personnel_service.register(**self.user_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, self.user_data['username'])

    def test_register_invalid_team(self):
        invalid_team = self.team_service.create_team("GEÇERSİZ TAKIM")
        self.user_data['team_id'] = invalid_team.id
        with self.assertRaises(ValueError):
            self.personnel_service.register(**self.user_data)

    def test_login_valid_credentials(self):
        user = self.personnel_service.register(**self.user_data)
        request = self.request_factory.post('/login/')
        # Manually add session support to the request
        request.session = self.client.session
        authenticated_user, token = self.personnel_service.login(
            username=self.user_data['username'],
            password=self.user_data['password'],
            request=request
        )
        self.assertEqual(authenticated_user, user)
        self.assertIsNotNone(token)

    def test_login_invalid_credentials(self):
        request = self.request_factory.post('/login/')
        with self.assertRaises(BusinessException):
            self.personnel_service.login(
                username='wronguser',
                password='wrongpass',
                request=request
            )
