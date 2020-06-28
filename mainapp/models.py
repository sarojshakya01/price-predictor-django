from django.db import models
from django.contrib.auth.models import User


# class QuoteHistory(models.Model):
#     myid = models.IntegerField(unique=True)
#     req_gallons = models.IntegerField(unique=True)
#     del_address = models.CharField()
#     delivery_date = models.DateTimeField(auto_now=False)
#     sugg_price = models.DecimalField()
#     due_amount = models.DecimalField()
#     updated_on = models.DateTimeField(auto_now=True)
#     created_on = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-created_on']

#     def __str__(self):
#         return self.myid
