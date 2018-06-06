# -*- coding: utf-8 -*-

import json

f  = open('pluginText.dump', 'r')
data = json.load(f)
print len(data)
