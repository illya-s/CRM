import requests, config, os, datetime
from django.db import models
import xml.etree.ElementTree as ET


def sup_upload_to(instance, filename):
    return os.path.join('suppliers', f"{instance.pk}_{datetime.datetime.now().strftime("%d_%m_%y")}", filename)

class Supplier(models.Model):
    name = models.CharField(max_length=500, blank=False, null=True, verbose_name="Название")
    logo = models.ImageField(upload_to=sup_upload_to, blank=True, null=True)

    import_url = models.URLField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    def fetch_data(self):
        if not self.import_url:
            return None

        root = ET.Element("items")
        response = requests.get(self.import_url, headers=config.firefox_mask)

        if response.status_code == 200:
            items = ET.fromstring(response.content).find("items").findall("item")
            root.extend(items)
            return root
        else:
            return None



def myp_upload_to(instance, filename):
    return os.path.join('my_products', f"{instance.pk}_{datetime.datetime.now().strftime("%d_%m_%y")}", filename)

# class MyProduct(models.Model):
#     article = models.CharField(max_length=250, blank=True, null=True, verbose_name="Артикул")
#     name = models.CharField(max_length=500, blank=False, null=True, verbose_name="Название")

#     price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Цена")
#     image = models.ImageField(upload_to=myp_upload_to, blank=True, null=True)

#     created = models.DateTimeField(auto_now_add=True, null=True)
#     updated = models.DateTimeField(auto_now=True, null=True)

#     def __str__(self):
#         return self.name



class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplier_products')

    article = models.CharField(max_length=250, blank=True, null=True, verbose_name="Артикул")
    name = models.CharField(max_length=500, blank=False, null=True, verbose_name="Название")

    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Цена")
    image = models.URLField(blank=True, null=True)

    url   = models.URLField(null=True, blank=True, verbose_name="Ссылка на товар")

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class ProductAvailability(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True, related_name='products_availability')

class ProductAvailabilityAmount(models.Model):
    spa = models.ForeignKey(ProductAvailability, on_delete=models.CASCADE, null=True, related_name='products_amount')

    size   = models.CharField(max_length=500, blank=False, null=True, verbose_name="Размер")
    amount = models.PositiveIntegerField(null=True, blank=False, verbose_name="Количество")