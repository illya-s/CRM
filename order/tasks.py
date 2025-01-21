from CRM.celery import app
from datetime import datetime
from .models import *
import xml.etree.ElementTree as ET



# @app.task
# def get_ttns_status():
#     orders = Order.objects.all()
#     ttns = [{ 'ttn': order.ttn, 'id': order.pk } if order.ttn_is_archive else None for order in orders ]
#     ttns = list(filter(lambda x: x is not None, [ order.ttn if order.ttn_is_archive else None for order in orders ]))
#     headers = { 'Content-Type': 'application/json', 'Api-Key': config.api_key }
#     data = {
#         "modelName": "TrackingDocumentGeneral",
#         "calledMethod": "getStatusDocuments",
#         "methodProperties": {
#             "Documents": [{ "DocumentNumber": ''.join(ttn.split(" ")) } for ttn in ttns]
#         }
#     }
#     response = requests.get(config.np_url, json=data, headers=headers)
#     if response.status_code == 200:
#         for el in response.json()['data']:
#             if el["StatusCode"] == "1":
#                 st = "Очікування відправки"
#             elif el["StatusCode"] in ["9", "10", "11"]:
#                 st = "Отримано"
#             else:
#                 st = el["Status"]
#             { "code": el["StatusCode"], "name": st }
#     return None

@app.task
def get_ttn_status(oID:int):
    try:
        order = Order.objects.get(id=oID)
    except:
        return False

    if not order.ttn:
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
            case ["9", "10", "11"]:
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


@app.task
def fetch_orders_data():
    orders = Order.objects.all()
    for order in orders:
        if order.ttn_is_archive:
            continue
        order.ttn_data()
    print(f'LOADED {len(orders)} TTN Data')
