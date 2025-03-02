from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='units')

    def __str__(self):
        return f"{self.name} ({self.company.name})"


class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='employees')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
