# master/models/city.py

from django.db import models
from master.models.country import Country
from master.models.state import State
from utils.basemodel import BaseModel

class City(BaseModel):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL, related_name='cities')
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL, related_name='cities')
    name = models.CharField(max_length=40, blank=True, null=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, default=0)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, default=0)
    location_url = models.URLField(blank=True, null=True)
    phonecode = models.IntegerField(default=0)
    population = models.BigIntegerField(default=0)
    timezone = models.CharField(max_length=20, blank=True, null=True)
    founded_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)

    class Meta:
        db_table = '"master"."cities"'
        indexes = [
            models.Index(fields=['name']),              
            models.Index(fields=['status', 'is_active']), 
            models.Index(fields=['country_id']),           
            models.Index(fields=['state_id']),
        ]

    def __str__(self):
        return self.name