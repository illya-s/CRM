from CRM.celery import app
from .models import *
from django.db.models import Value
from django.db.models.functions import Replace
# import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

@app.task
def get_ttns_status():
    orders = Order.objects.all().order_by('-id')[:100]
    if not orders:
        logger.info("Skipped: No orders!")
        return

    ttns = [
        { 'ttn': ''.join(order.ttn.split(" ")) , 'id': order.pk }
        for order in orders if not order.ttn_is_archive
    ]

    headers = { 'Content-Type': 'application/json', 'Api-Key': config.api_key }
    data = {
        "modelName": "TrackingDocumentGeneral",
        "calledMethod": "getStatusDocuments",
        "methodProperties": {
            "Documents": [{ "DocumentNumber": ttn_data['ttn'] } for ttn_data in ttns]
        }
    }

    response = requests.get(config.np_url, json=data, headers=headers)
    if response.status_code == 200:
        for el in response.json()['data']:
            try:
                order = Order.objects.annotate(
                    normalized_field=Replace('ttn', Value(" "), Value(""))
                ).filter(normalized_field=el["Number"])[0]
            except:
                continue

            match el["StatusCode"]:
                case '1':
                    st = "Очікування відправки"
                case '2' | '3':
                    st = el["Status"]
                    order.ttn_is_archive = True
                case "9" | "10" | "11":
                    st = "Отримано"
                    order.ttn_is_archive = True
                case "102" | "103" | "105" | "106" | "111":
                    st = el["Status"]
                    order.amount = 0
                    order.ttn_is_archive = True
                case _:
                    st = el["Status"]
            order.ttn_status_code = el["StatusCode"]
            order.ttn_status = st
            order.ttn_address = el["WarehouseRecipient"]
            order.save()
    return None

@app.task
def get_ttn_status(oID:int):
    try:
        order = Order.objects.get(id=oID)
    except:
        return False

    if not order.ttn or order.ttn_is_archive == True:
        return False

    headers = { 'Content-Type': 'application/json', 'Api-Key': config.api_key }
    data = {
        "modelName": "TrackingDocumentGeneral",
        "calledMethod": "getStatusDocuments",
        "methodProperties": {
            "Documents": [{ "DocumentNumber": ''.join(order.ttn.split(' ')) }]
        }
    }
    response = requests.get(config.np_url, json=data, headers=headers)
    if response.status_code == 200:
        el = response.json()['data'][0]

        match el["StatusCode"]:
            case '1':
                st = "Очікування відправки"
            case '2' | '3':
                st = el["Status"]
                order.ttn_is_archive = True
            case "9" | "10" | "11":
                st = "Отримано"
                order.ttn_is_archive = True
            case _:
                st = el["Status"]

        order.ttn_status_code = el["StatusCode"]
        order.ttn_status = st
        order.ttn_address = el["WarehouseRecipient"]
        order.save()
        return True
    return False


# import csv
# def load_orders_by_csv(file:str):
#     with open('file.csv', mode='r', newline='', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             print(row)
#     durl = f"https://check.checkbox.ua/{data_hash}/pdf?download=true"
#     pass


@app.task
def fetch_orders_data():
    orders = Order.objects.all()
    for order in orders:
        if order.ttn_is_archive:
            continue
        order.ttn_data()
    print(f'LOADED {len(orders)} TTN Data')
