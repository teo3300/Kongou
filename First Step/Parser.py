import logging as l                 # logging
from html.parser import HTMLParser

class Parser(HTMLParser):                                                       # Parser class
    def __init__(self, name):
        HTMLParser.__init__(self)
        self.name = name
        self.record = False                                                     # True: record, False: do not
        self.isKey = False                                                      # True: reading key, False: reading content
        self.key = ""
        self.data = {}

    def handle_starttag(self, tag, attributes):
        if tag != "td": return                                                  # ignore other tags
        for name, value in attributes:
            if name == 'colspan' and value == '2':                              # ignore image and head
                self.record = False
                return
        self.record = True
        self.isKey = not self.isKey

    def handle_endtag(self, tag):
        if tag == "td":
            self.record = False

    def handle_data(self, text):
        if self.record:
            if self.isKey:
                self.key = text.replace(':', '')
            else:
                if not self.key in self.data:
                    self.data[self.key] = text
                else:
                    self.data[self.key] += text

    def format(self):
        for val in self.data:
            self.data[val] = self.data[val].strip('\n').replace('\xa0', ' ')

    def ret(self):
        return self.data
