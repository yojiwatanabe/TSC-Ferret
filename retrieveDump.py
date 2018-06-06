# -*- coding: utf-8 -*-

import json

DUMP_FILE = 'pluginText.dump'


# 		loadData():()
#
# Function to load JSON information from a file stream
# Input  - none
# Output - Python dictionary with data
def loadData():
    f = open(DUMP_FILE, 'r')
    rawData = json.load(f)
    f.close()

    return rawData


def main():
    data = loadData()

    return 0


# # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    main()
