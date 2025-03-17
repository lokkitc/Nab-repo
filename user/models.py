from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings
from product.models import Product
import uuid
# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    money = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)  

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('user:profile', args=[self.id])
