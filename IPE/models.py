from django.db import models

# Create your models here.
class LimitsIPE(models.Model):
    date = models.DateTimeField(null=True, blank=True, verbose_name="Дата создания")
    
    cash        = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Готівка")
    card        = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Карта")
    PrivatBank  = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="безг.PrivatBank")
    NovaPay     = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Безг.NovaPay")

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

class LimitsMonthIPE(models.Model):
    date = models.DateTimeField(null=True, blank=True, verbose_name="Дата создания")

    

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)