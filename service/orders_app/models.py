from django.db import models
from django.contrib.auth import get_user_model


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.JSONField()
    is_paid = models.BooleanField(default=False)


class Status(models.Model):
    STATUS_CHOICES = [
        (1, 'В сборке'),
        (2, 'В доставке'),
        (3, 'Доставлен'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='statuses')
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'statuses'
