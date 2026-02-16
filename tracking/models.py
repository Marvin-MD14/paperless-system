from django.db import models
from django.contrib.auth.models import User

# Maps to 'Office' in your ERD
class Office(models.Model):
    office_name = models.CharField(max_length=150, unique=True)
    # Self-reference for parent offices/departments
    parent_office = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_offices')

    def __str__(self):
        return self.office_name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('GOVERNOR', 'Governor'),
        ('EXECUTIVE', 'Executive'),
        ('HEAD', 'Department Head'),
        ('STAFF', 'Department Staff'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Document(models.Model):
    title = models.CharField(max_length=255)
    content_ocr = models.TextField(null=True, blank=True)
    file_hash = models.CharField(max_length=64, unique=True)
    
    # Tracking ownership
    origin_office = models.ForeignKey(Office, on_delete=models.PROTECT, related_name='originated_documents')
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_documents')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=50, default='PENDING')

    def __str__(self):
        return self.title

class DocumentRouting(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='routings')
    from_office = models.ForeignKey(Office, on_delete=models.PROTECT, related_name='sent_routings')
    to_office = models.ForeignKey(Office, on_delete=models.PROTECT, related_name='received_routings')
    
    routed_by = models.ForeignKey(User, on_delete=models.PROTECT)
    routed_at = models.DateTimeField(auto_now_add=True)
    
    remarks = models.TextField(blank=True)
    is_final = models.BooleanField(default=False)

    class Meta:
        ordering = ['-routed_at']