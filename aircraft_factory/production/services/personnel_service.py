from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

from production.exceptions.custom_exception import BusinessException
from production.models import Personnel
from production.services.team_service import TeamService


class PersonnelService:

    def __init__(self, personnel_model=Personnel, team_service=TeamService()):
        self.personnel = personnel_model
        self.team_service = team_service

    def register(self, username, password, email, team_id):
        team = self.team_service.find_team_by_id(team_id)
        user = self.personnel.objects.create(username=username, email=email, team=team)
        user.set_password(password)  # For hash
        user.save()
        return user

    def login(self, username, password, request):
        user = authenticate(username=username, password=password)
        if user is None:
            raise BusinessException('Invalid username or password')
        login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return user, access_token
