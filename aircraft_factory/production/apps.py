from django.apps import AppConfig
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_migrate


class ProductionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'production'

    def ready(self):
        post_migrate.connect(create_initial_data, sender=self)


def create_initial_data(sender, **kwargs):
    from production.models import Team, Aircraft, Part, Inventory

    # Team verilerini ekle
    team_choices = [
        ('KANAT TAKIMI', 'KANAT TAKIMI'),
        ('GOVDE TAKIMI', 'GOVDE TAKIMI'),
        ('KUYRUK TAKIMI', 'KUYRUK TAKIMI'),
        ('AVIYONIK TAKIMI', 'AVIYONIK TAKIMI'),
        ('MONTAJ TAKIMI', 'MONTAJ TAKIMI'),
    ]
    for code, name in team_choices:
        Team.objects.get_or_create(name=name)

    # Aircraft verilerini ekle
    aircraft_types = [
        ('TB2', 'TB2'),
        ('TB3', 'TB3'),
        ('AKINCI', 'AKINCI'),
        ('KIZILELMA', 'KIZILELMA')
    ]
    for code, name in aircraft_types:
        Aircraft.objects.get_or_create(type=name)

    # Part verilerini ekle
    part_types = [
        ('KANAT', 'KANAT'),
        ('GOVDE', 'GOVDE'),
        ('KUYRUK', 'KUYRUK'),
        ('AVIYONIK', 'AVIYONIK')
    ]

    for aircraft_type, _ in aircraft_types:
        aircraft = Aircraft.objects.get(type=aircraft_type)
        for part_type, _ in part_types:
            try:
                team = Team.objects.get(name=f"{part_type} TAKIMI")  # Part eklerken uygun takımı bul
                part, created = Part.objects.get_or_create(aircraft=aircraft, type=part_type, team=team)
                Inventory.objects.get_or_create(aircraft=aircraft, part=part, defaults={'quantity': 0})
            except ObjectDoesNotExist:
                continue