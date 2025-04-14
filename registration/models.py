# registration/models.py
from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    hours_per_week = models.FloatField()
    hourly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"