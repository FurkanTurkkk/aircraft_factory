from production.models import Team
from production.exceptions.custom_exception import BusinessException


class TeamService:
    def __init__(self, team_model=Team):
        # Hangi model üzerinde işlem yapılacağı belirlenir (bağımlılık enjeksiyonu kolaylaşır).
        self.team_model = team_model

    def find_team_by_name(self, team_name):
        """
        Verilen isimdeki takımı getirir.
        Eğer takım bulunamazsa BusinessException fırlatır.
        """
        try:
            return self.team_model.objects.get(name=team_name)
        except self.team_model.DoesNotExist:
            raise BusinessException(f"Team with name '{team_name}' does not exist.")

    def find_team_by_id(self, team_id):
        """
        Verilen ID'ye sahip takımı getirir.
        Eğer takım bulunamazsa BusinessException fırlatır.
        """
        try:
            return self.team_model.objects.get(id=team_id)
        except self.team_model.DoesNotExist:
            raise BusinessException(f"Team with id '{team_id}' does not exist.")

    def create_team(self, team_name):
        """
        Yeni bir takım oluşturur. Aynı isimde bir takım varsa BusinessException fırlatır.
        """
        if self.team_model.objects.filter(name=team_name).exists():
            raise BusinessException("Team already exists.")

        team = self.team_model.objects.create(name=team_name)
        return team
