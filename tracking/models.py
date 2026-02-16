from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True) 

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('GOVERNOR', 'Governor'),
        ('EXECUTIVE', 'Executive'),
        ('HEAD', 'Department Head'),
        ('STAFF', 'Department Staff'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"