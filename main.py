import asyncio
import aiohttp
import requests

from prettytable import PrettyTable
from bs4 import BeautifulSoup


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

            image = '\n'
            image_container = soup.find(class_="ux-image-carousel-container image-container")
            if image_container:
                image_elements = image_container.find_all(class_="ux-image-carousel-item image-treatment image")
                for i in image_elements:
                    image += f"{i.get('data-idx')} - {i.find('img').get('data-src')}\n"

            price_element = soup.find(class_='x-price-primary')
            price = price_element.get_text(strip=True) if price_element else 'N/A'

            seller_element = soup.find(class_="x-sellercard-atf")
            seller_url = seller_element.find('a').get('href')
            seller_name = seller_url.find('span').
            seller = f"{seller_name} - {seller_url}"

            description = soup.find(id='desc_ifr').get('src')

            return {
                'title': title,
                'image': image,
                'item_url': self.url,
                'price': price,
                'seller': seller,
                'description': description
            }
        else:
            print(f"Failed to retrieve data, status code: {response.status_code}")
            return None

    def display_item_data(self, item_data):
        if item_data:
            print(f"Title: {item_data['title']}")
            print(f"Image: {item_data['image']}")
            print(f"Item_URL: {item_data['item_url']}")
            print(f"Price: {item_data['price']}")
            print(f"Seller: {item_data['seller']}")
            print(f"Description URL: {item_data['description']}")


if __name__ == '__main__':
    country_info = Country()
    asyncio.run(country_info.get_country_info())

    url = input("Enter ur URL:\n")
    ebay_item_info = EbayItem(url)
    item_data = ebay_item_info.get_item_data()
    ebay_item_info.display_item_data(item_data)
