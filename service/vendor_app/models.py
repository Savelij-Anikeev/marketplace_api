from django.db import models


class Vendor(models.Model):
    name = models.CharField(max_length=128)
    photo = models.ImageField(null=True, blank=True)
    rating = models.FloatField(default=0)  # add validator

    def __str__(self):
        return self.name
