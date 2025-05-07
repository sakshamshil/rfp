from django.db import models
from rfp.settings import AUTH_USER_MODEL
from category.models import Categories



class Vendor (models.Model):
    APPROVAL_CHOICES = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected')
    ]

    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    approval = models.CharField(max_length=10, choices=APPROVAL_CHOICES, default='pending')
    revenue = models.PositiveIntegerField()
    no_of_employees = models.PositiveIntegerField()
    gst_no = models.CharField(max_length=15)
    pan_no = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=20)
    categories = models.ManyToManyField(Categories)

    def __str__(self):
        return f"uID:{self.user.id} vID:{self.id} {self.user.email}: {self.approval}"