from CRM.celery import app
from datetime import datetime
from .models import *
import xml.etree.ElementTree as ET


@app.task
def fetch_supplier_data(sID):
    try:
        supplier = Supplier.objects.get(id=sID)
        fetch_data = supplier.fetch_data()

        print(fetch_data)

        root = ET.parse(fetch_data)
        item_list = root.findall("item")

        li = []
        for item in item_list:
            data = {
                "supplier": self,
                "article": item.find("barcode").text,
                "name": item.find("name").text,
                "price": int(item.find("priceuah").text) - 1,
                "image": item.find("image").text
            }
            li.append(item.find("name").text)
            author, created = Product.objects.get_or_create(article=item.find("barcode").text, defaults=data)

        print(f'LOAD Data - {supplier.name}: {"None" if not li else li}')
    except Exception as e:
        print(f'LOAD Data Error: \n{e}')

@app.task
def fetch_suppliers_data():
    for supplier in Supplier.objects.all():
        if not supplier.auto_import:
            name = supplier.name
            print(f'LOAD Skipped: {name}')
            continue

        supplier.load_data()
        print(f'LOAD Data - {supplier.name}')
