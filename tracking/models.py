# tracking/models.py
from django.db import models
from django.contrib.auth.models import User
from .choices import OFFICE_CHOICES, OFFICE_DICT, STATUS_CHOICES

class Office(models.Model):
    office_code = models.CharField(max_length=50, choices=OFFICE_CHOICES, unique=True)
    office_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.office_name
    
    class Meta:
        ordering = ['office_name']

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('HEAD', 'Department Head'),
        ('STAFF', 'Staff'),
        ('GOVERNOR', 'Governor'),
        ('EXECUTIVE', 'Executive'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STAFF')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Document(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('FOR_REVIEW', 'For Review'),
        ('COMPLETED', 'Completed'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    def __str__(self):
        return self.title

class Routing(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='routings')
    from_office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, related_name='routings_from')
    to_office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, related_name='routings_to')
    routed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')