import logging as l                 # logging

class Writer:
    letter = ""
    classId = ""
    cnt = 0
    ship = None

    def __init__(self, outFolder, className, pLen):
        import os                                                               # operate in fs
        if not os.path.isfile(className):                                       # check for directory containing ships data
            l.error(className + ' does not exists')
            exit(1)
        classFile = open(className, "r")
        self.classList = []
        for line in classFile:
            self.classList.append(line[:-1])                                    # list class
        self.classLen = len(self.classList)                                     # class len
        self.pLen = pLen                                                        # digits for progressive number
        self.outFolder = outFolder                                              # directory for output file

    def setLetter(self, letter):
        self.letter = letter

    def setShip(self, ship):
        self.ship = ship

    def reset(self, start):
        self.cnt = start

    def save(self):

        ID = self.letter

        if not self.ship.entry["Type"]:
            self.classId = "00"
        elif not self.ship.entry["Type"] in self.classList:
            self.classId = "99"
        else:
            self.classId = str(self.classList.index(self.ship.entry["Type"])+1).zfill(2)

        ID += self.classId
        ID += str(self.cnt).zfill(3)

        import json
        with open(self.outFolder + "\\" + ID + ".json", 'w') as fp:
            json.dump(self.ship.data, fp)
            fp.close()
        self.cnt += 1
