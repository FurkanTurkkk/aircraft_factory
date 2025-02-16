from django.contrib.auth.models import AbstractUser
from django.db import models


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

    class Meta:
        unique_together = ('aircraft', 'type')


class Inventory(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=0)

    class Meta:
        unique_together = ('aircraft', 'part')


class Assembly(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    creator = models.ForeignKey(Personnel, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)


class AssemblyItem(models.Model):
    assembly = models.ForeignKey(Assembly, on_delete=models.CASCADE)
    item = models.ForeignKey(Part, on_delete=models.DO_NOTHING)
    quantity = models.PositiveBigIntegerField(default=0)


class ManufacturedAircraft(models.Model):
    assembly = models.ForeignKey(Assembly, on_delete=models.CASCADE)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
