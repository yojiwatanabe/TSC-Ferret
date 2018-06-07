# SoftwareCompare
#### Yoji Watanabe & Saurav Gyawali
###### Summer 2018
Using Tenable Security Center's API, retrieve plugin output from scanned hosts to be saved in a human-friendly format (HTML table). Requires a valid Tenable Security Center account.

User can specify the plugin they would wish to retrieve the scan data for. Certain plugins also have special queries to create tables with a processed plugin output. See _Special Queries_ below for more information.

***

### Usage
1. Enter your Tenable Security Center host URL in the `dumpPluginOut.py` `HOST` global variable
2. Execute `run.py [-i I_FILE] PLUGIN_ID`, where `I_FILE` specifies an optional argument for a special query (explained below), and `PLUGIN_ID` is the desired plugin ID whose data will be retrieved.
3. Open `results.html` in an internet browser to see your results

### Special Queries
SoftwareCompare allows for special queries for certain plugins. This gives the user more control over how they wish to retrieve the plugin output. The plugins with special queries are:
##### Software Enumeration (SSH) - #22869
* A text file (.txt) with newline separated words can be used to specify which programs to query. For example, if one was interested in the versions of `gcc`, `make`, and `python` running on the different hosts, the text file would look like:
```
gcc
make
python
``` 

### Examples
* Find all software running on hosts (plugin 22869):
```
python run.py 22869
```
* Find certain software, specified in programs.txt, running on hosts (special query of plugin 22869):
```
python run.py -i programs.txt 22869
```
* Find if hosts are ARP, ICMP, TCP, or UDP ping-able by Nessus:
```
python run.py 10180
```