from django.contrib.auth.models import AbstractUser
from django.db import models

from vendor_app.models import Vendor


class User(AbstractUser):
    ROLES = [
        ("default", "default"),
        ("vendor_staff", "vendor_staff"),
        ("vendor_manager", "vendor_manager"),
    ]
    photo = models.ImageField(null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)  # set null=False, it is required
    balance = models.PositiveIntegerField(default=0)

    work_place = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=24, choices=ROLES, default=ROLES[0])
