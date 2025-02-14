from django.db import models
from django.contrib.auth.models import AbstractUser

class Team(models.Model):
    TEAM_CHOICES = [
        ('KANAT TAKIMI','KANAT TAKIMI'),
        ('GOVDE TAKIMI','GOVDE TAKIMI'),
        ('KUYRUK TAKIMI','KUYRUK TAKIMI'),
        ('AVIYONIK TAKIMI','AVIYONIK TAKIMI'),
        ('MONTAJ TAKIMI','MONTAJ TAKIMI'),
    ]

    name = models.CharField(max_length=50,choices=TEAM_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Personnel(AbstractUser):
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='personnels',null=True,blank=True)

    def __str__(self):
        return self.username

class Aircraft(models.Model):
    AIRCRAFT_TYPE = [
        ('TB2','TB2'),
        ('TB3','TB3'),
        ('AKINCI','AKINCI'),
        ('KIZILELMA','KIZILELMA')
    ]
    type = models.CharField(max_length=20,choices=AIRCRAFT_TYPE)
    assembly_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.type}-{self.id}"

class Part(models.Model):
    PART_TYPE = [
        ('KANAT','KANAT'),
        ('GOVDE','GOVDE'),
        ('KUYRUK','KUYRUK'),
        ('AVIYONIK','AVIYONIK')
    ]
    
    AIRPLANE_TYPE = [
        ('TB2','TB2'),
        ('TB3','TB3'),
        ('AKINCI','AKINCI'),
        ('KIZILELMA','KIZILELMA')
    ]

    part_type = models.CharField(max_length=20,choices=PART_TYPE)
    airplane_type_of_part = models.CharField(max_length=20, choices=AIRPLANE_TYPE, default='')
    stock = models.PositiveBigIntegerField(default=0)
    aircraft = models.ForeignKey(Aircraft,on_delete=models.CASCADE,related_name='parts',null=True,blank=True)
    added_by = models.ForeignKey(Personnel,on_delete=models.CASCADE,related_name='added_parts')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['part_type','airplane_type_of_part'],name='unique_part') # For unique part with part of aircraft
        ]
    

    def __str__(self):
        return f"{self.get_part_type_display()} - Stock: {self.stock}"
    
    def increase_stock(self,quantity):
        self.stock += quantity
        self.save()
    
    def decrease_stock(self,quantity):
        if self.stock < quantity:
            raise ValueError("Stok sayısı sıfır(0) ın altına inemez!")
        self.stock -= quantity
        self.save()
        if self.stock == 0:
            print(f"UYARI: {self.get_part_type_display()} stoğu bitti!")

class AssemblyRegistration(models.Model):
    aircraft = models.ForeignKey(Aircraft,on_delete=models.CASCADE,related_name='assembly_registration')
    parts_used = models.ManyToManyField(Part,related_name='assembly_registration')
    assembler = models.ForeignKey(Personnel,on_delete=models.CASCADE,related_name='assembly_transactions')
    assembly_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assembly registration {self.id} - Aircraft: {self.aircraft.type}"

