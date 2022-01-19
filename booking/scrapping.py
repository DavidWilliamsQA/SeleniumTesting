import requests
from helium import *
from bs4 import BeautifulSoup
import pandas as pd


class Scrapping:
    def extract(self, page_source):
        soup = BeautifulSoup(page_source, "html.parser")
        return soup

    def transform(self, soup):
        propertyList = []
        property_divs = soup.find_all(
            "div",
            class_="_fe1927d9e _0811a1b54 _a8a1be610 _022ee35ec b9c27d6646 fb3c4512b4 fc21746a73",
        )

        for property in property_divs:
            name = property.find("div", class_="fde444d7ef _c445487e2").text.strip()
            price = property.find("span", class_="fde444d7ef _e885fdc12").text.strip()
            propertyDictionary = {"name": name, "price": price}
            propertyList.append(propertyDictionary)

        return propertyList

    def execute(self, page_source):
        extracting = self.extract(page_source)
        properties = self.transform(extracting)

        df = pd.json_normalize(properties)
        df.to_csv("results.csv")
