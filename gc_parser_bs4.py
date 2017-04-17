from urllib.request import urlopen
from os import path
import pickle
import re

from bs4 import BeautifulSoup

PLOTTABLE = True
try:
    from plotter import display_results as plt_disp
except ImportError:
    PLOTTABLE = False


class Guitar:
    def __init__(self, link, image, condition, price, item_id):
        self.link = link             # string - link
        self.image = image           # string - link
        self.condition = condition   # string
        self.price = price           # string
        self.item_id = item_id       # int

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.link, self.image, self.condition, self.price, self.item_id)

    def __eq__(self, other):
        return self.item_id == other.item_id

    def __ne__(self, other):
        return self.item_id != other.item_id

    def same_price(self, other):
        return self.price == other.price


class GCParserBS4:
    def __init__(self, data):
        self.soup = BeautifulSoup(data, "html.parser")
        self.guitars = []

        self.get_guitars()

    def get_guitars(self):
        sections = self.soup.find_all("div", class_="product")

        for section in sections:
            link = "http://www.guitarcenter.com" + str(section.find("a", href=True).attrs["href"])
            image = str(section.find("img", attrs={"data-original": True}).attrs["data-original"])
            condition = str(section.find("div", string=re.compile("Condition")).string)[:-10]
            price = str(section.find(string=re.compile("lowPrice:")))[15:]
            item_id = int(str(section.find("var", class_="hidden displayId").string))

            self.guitars.append(Guitar(link, image, condition, price, item_id))

    def get_results(self):
        return self.guitars


def main():
    # search - the search URL, and the keyword to look for
    search = "http://www.guitarcenter.com/Used/?Ntt=taylor%20314ce&Ns=r"
    response = urlopen(search)
    data = response.read().decode('utf-8')

    pth = path.join(path.dirname(path.abspath(__file__)), "314CE_GuitarCenter")

    gcp = GCParserBS4(data)

    results = gcp.get_results()
    for guitar in results:
        print(guitar)
    # pickle.dump(results, open(pth, "wb"))
    #
    # if PLOTTABLE:
    #     plt_disp(results)

if __name__ == '__main__':
    main()
