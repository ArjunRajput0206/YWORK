from django.db import models
import datetime

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=100)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.IntegerField()  # 1–12
    year = models.IntegerField()
    leave_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ("employee", "month", "year")

    def __str__(self):
        return f"{self.employee.name} - {self.month}/{self.year}"
