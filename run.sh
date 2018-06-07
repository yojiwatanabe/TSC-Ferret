#!/bin/bash

echo "Getting plugin output for plugin" $1


python dumpPluginOut.py $1
echo "Retrieved plugin, dumped data to 'pluginText.dump'"

echo "Building table..."
python processDump.py
echo "Table built, saved to results.html"