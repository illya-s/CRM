from django.db import models

# Create your models here.
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=500, blank=False, null=True, verbose_name="Название")

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.name

class Expense(models.Model):
    expense = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, verbose_name="Категория")

    description = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Описание")

    price   = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Стоимость")

    date    = models.DateTimeField(null=True, blank=True, verbose_name="Дата создания")

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.description