import logging as l                 # logging
from Parser import Parser

class Ship:
    tab = None
    data = None
    def __init__(self, entry):
        '''Create Ship properties from entry'''
        self.entry = entry
        self.ID = entry["ID"]                                                   # fast access to ship properties
        self.name = entry["Name"]                                               # remove redundant afterwards
        self.fullname = entry["Fullname"]                                       #
        self.page = entry["Page"]                                               #
        self.navy = entry["Navy"]                                               #
        self.Class = entry["Class"]                                             #
        self.type = entry["Type"]                                               #
        self.dislacement = entry["Displacement"]                                #
        self.commissioned = entry["Commissioned"]                               #
        self.fate = entry["Fate"]                                               #

    def getTab(self):
        '''request wiki table'''
        #import logging as l                                                     # logging
        if not self.page:
            l.debug("page for " + self.name + " does not exists")
        else:
            import requests as req                                              # infos come from wikipedia :3
            try:
                try:
                    res = req.get(self.page)
                except:
                    l.error("no response from" + self.name)
                    exit(1)
                else:
                    if res.status_code != 200:
                        l.warning("can't reach page for " + self.name)
                    else:
                        res = res.text
                        res = res.split("</tbody>")[0]
                        res = res.split("<tbody>")[1]
                        self.tab = res
            except:
                l.error("getting tab for " + self.name)

    def getData(self):
        if self.page:
            parser = Parser(self.name)
            parser.feed(self.tab)
            parser.format()
            self.data = parser.ret()
