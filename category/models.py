from django.db import models
from django.utils import timezone

# Create your models here.


class Categories (models.Model):
    STATUS_CHOICES = [
        (1 , 'Active'),
        (0, 'Inactive')
    ]
    name = models.CharField(max_length=50, unique=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id}. {self.name}"
    
