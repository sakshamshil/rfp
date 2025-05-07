from django.db import models
from category.models import Categories
from vendor.models import Vendor
from django.core.validators import MinValueValidator



class RFP (models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('close', 'Close')
    ]

    title = models.CharField(max_length=100)
    item_description = models.TextField()
    quantity = models.PositiveIntegerField()
    last_date = models.DateTimeField()
    minimum_price = models.FloatField(validators=[MinValueValidator(0.0)])
    maximum_price = models.FloatField(validators=[MinValueValidator(0.0)])
    categories = models.ManyToManyField(Categories)
    vendors = models.ManyToManyField(Vendor)
    rfp_no = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='open')
    

    def __str__(self):
        return f"{self.id}. {self.title}"