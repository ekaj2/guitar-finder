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
        # TODO - fill in the following sections w/ bs4
        self.link = link
        self.image = image
        self.condition = condition
        self.price = price
        self.item_id = item_id


class GCParserBS4:
    def __init__(self, data):
        self.soup = BeautifulSoup(data, "html.parser")
        self.guitar_sections = []
        self.guitars = []

        self.get_instrument_tag_section()
        self.get_guitars_from_sections()

    def get_instrument_tag_section(self):
        self.guitar_sections = self.soup.find_all("div", class_="product")

    def get_guitars_from_sections(self):
        for section in self.guitar_sections:
            link = "http://www.guitarcenter.com" + str(section.find("a", href=True).attrs["href"])
            image = str(section.find("img", attrs={"data-original": True}).attrs["data-original"])
            condition = str(section.find(name="div", string=re.compile("Condition")).string)[:-10]
            price = str(section.find(string=re.compile("lowPrice:")))[15:]
            item_id = str(section.find("var", class_="hidden displayId").string)

            print(link, image, condition, price, item_id)
            self.guitars.append(Guitar(link, image, condition, price, item_id))

    def get_results(self):
        return self.guitar_sections


def main():
    # search - the search URL, and the keyword to look for
    search = "http://www.guitarcenter.com/Used/?Ntt=taylor%20314ce&Ns=r"
    response = urlopen(search)
    data = response.read().decode('utf-8')

    pth = path.join(path.dirname(path.abspath(__file__)), "314CE_GuitarCenter")

    gcp = GCParserBS4(data)

    results = gcp.get_results()
    for r in results:
        print("=" * 50)
        print(r)
    # pickle.dump(results, open(pth, "wb"))
    #
    # if PLOTTABLE:
    #     plt_disp(results)

if __name__ == '__main__':
    main()
