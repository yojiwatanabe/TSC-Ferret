# -*- coding: utf-8 -*-

import json

DUMP_FILE = 'pluginText.dump'
INPUT_FILE = 'programs.txt'

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

def readInput():
	f = open(INPUT_FILE, 'r')
	inputList = []
	temp = f.read().splitlines()
	return temp


def main():
    data = loadData()
    inputData = readInput()
    for host in data:
        for program in host['CONTENT']:
            for inputProgram in inputData:
                if inputProgram in program:
                    print program
    return 0


# # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    main()