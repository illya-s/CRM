import os, re, glob, django, tqdm, json, datetime
from django.utils import timezone
from django.db.models import Value
from django.db.models.functions import Replace

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRM.settings")
django.setup()

from expense.models import *

# JOData = {"Expenses": []}

# with open("t.txt", "r", encoding="utf-8") as file:
#     data = file.readlines()
# for i in tqdm.tqdm(data, desc="Обработка", bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}"):
#     d = i.split("\t")
#     obj = {
#         "date": d[0],
#         "price": d[1],
#         "description": d[2],
#         "cat": d[3].replace("\n", '')
#     }
#     JOData["Expenses"].append(obj)
#     print(str(obj).replace("\'", "\"").replace("\n", ""))

# with open("t.json", "w", encoding="utf-8") as file:
#     json.dump(JOData, file, ensure_ascii=False, indent=4)


with open("t.json", "r", encoding="utf-8") as file:
    JOData = json.load(file)

for i in tqdm.tqdm(JOData["Expenses"], desc="Обработка", bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}"):
    date = datetime.datetime.strptime(i["date"], "%d.%m.%Y") # .strftime("%Y-%m-%d")
    aware_datetime = timezone.make_aware(date)
    price = i["price"]
    description = i["description"]

    eCat, created = ExpenseCategory.objects.get_or_create(name=i["cat"])
    Expense.objects.create(date=aware_datetime, price=price, description=description, category=eCat)


# Dobronravov

# def fetch_data(file):
#     tree = ET.parse(file)
#     root = tree.getroot()
#     items = root.find("items").findall("item")

#     new_root = ET.Element("items")
#     new_root.extend(items)
#     return new_root


# def fetch_supplier_data(sID):
#     try:
#         supplier = Supplier.objects.get(id=sID)
#         data = fetch_data('media/import/dobronravov.xml')
#         item_list = data.findall("item")

#         for item in tqdm.tqdm(item_list, desc="Processing"):
#             author, created = Product.objects.get_or_create(article=item.find("barcode").text, defaults={
#                 "supplier": supplier,
#                 "article": item.find("barcode").text,
#                 "name": item.find("name").text,
#                 "price": int(item.find("priceuah").text) - 1,
#                 "image": item.find("image").text
#             })

#         print(f'LOAD Data - {supplier.name}')
#     except Exception as e:
#         print(f'LOAD Data Error: \n{e}')

# fetch_supplier_data(14)

# import requests, config
# from bs4 import BeautifulSoup
# import xml.etree.ElementTree as ET

# import_url = "https://easydrop.one/prom-export?key=19100792694610&pid=82496907679816"

# root = ET.Element("items")
# response = requests.get(import_url, headers=config.firefox_mask) # 

# if response.status_code == 200:
#     items = ET.fromstring(response.content).find("items").findall("item")
#     root.extend(items)
#     print(root)
# else:
#     print(response.text)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     title = soup.title.string
#     text = soup.body.get_text(separator=" ", strip=True)
#     print(title, text)