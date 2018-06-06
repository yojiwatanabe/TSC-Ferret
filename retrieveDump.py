# -*- coding: utf-8 -*-

import json

DUMP_FILE = 'pluginText.dump'

f = open(DUMP_FILE, 'r')
rawData = json.load(f)
f.close()

for value in rawData:
    print value['DNS']
