from django.db import models
from django.contrib.auth.models import AbstractUser


class Team(models.Model):
    TEAM_CHOICES = [
        ('KANAT TAKIMI', 'KANAT TAKIMI'),
        ('GOVDE TAKIMI', 'GOVDE TAKIMI'),
        ('KUYRUK TAKIMI', 'KUYRUK TAKIMI'),
        ('AVIYONIK TAKIMI', 'AVIYONIK TAKIMI'),
        ('MONTAJ TAKIMI', 'MONTAJ TAKIMI'),
    ]
    name = models.CharField(max_length=50, choices=TEAM_CHOICES, unique=True)


class Personnel(AbstractUser):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='personnels', null=True, blank=True)


class Aircraft(models.Model):
    AIRCRAFT_TYPE = [
        ('TB2', 'TB2'),
        ('TB3', 'TB3'),
        ('AKINCI', 'AKINCI'),
        ('KIZILELMA', 'KIZILELMA')
    ]
    type = models.CharField(max_length=20, choices=AIRCRAFT_TYPE, unique=True)


class Part(models.Model):
    PART_TYPE = [
        ('KANAT', 'KANAT'),
        ('GOVDE', 'GOVDE'),
        ('KUYRUK', 'KUYRUK'),
        ('AVIYONIK', 'AVIYONIK')
    ]

    type = models.CharField(max_length=20, choices=PART_TYPE)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    creator = models.ForeignKey(Personnel, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)


class Inventory(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE,default=0)
    part_type = models.CharField(max_length=20,default="")
    quantity = models.PositiveBigIntegerField(default=0)

    class Meta:
        unique_together = ('aircraft', 'part_type') # Create inventory database only one registration to same aircraft and part type


class Assembly(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(Personnel, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)


class AssemblyItem(models.Model):
    assembly = models.ForeignKey(Assembly, on_delete=models.CASCADE)
    item = models.ForeignKey(Inventory, on_delete=models.DO_NOTHING,default=0)
    quantity = models.PositiveBigIntegerField(default=0)

class ManufacturedAircraft(models.Model):
    assembly = models.ForeignKey(Assembly, on_delete=models.DO_NOTHING)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
