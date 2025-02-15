from production.models import Team
from production.exceptions.custom_exception import BusinessException


class TeamService:
    def __init__(self, team_model=Team):
        self.team_model = team_model

    def find_team_by_name(self, team_name):
        try:
            return self.team_model.objects.get(name=team_name)
        except self.team_model.DoesNotExist:
            raise BusinessException(f"Team with name '{team_name}' does not exist.")

    def find_team_by_id(self, team_id):
        try:
            return self.team_model.objects.get(id=team_id)
        except self.team_model.DoesNotExist:
            raise BusinessException(f"Team with id '{team_id}' does not exist.")

    def create_team(self, team_name):
        if self.team_model.objects.filter(name=team_name).exists():
            raise BusinessException("Team already exists.")

        team = self.team_model.objects.create(name=team_name)
        return team
