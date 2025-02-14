from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

from production.exceptions.custom_exception import BusinessException
from production.models import Personnel
from production.services.team_service import TeamService


class PersonnelService:
    def __init__(self, personnel_model = Personnel, service_team = TeamService()):
        self.personnel_model = personnel_model
        self.team_service = service_team

    def register(self,username,password,email,team_id):
        allowed_teams = ['KANAT TAKIMI','GOVDE TAKIMI','AVIYONIK TAKIMI','KUYRUK TAKIMI','MONTAJ TAKIMI']
        team = self.team_service.find_team_by_id(team_id)
        team_name = team.name
        if team_name not in allowed_teams:
            raise ValueError('Invalid team name'+", Valid team names are: "+', '.join(allowed_teams))
        user = self.personnel_model.objects.create(username=username,email=email,team=team)
        user.set_password(password)
        user.save()
        return user

    def login(self,username,password,request):
        user = authenticate(username=username, password=password)
        if user is None:
            raise BusinessException('Invalid username or password')
        login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return user,access_token

    def update_personnel(self,user,**kwargs):
        if 'password' in kwargs:
            user.set_password(kwargs.pop('password'))
        for key, value in kwargs.items():
            setattr(user,key,value)
        user.save()
        return user