# TSC Ferret
```
             .,..,.,
         .***//***/(//((/           _________   ______     ______
           *,**,//((//(( .*.,      |  _   _  |.' ____ \  .' ___  |
      .,,./.,,****/***.,(((/,      |_/ | | \_|| (___ \_|/ .'   \_|
     ..,* .   , ,  .     ,/(/,,        | |     _.____`. | |
     .,,.                 ./#,.       _| |_   | \____) |\ `.___.'\
      .       .   .   .,/*,./*,.     |_____|   \______.' `.____ .'
          *(//.**,.,/(/%%%*,,,.     ________                               _
         .*#&(**((*/#%&@&&%,.*.    |_   __  |                             / |_
  ,...   ,*//,*//*/%%%%%%*,/         | |_ \_|.---.  _ .--.  _ .--.  .---.`| |-'
  *,*,,. ,/(*     ,,*/*/%&%./.       |  _|  / /__\\[ `/'`\][ `/'`\]/ /__\\| |
 ./****,  .*      ..,*/,(((##(.     _| |_   | \__., | |     | |    | \__.,| |,
./***/(*(,.       ../...*%%%%%(*   |_____|   '.__.'[___]   [___]    '.__.'\__/
,//*/(/(((//,.     ..,*%/%%&&&%(#,,,..  ..
.///((##(##(##(%&&&&%%%%&&&&&&&&%%##%%%%%%#/,
.(((((###/%%#%%&%#&%&&%&&&&@&&&&%%%#%%%%&&%%%#/.
.((###%%##%%%%%&&&&&%%&&&@@&&&&&%%%#&&&&&&&&&%#*
./#(#%%%#%%%%&&&&&&&&&&&&&@@@@@&&&%%%%%%&&&&&&&&%#/.
 (#%%%%%%%%%&&&&&&@&@&&&&@@@@@@@&&%%%%%&&&&&&&&&&&%/.
,##%%%&&&&&&&&&&&&&&@@&@@@@@@@@@@&%%%%%%&&&&&&&&&&&&%/,,,.,,...
,#%%%%%&&&&&&&&&@@@@@@@@@@@@@@@@@&%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%#(*,.
*%%%%%&&&&&&@&@@@@@@@@@@@@@@@@@@@&&%%&&&&&&&@@@@@&&&&&@@@@@@@@@@@&&@&&&&&%*
,#%%&&&&&@&@@@@@@@&@@@@@@@@@@@@@@@&&%%&&&&&&@@@@@@&@@@@@@@@@@@@@@@@@@@@&&&%,
 /%%&&&@&@@&@@@@@@@@@@@@@@@@@@@@@@@&%&&&&&&&&&&&&&&@@@@@@@@@@@@@@@@@@@@@@@@&(
  (%&&&@@@@@@&@@@&&@@@@@@&@@@@@@@@@&&&&&&&&&&&&&&&&&&&@@@@@@@@@@@@@@@&@&@@@&/
  ,%%&&@@@@@@@@@@&&&@@@@@@@@@@@@@@@@&&&&&&&&&&&&&%%##((///**////(#&@@@@@@@@&/.
  *%&@@@@@@/*(%&&@@&@@@@@&&@@@@@@@@@@@@@&&%%##((//**,...         ..,,(&@@@/.
  %&@@@&@@&//(#%&&&&@@@@@&&@@@@@@@&&&&&%%%%%%###((//
  /&&(,@%,@&(#////#&@@@@&@@&&@%&&%###((//**,,,.
                  /#&/@@@*@@&&%&&%(*.
```
#### Yoji Watanabe & Saurav Gyawali
###### Summer 2018
Using Tenable Security Center's API, retrieve plugin output from scanned hosts to be saved in a human-friendly format (HTML table). Requires a valid Tenable Security Center account.

User can specify the plugin they would wish to retrieve the scan data for. User can also add filters and search query to get a customized table. Results can be filtered based on IP addresses and repository. User can also search for multiple queries inside the plugin output data with or without the filters.

***

### Usage
1. Enter your Tenable Security Center host URL in the `dumpPluginOut.py` `HOST` global variable
2. Execute `$ ./run.py [-h] (-P PLUGIN_ID | -C CONFIG) [-s SEARCH_LIST] [-R REPOS] [-H HOSTS] [-i IP_RANGE] [-d] [-e] [-o OUTPUT]`
    * `-C CONFIG_FILE` allows user to pass arguments from a pre-written config file (see Config File section below)
    * `-P PLUGIN_ID` the desired plugin ID whose output will be retrieved
    * `-s SEARCH LIST` allows user to query each plugin output for keywords (see Search Queries section below)
    * `-R REPOS` allows user to filter for certain repositories (see Repository Filter section below)
    * `-H HOSTS` allows user to filter for certain IP addresses (see IP Address + IP Range filter section below)
    * `-i IP_RANGE` allows user to filter for certain IP addresses (see IP Address + IP Range filter section below)
    * `-c COLUMNS` filters in only the specified host columns (DNS, IP, MAC, REPO, L_SEEN) and content (CONTENT)
    * `-d` allows duplicates to be shown in table, default behavior is to only show latest scan result
    * `-e` will email the results to user-specified recipients (see Emailing Results) below
    * `-o` changes the output file type from the default (HTML) to one of four total choices: HTML, PDF, CSV, and JSON
3. Open results with an HTML, CSV, or PDF viewer, according to the chosen output

### Filters
There are three available filters in TSC Ferret. These filters can be used to output data with only the desired ip or repository. 

#### Repository Filter
For getting data based on repository, user can make a text file (.txt) with a single repository per line. For example, if the user needs the data related to `atst01nix001` and `aprd01nix001` repositories, the text file would look like:
```
atst01nix001
aprd01nix001
```
The user would then use `[-R REPO_LIST]` as an optional argument where `REPO_LIST` is the text file name.

#### IP Address + IP Subnet Filter
For getting data based on IP addresses, user has two choices. One way is to make a text file (.txt) with one IP Address or one IP subnet per line (IPv4, IPv6, or CIDR). Then the user should use `[-H --host_list HOST_LIST]` as an optional argument where `HOST_LIST` is the text file name. Another way is to specify an IP subnet to query from the command line. The user can use `[-i --ip_range IP_RANGE]` as an optional argument where `IP_RANGE` is in the format `xxx.xxx.xxx.xxx/xx` without any spaces in the IP. The subnet should be in CIDR notation.

#### Column Filter
For filtering in only specific data, users can specify the columns to return. By default, the host's DNS, IP, and MAC address, repository, and last seen date is returned along with the plugin output. These columns can be specified by passing in a list of the desired data with the column argument. The columns that can be specified are:
* DNS
* IP
* MAC
* L_SEEN
* REPO
* CONTENT (Plugin output or search query output)

For example. including `-c "DNS, MAC, L_SEEN, CONTENT"` with the program call will filter in only these datapoints, not returning the IP address and repository. Similarly, `-c CONTENT` will make the program only return the plugin output" 

### Features
#### Search Queries
Tenable Security Center Ferret allows for special queries for all plugins. This gives the user more control over how they wish to retrieve the plugin output. A text file (.txt) with newline separated words can be used to specify which word to query. For example, if one was interested in `gcc`, `make`, and `python` on different hosts, the text file would look like:
```
gcc
make
python
``` 
User can also use regular expression for search query. The program will look for characters that match with the regular expression. If the regular expression search finds a result inside the line being searched the program includes the line in the output. The user does not have to specify the program to use regex search. But the user has to be careful while using search queries that contains characters used in regular expression syntax. Such characters have to be escaped using a back slash `\`.  

#### Highlight on hosts not scanned recently
TSC Feret is able to highlight the hosts that have not been scanned for a week. This feature is enabled for HTML and PDF outputs. The font color of the hosts not scanned within a week is set to red. Users can then easily start investigating dead hosts. However, this feature is disabled if the user wants the output data to be presented in specific columns they want. 



#### Config File
Users can save their choice of arguments and credentials in config files that can be read by TSC Ferret to easily query the scan results. The config file can have any name and should be fed in the format `python run.py -C CONFIG_FILE` where `CONFIG_FILE` is the name of the file that has the user's choices in json format. 
A config file can be generated using the script `config_gen.py` which can be run using the command `python config_gen.py`. This script asks the user for choices interactively and stores them in a file with the name specified by user. Note: password is base64 encoded, and thus the config file should not be shared with others, as they will have access to your stored password.

__Note: the configuration file stores a base64 encoded version of the password. **This is not secure.** Unless running the application locally, all those with access to the host running TSC Ferret will be able to decode your password__

A dummy account has been set up without critical permissions in order to run this script. Email yoji(dot)watanabe(at)tufts(dot)edu for account credentials.

* Example config file: Output as CSV file, retrieving plugin 10180 data on hosts belonging to repositories listed in repos.txt

```
{"user": "jane_doe", 
 "pass": "base_64_is_not_encryption", 
 "duplicates": false, 
 "host_list": "", 
 "plugin_id": "10180", 
 "output": "csv", 
 "search_list": "", 
 "repo_list": "repos.txt", 
 "ip_range": "",
 "columns": ""}
```


#### Emailing Results
The user can choose to email the resulting table (in CSV or HTML format) to a list of recipients. This is done by connecting to a user-specified SMTP server, specified in the global variables in `email_results.py` lines 19, 20. Recipients are added in line 21. Results are sent as an email attachment along with a short summary of the query in the body of the email. 
(Note: some email providers may filter these reports as spam/junk)

### Examples Use Cases
* Find all software running on hosts (plugin 22869):
```
python run.py -P 22869
```
* Find certain software, specified in programs.txt, running on hosts, output as pdf:
```
python run.py -s programs.txt -o pdf -P 22869
```
* Find software version history on host 127.0.0.1 (plugin 22869) an only display plugin output:
```
python run.py -d -i 127.0.0.1/32 -c CONTENT -P 22869
```
* Find if hosts in the `win01dev-repository` (repository name saved to the repo_list text file) are ARP, ICMP, TCP, or UDP ping-able by Nessus, email results in a JSON file:
```
python -e run.py -P 10180 -R repo_list -o json
```
