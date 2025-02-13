from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Team, Part, Aircraft, AssemblyRegistration

User = get_user_model()

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id','name']

class PersonnelSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source='team',write_only=True)

    class Meta:
        model = User
        fields = ['id','username','password','email','team','team_id']
        extra_kwargs = {'password':{'write_only' : True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ['id','part_type','variant_type','stock','aircraft','added_by']
    
class AircraftSerializer(serializers.ModelSerializer):
    parts = PartSerializer(many=True,read_only=True)

    class Meta:
        model = Aircraft
        fields = ['id','type','assembly_date','parts']

class AssemblyRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssemblyRegistration
        fields = ['id','aircraft','parts_used','assembler','assembly_date']
