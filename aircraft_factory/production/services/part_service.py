from production.exceptions.custom_exception import BusinessException
from production.models import Part


class PartService:
    def __init__(self, part=Part):
        self.part = part

    def create_part(self, type, aircraft_id, team_id, team_name):

        self._check_permission(type, team_name)
        part = self.part.objects.create(type=type, aircraft_id=aircraft_id, team_id=team_id)
        return part

    def find_part_by_id(self, part_id):
        try:
            return self.part.objects.get(id=part_id)
        except self.part.DoesNotExist:
            raise BusinessException(f"Part could not found by id: {part_id}")

    def delete_part_by_id(self, part_id, user_team):
        part = self.find_part_by_id(part_id)
        self._check_permission(part.type, user_team)
        part.delete()

    def find_parts_by_team(self, team_id):
        return self.part.objects.filter(team_id=team_id)

    def _check_permission(self, type, team_name):
        team_mapping = {
            'KANAT': 'KANAT TAKIMI',
            'GOVDE': 'GOVDE TAKIMI',
            'KUYRUK': 'KUYRUK TAKIMI',
            'AVIYONIK': 'AVIYONIK TAKIMI'
        }
        expected_team = team_mapping.get(type)
        if not expected_team or team_name != expected_team:
            raise BusinessException(f"Team of user {team_name} not compatible with part {type}")
