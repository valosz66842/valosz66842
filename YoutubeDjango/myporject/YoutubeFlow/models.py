from django.db import models

# # Create your models here.
# class App1(models.Model):
#     title = models.CharField(max_length=100)
#
#     category = models.CharField(max_length=50, blank=True)
#
#     date_time = models.DateTimeField(auto_now_add=True)
#
#     def __unicode__(self):
#         return self.title
#
#     class Meta:
#         ordering = ['-date_time']
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now


