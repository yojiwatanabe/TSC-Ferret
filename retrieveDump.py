# -*- coding: utf-8 -*-

import json

DUMP_FILE = 'pluginText.dump'

f = open(DUMP_FILE, 'r')
rawData = json.load(f)
f.close()

formattedDict = []
for i in range(len(rawData)):
    formattedDict.append(json.loads(rawData[i]))

del f, rawData
