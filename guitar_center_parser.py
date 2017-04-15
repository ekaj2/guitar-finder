#! /usr/bin/python3

from urllib.request import urlopen
from html.parser import HTMLParser
import pickle
from os import path

from emailer import Emailer

PLOTTABLE = True
try:
    from plotter import display_results as plt_disp
except ImportError:
    PLOTTABLE = False


class GuitarCenterParser(HTMLParser):

    def __init__(self, keyword, results=None):
        super().__init__()

        if results is None:
            results = {}
        self.divs = 0
        self.found_guitar = False
        self.keyword = keyword
        self.item_id = ""
        self.in_item_id = False

        self.link = ""
        self.image = ""
        self.condition = ""
        self.price = ""
        self.results = {"poor": {}, "fair": {}, "good": {}, "great": {}, "excellent": {}}
        for result in results:
            self.results[result] = results[result]

    def error(self, message):
        print(message)

    def handle_starttag(self, tag, attrs):
        # for the "guitar" divs
        if tag == "div":
            self.divs += 1  # increment the number of divs
            if attrs and attrs[0][0] == "class" and attrs[0][1] == "product":
                print("\n=============== FOUND AN INSTRUMENT ===============")
                self.found_guitar = True
                self.divs = 1  # reset number of <div> tags when we find a guitar

        # for the item ID
        elif tag == "var":
            if attrs and attrs[0][0] == "class" and attrs[0][1] == "hidden displayId":
                self.in_item_id = True

        elif tag == "a":
            if self.found_guitar and attrs and attrs[0][0] == "href":
                self.link = "http://www.guitarcenter.com" + attrs[0][1].strip()

        elif tag == "img":
            if self.found_guitar and len(attrs) >= 3 and attrs[2][0] == "data-original":
                self.image = attrs[2][1].strip()  # get the image url

    def handle_endtag(self, tag):
        if tag == "div":
            self.divs -= 1

        elif tag == "var" and self.in_item_id:
            self.in_item_id = False

        if self.found_guitar and self.divs == 0:  # finalize a guitar entry
            try:
                if self.results[self.condition][self.item_id] != self.price:
                    self.send_email("Price was changed from ${} to ${} on item #{}.".format(
                        self.results[self.condition][self.item_id], self.price, self.item_id))
                    self.add_price()
            except KeyError:
                self.send_email("Found a new guitar for ${} (item #{})".format(
                    self.price, self.item_id))
                self.add_price()

            self.found_guitar = False
            print("=============== END OF INSTRUMENT INFO ===============")

    def handle_data(self, data):
        if self.found_guitar and data.strip():
            if self.keyword in data:
                print(data)

            elif "lowPrice" in data:
                first_index = str(data).find("lowPrice")
                # the format is "lowPrice:DOLLAR_AMOUNT" so we move 9 chars ahead of the match
                self.price = float(data[first_index + 9:])
                print("${}".format(self.price))

            elif "Condition" in data:
                first_index = str(data).find("Condition")
                self.condition = data[:first_index].strip().lower()
                print("Condition: " + self.condition.title())

            elif self.in_item_id:
                self.item_id = data.strip()
                print(self.item_id)

    def add_price(self):
        self.results[self.condition][self.item_id] = self.price

    def send_email(self, information, prnt=True):
        if prnt:
            print("Sending information in email...")
            print(information)

        link = '<a href="{}">Click here to view guitar</a>'.format(self.link)
        image = '<img src="{}">'.format(self.image)

        Emailer(information, "<html>{info}<br><br>{link}<br><br>{img}</html>".format(info=information, link=link, img=image))

    def get_results(self):
        return self.results


def main():
    # dummy call to get info added correctly
    Emailer("Success!", "<html>Success!</html>")

    # search - the search URL, and the keyword to look for
    search = "http://www.guitarcenter.com/Used/?Ntt=taylor%20314ce&Ns=r"
    response = urlopen(search)
    data = response.read().decode('utf-8')

    pth = path.join(path.dirname(path.abspath(__file__)), "314CE_GuitarCenter")

    try:
        gcp = GuitarCenterParser("314CE", pickle.load(open(pth, "rb")))
    except FileNotFoundError:
        gcp = GuitarCenterParser("314CE")
    gcp.feed(data)

    results = gcp.get_results()
    print(results)
    pickle.dump(results, open(pth, "wb"))

    if PLOTTABLE:
        plt_disp(results)

if __name__ == '__main__':
    main()
