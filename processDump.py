# -*- coding: utf-8 -*-

import json
import numpy as np

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
	input = f.read().splitlines()
	return input


def main():
    data = loadData()
    inputData = readInput()

    resultMat = np.matrix('', dtype=str)
    resultMat = np.resize(resultMat, (len(data), len(inputData)))
    for i, host in enumerate(data):
        for j, inputProgram in enumerate(inputData):
            tempList = []
            for program in host['CONTENT']:
                if inputProgram in program:
                    tempList.append(program)
            resultMat.put([i, j], tempList)


    print resultMat.flatten()

    return 0


# # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    main()