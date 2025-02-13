from production.models import Team


class TeamService:
    def __init__(self, team_model = Team):
        self.team_model = team_model

    def find_team_by_name(self, team_name):
        return self.team_model.objects.get(name=team_name)

    def find_team_by_id(self, team_id):
        team = self.team_model.objects.get(id=team_id)
        return team

    def create_team(self, team_name):
        teams = self.team_model.objects.all()
        if team_name in [team.name for team in teams]:
            raise Exception('Team already exists')
        team = self.team_model.objects.create(name=team_name)
        return team