DICT_FOLDER = r".\Scraped alphabetical list of ships"
OUTPUT_FOLDER = r".\raw"
CLASSES = r".\sorted_classes.txt"

from time import sleep
import os                           # operate in fs
import logging as l                 # logging
import json                         # read dict
from Ship import Ship               # Ship class for requests
from Writer import Writer           # Writer class to write single file

# ENTRY TEMPLATE:
#   "A0":{
#       "ID":"",
#       "Name":"Aaron Ward (DD-483)",
#       "Fullname":"USS Aaron Ward (DD-483)",
#       "Page":"https://en.wikipedia.org/wiki/USS_Aaron_Ward_(DD-483)",
#       "Navy":"United States Navy",
#       "Class":"Gleaves",
#       "Type":"destroyer",
#       "Displacement":1630,
#       "Commissioned":"4 March 1942",
#       "Fate":"Sunk 7 April 1943[5]"
#    }

def file_check():
                                                                                # DICT_FOLDER
    if not os.path.isdir(DICT_FOLDER):                                          # check for directory containing ships data
        l.error(DICT_FOLDER + ' does not exists')
        exit(1)
    elif not os.listdir(DICT_FOLDER):                                           # if empty can't fetch data
        l.error(DICT_FOLDER + ' is empty')
        exit(1)
                                                                                # OUTPUT_FOLDER
    if not os.path.isdir(OUTPUT_FOLDER):                                        # check for an output directory
        try:
            os.mkdir(OUTPUT_FOLDER)                                             # create if missing
        except OSError:
            l.error(OUTPUT_FOLDER + " does not exists, impossible to create")
            exit(1)
        l.warning(OUTPUT_FOLDER + " does not exists, created now")
    #elif os.listdir(OUTPUT_FOLDER):                                             # warn if not empty
        #keep = input(OUTPUT_FOLDER + '" not empty, continue? [y/N] ')
        #if keep.lower() != "y":
        #    l.error("can't write in " + OUTPUT_FOLDER)
        #    exit(1)

def main():

    track = []
    tf = open(r".\track.txt","r")
    for line in tf:
        track.append(line[:-1])
    tf.close()

    dict_fold = os.listdir(DICT_FOLDER)
    writer = Writer(OUTPUT_FOLDER, CLASSES, 3)                                  # output folder, class file, progressive number length
    for file in dict_fold:
        letter = file.split("_")[1]                                             # current letter (for temporary ID)
        writer.reset(0)
        writer.setLetter(letter)
        file = DICT_FOLDER + '\\' + file
        file = open(file, encoding='utf-8')
        page = json.load(file)
        l.warning("fetching " + letter + ", length: " + str(len(page)))
        for entry in page:
            if not entry in track:
                tf = open(r".\track.txt","a")
                tf.write(entry + "\n")
                ship = Ship(page[entry])                                            # TODO: usa le eccezioni al posto dei null
                l.debug("REQ:" + entry)
                ship.getTab()
                ship.getData()
                sleep(0.4)
                if ship.page:
                    writer.setShip(ship)
                    writer.save()
                tf.close()
    tf.close()
    print("YEEE")

if __name__ == "__main__":
    l.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=l.NOTSET)
    file_check()
    main()
