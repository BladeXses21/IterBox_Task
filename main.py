import asyncio
import aiohttp
import requests

from prettytable import PrettyTable
from bs4 import BeautifulSoup
import json


class Country:
    def __init__(self):
        self.url = "https://restcountries.com/v3.1/all"

    async def get_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(f'Error! Response status: {response.status}')
                    return None

    def display_data(self, countries):
        table = PrettyTable()
        table.field_names = ["Country Name", "Ca[ital", 'Flag URL']
        for country in countries:
            name = country.get('name', {}).get("common", "N/A")
            capital = country.get("capital", ["N/A"])[0]
            flag = country.get("flags", {}).get("png", "N/A")
            table.add_row([name, capital, flag])

        print(table)

    async def get_country_info(self):
        data = await self.get_data()
        if data:
            self.display_data(data)


class EbayItem:
    def __init__(self, url):
        self.url = url

    def get_item_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            title_element = soup.find(class_="x-item-title__mainTitle")
            title = title_element.get_text(strip=True) if title_element else 'N/A'

            images = []
            image_container = soup.find(class_="ux-image-carousel-container image-container")
            if image_container:
                image_elements = image_container.find_all(class_="ux-image-carousel-item image-treatment image")
                for i in image_elements:
                    img_url = i.find('img').get('data-src')
                    images.append(img_url)

            price_element = soup.find(class_='x-price-primary')
            price = price_element.get_text(strip=True) if price_element else 'N/A'

            seller_element = soup.find(class_="x-sellercard-atf")
            seller_url = seller_element.find('a').get('href')
            seller_name = seller_element.find('span').get_text(strip=True)
            seller = f"{seller_name} - {seller_url}"

            shipping_container = soup.find(class_="ux-labels-values col-12 ux-labels-values--shipping").find(class_='ux-labels-values__values col-9').get_text(strip=True)

            description = soup.find(id='desc_ifr').get('src')

            return {
                'title': title,
                'images': images,
                'item_url': self.url,
                'price': price,
                'seller': seller,
                'shipping': shipping_container,
                'description': description
            }
        else:
            print(f"Failed to retrieve data, status code: {response.status_code}")
            return None

    def display_item_data(self, item_data):
        if item_data:
            print(f"Title: {item_data['title']}")
            for index, img_url in enumerate(item_data['images'], start=1):
                print(index, img_url)
            print(f"Item_URL: {item_data['item_url']}")
            print(f"Price: {item_data['price']}")
            print(f"Seller: {item_data['seller']}")
            print(f"Shipping: {item_data['shipping']}")
            print(f"Description URL: {item_data['description']}")

    def save_to_json(self, item_data, filename='item_data.json'):
        if item_data:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(item_data, f, ensure_ascii=False, indent=4)
            print(f"Data saved to {filename}")


if __name__ == '__main__':
    country_info = Country()
    asyncio.run(country_info.get_country_info())

    url = input(
        "You can use this - https://www.ebay.com/itm/355841037427?_trkparms=amclksrc%3DITM%26aid%3D777008%26algo%3DPERSONAL.TOPIC%26ao%3D1%26asc%3D20230906152218%26meid%3D50b65bd094cc434ba3fca4adec279fb6%26pid%3D101817%26rk%3D1%26rkt%3D1%26itm%3D355841037427%26pmt%3D0%26noa%3D1%26pg%3D4375194%26algv%3DPersonalizedTopicsV2WithDynamicSizeRanker%26brand%3DJordan&_trksid=p4375194.c101817.m47269&_trkparms=parentrq%3Aa24e31dd1900a514ba3b8ae4ffff9afe%7Cpageci%3A220cc051-3f96-11ef-a420-fea1091129b8%7Ciid%3A1%7Cvlpname%3Avlp_homepage\nEnter ur URL :\n")
    ebay_item_info = EbayItem(url)
    item_data = ebay_item_info.get_item_data()
    ebay_item_info.display_item_data(item_data)
    ebay_item_info.save_to_json(item_data)
