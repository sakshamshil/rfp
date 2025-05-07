from django.db import models
from rfpDetails.models import RFP
from vendor.models import Vendor


class Quotes (models.Model):
    rfp = models.ForeignKey(RFP, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    vendors_price = models.IntegerField()
    quantity = models.IntegerField()
    item_description = models.TextField()
    total_cost = models.TextField()

