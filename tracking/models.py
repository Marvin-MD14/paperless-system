import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .choices import OFFICE_CHOICES, OFFICE_DICT, STATUS_CHOICES, ROLE_CHOICES, REGISTRATION_TYPES

# --- OFFICE MODEL ---
class Office(models.Model):
    office_code = models.CharField(max_length=50, choices=OFFICE_CHOICES, unique=True)
    office_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.office_name
    
    class Meta:
        ordering = ['office_name']

# --- USER PROFILE MODEL ---
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STAFF')
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_users')
    
    registration_type = models.CharField(
        max_length=20,
        choices=REGISTRATION_TYPES,
        default='ADMIN',
        help_text="How was this user account created?"
    )
    
    registered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

# --- DOCUMENT MODEL ---
class Document(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('FOR_REVIEW', 'For Review'),
        ('COMPLETED', 'Completed'),
    )
    
    CATEGORY_CHOICES = [
        ('word', 'Microsoft Word'),
        ('excel', 'Microsoft Excel'),
        ('ppt', 'PowerPoint'),
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, help_text="Comment from the sender/uploader")
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents')
    
    recipient = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='received_documents'
    )
    is_read = models.BooleanField(default=False)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='pdf')
    
    # NEW FIELD: Ito ang mag-iimbak ng feedback/comment mula sa Receiver (Approved/Rejected note)
    remarks = models.TextField(blank=True, null=True, help_text="Feedback or reason from the receiver")

    def save(self, *args, **kwargs):
        if self.file:
            ext = os.path.splitext(self.file.name)[1].lower()
            if ext in ['.doc', '.docx']:
                self.category = 'word'
            elif ext in ['.xls', '.xlsx', '.csv']:
                self.category = 'excel'
            elif ext in ['.ppt', '.pptx']:
                self.category = 'ppt'
            elif ext in ['.pdf']:
                self.category = 'pdf'
            elif ext in ['.jpg', '.jpeg', '.png', '.gif']:
                self.category = 'image'
            else:
                self.category = 'other'
        super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

# --- ROUTING MODEL ---
class Routing(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='routings')
    from_office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, related_name='routings_from')
    to_office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, related_name='routings_to')
    routed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Document.STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Route for {self.document.title}"

# --- NOTIFICATION MODEL ---
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('NEW_DOC', 'New Document Received'),
        ('APPROVE', 'Document Approved'),
        ('REJECT', 'Document Rejected/Returned'),
        ('SYSTEM', 'System Message'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    document = models.ForeignKey('Document', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='NEW_DOC')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.notification_type}"

    class Meta:
        ordering = ['-created_at']

# --- SIGNALS ---
@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        UserProfile.objects.get_or_create(user=instance)