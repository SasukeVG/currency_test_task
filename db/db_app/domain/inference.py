import asyncio
import xml.etree.ElementTree as ET

import requests
from db_app.crud.crud_ops import create_currency
from db_app.db.database import AsyncSessionLocal


async def fetch_and_store_currency_rates():
    while True:
        await update_currency_rates()
        await asyncio.sleep(86400)  # 24 hours in seconds


async def update_currency_rates():
    response = requests.get("https://cbr.ru/scripts/XML_daily.asp")
    if response.status_code == 200:
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()

        async with AsyncSessionLocal() as db:
            for valute in root.findall('Valute'):
                num_code = valute.find('NumCode').text
                char_code = valute.find('CharCode').text
                nominal = int(valute.find('Nominal').text)
                name = valute.find('Name').text
                value = float(valute.find('Value').text.replace(',', '.'))
                unit_rate = float(valute.find('VunitRate').text.replace(',', '.'))

                await create_currency(db, num_code, char_code, nominal, name, value, unit_rate)

