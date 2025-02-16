from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Team, Part, Aircraft, Assembly, AssemblyItem, ManufacturedAircraft, Inventory

User = get_user_model()


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']


class PersonnelSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source='team', write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'team', 'team_id']


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['id', 'type']


class PartSerializer(serializers.ModelSerializer):
    aircraft = AircraftSerializer(read_only=True)

    class Meta:
        model = Part
        fields = ['id', 'type', 'aircraft']


class InventorySerializer(serializers.ModelSerializer):
    aircraft = AircraftSerializer(read_only=True)
    part = PartSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'aircraft', 'part', 'quantity']


class AssemblySerializer(serializers.ModelSerializer):
    aircraft = AircraftSerializer(read_only=True)

    class Meta:
        model = Assembly
        fields = ['id', 'aircraft']


class AssemblyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssemblyItem
        fields = ['id', 'assembly', 'item', 'quantity']


class AssemblyItemRequestSerializer(serializers.Serializer):
    part_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class AssemblyRequestSerializer(serializers.Serializer):
    aircraft_id = serializers.IntegerField()
    items = serializers.ListField(child=AssemblyItemRequestSerializer())


class ManufacturedAircraftSerializer(serializers.ModelSerializer):
    aircraft = AircraftSerializer(read_only=True)

    class Meta:
        model = ManufacturedAircraft
        fields = ['id', 'aircraft', 'created_at']
