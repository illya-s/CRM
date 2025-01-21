import requests, os, config
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from product.models import *



def upload_to(instance, filename):
    return os.path.join('orders', f"{instance.id}_{instance.created.strftime("%d_%m_%y")}", filename)


def get_ttn_status(ttn:str):
    headers = { 'Content-Type': 'application/json', 'Api-Key': config.api_key }
    data = {
        "modelName": "TrackingDocumentGeneral",
        "calledMethod": "getStatusDocuments",
        "methodProperties": {
            "Documents": [{ "DocumentNumber": ''.join(ttn.split(" ")) }]
        }
    }
    response = requests.get(config.np_url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['data'][0]
    return None
def get_ttn_address(ttn:str):
    ttn = ''.join(ttn.split(" "))
    headers = { 'Content-Type': 'application/json', 'Api-Key': config.api_key }
    data = {
        "modelName": "TrackingDocumentGeneral",
        "calledMethod": "getStatusDocuments",
        "methodProperties": {
            "Documents": [ { "DocumentNumber": ttn } ]
        }
    }
    response = requests.get(config.np_url, json=data, headers=headers)

    return response.json()['data'][0]["WarehouseRecipientAddress"] if response.status_code == 200 else None


class Order(models.Model):
    # WHOSE = {
    #     ("MY", "Мои"),
    #     ("SUP", "Поставщика"),
    # }
    PAYMENTS = [
        ("P", "Передплата"),
        ("S", "Накладений"),
        ("O", "OLX"),
    ]
    inID              = models.IntegerField(null=True, blank=True, verbose_name="Номер заказа")

    product           = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    price             = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="РЦ")
    amount            = models.IntegerField(null=True, blank=False, verbose_name="Количество")

    client_name       = models.CharField(max_length=200, null=True, verbose_name="Введыть Ім'я")
    client_surname    = models.CharField(max_length=200, null=True, verbose_name="Введыть Прізвище")
    client_patronymic = models.CharField(max_length=200, null=True, blank=True, verbose_name="Введыть по-батькові")
    client_phone      = models.CharField(max_length=50, null=True, verbose_name="Телефон")
    client_check      = models.ImageField(verbose_name="Чек клиента", upload_to=upload_to, blank=True, null=True)

    ttn               = models.CharField(verbose_name="TTN", max_length=100, null=True, blank=True)
    ttn_status_code   = models.IntegerField(null=True, blank=True)
    ttn_status        = models.CharField(max_length=500,  null=True, blank=True)
    ttn_address       = models.CharField(max_length=1000, null=True, blank=True)
    ttn_is_archive    = models.BooleanField(default=False, null=True)

    payment           = models.CharField(verbose_name="Оплата", max_length=5, choices=PAYMENTS, default="S", blank=True)
    bank_check        = models.ImageField(verbose_name="Чек банка", upload_to=upload_to, null=True, blank=True)

    created           = models.DateTimeField(auto_now_add=True, null=True)
    updated           = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.client_name

    def ttn_data(self):
        if not self.ttn: return
        if self.ttn_is_archive: return

        self.ttn_address = get_ttn_address(self.ttn)

        el = get_ttn_status(self.ttn)
        if not el: return

        match el["StatusCode"]:
            case "1":
                st = "Очікування відправки"
            case "9" | "10" | "11":
                st = "Отримано"
                self.ttn_is_archive = True
            case _:
                st = el["Status"]

        self.ttn_status = st
        self.save()
        return


    def income(self):
        return self.price-self.product.price if self.product and self.product.price else None

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'