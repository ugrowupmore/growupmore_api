# master/models.py

from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)  # e.g., +91

    def __str__(self):
        return self.name

class State(models.Model):
    country = models.ForeignKey(Country, related_name='states', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('country', 'name')

    def __str__(self):
        return f"{self.name}, {self.country.code}"

class City(models.Model):
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('state', 'name')

    def __str__(self):
        return f"{self.name}, {self.state.name}"
