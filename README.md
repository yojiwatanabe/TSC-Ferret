# Tenable Security Center Search
#### Yoji Watanabe & Saurav Gyawali
###### Summer 2018
Using Tenable Security Center's API, retrieve plugin output from scanned hosts to be saved in a human-friendly format (HTML table). Requires a valid Tenable Security Center account.

User can specify the plugin they would wish to retrieve the scan data for. User can also add filters and search query to get a customized table. Results can be filtered based on IP addresses and repository. User can also search for multiple queries inside the plugin output data with or without the filters.

***

### Usage
1. Enter your Tenable Security Center host URL in the `dumpPluginOut.py` `HOST` global variable
2. Execute `$ ./run.py [-h] [-s SEARCH_LIST] [-R REPOS] [-H HOSTS] [-i IP_RANGE] [-c] [-d] [-e] plugin_id`, where `PLUGIN_ID` is the desired plugin ID whose output will be retrieved
    * `-s SEARCH LIST` allows user to query each plugin output for keywords (see Search Queries below)
    * `-R REPOS` allows user to filter for certain repositories (see Repository Filter below)
    * `-H HOSTS` allows user to filter for certain hosts (see IP Address + IP Range filter below)
    * `-i IP_RANGE` allows user to filter for certain IPs (see IP Address + IP Range filter below)
    * `-c` changes the table output method from an HTML table to a CSV file
    * `-d` allows duplicates to be shown in table, default behavior is to only show latest scan result
    * `-e` will email the results to user-specified recipients (see Emailing Results) below
3. Open results with an HTML or CSV viewer, according to the chosen output

### Search Queries
Tenable Security Center Search allows for special queries for all plugins. This gives the user more control over how they wish to retrieve the plugin output. A text file (.txt) with newline separated words can be used to specify which word to query. For example, if one was interested in `gcc`, `make`, and `python` on different hosts, the text file would look like:
```
gcc
make
python
``` 

### Filters
There are three available filters in TSCS. These filters can be used to output data with only the desired ip or repository. 

#### Repository Filter
For getting data based on repository, user can make a text file (.txt) with a single repository per line. For example, if the user needs the data related to `atst01nix001` and `aprd01nix001` repositories, the text file would look like:
```
atst01nix001
aprd01nix001
```
The user would then use `[-R REPO_LIST]` as an optional argument where `REPO_LIST` is the text file name.

 #### IP Address + IP Range filter
For getting data based on IP addresses, user has two choices. One way is to make a text file (.txt) with one IP Address per line. Then the user should use `[-H --host_list HOST_LIST]` as an optional argument where `HOST_LIST` is the text file name. Another way is to specify a range of ip. The user can use `[-i --ip_range IP_RANGE]` as an optional argument where `IP_RANGE` is in the format `xxx.xxx.xxx.xxx/xx` without any spaces in the IP. This range should be in CIDR notation.

### Config file
User can save the choice of arguments and the credential in config files which can be fed into TSCS to easily search in the scan results. The config file can have any name and should be fed in the format `python run.py -C CONFIG_FILE` where `CONFIG_FILE` is the name of the file that has the user's choices in json format. 
A config file can be generated using the script `config_gen.py` which can be run using the command `python config_gen.py`. This script asks the user for choices interactively and stores them in a file with the name specified by user.

### Emailing Results
The user can choose to email the resulting table (in CSV or HTML format) to a list of recipients. This is done by connecting to a user-specified SMTP server, specified in the global variables in `email_results.py` lines 19, 20. Recipients are added in line 21. Results are sent as an email attachment along with a short summary of the query in the body of the email. 
(Note: some email providers may filter these reports as spam/junk)

### Examples
* Find all software running on hosts (plugin 22869):
```
python run.py 22869
```
* Find software version history on host 127.0.0.1 (plugin 22869):
```
python run.py -d -i 127.0.0.1/32 22869
```
* Find certain software, specified in programs.txt, running on hosts:
```
python run.py -s programs.txt 22869
```
* Find if hosts are ARP, ICMP, TCP, or UDP ping-able by Nessus:
```
python run.py 10180
```
