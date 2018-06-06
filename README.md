# SoftwareCompare
## Yoji Watanabe & Saurav Gyawali
Using Tenable Security Center's software enumeration plugin (PluginID 22869), automatically compare software versions across all scanned hosts. User can specify a list of programs they are interested in, where the script can then identify them in scanned hosts. Requires a valid Tenable Security Center account.
***

### Usage
1. Enter input data into a text file named `programs.txt`, or specify the input file in the `processDump.py/` global variables.
2. Enter Tenable Security Center host URL in the `dumpPluginOut.py` global variables
3. Execute `run.py` and follow on-screen prompts

### Input Data
A text file ('programs.txt') with newline separated words can be used to specify which programs to query. For example, if one was interested in the versions of `gcc`, `make`, and `python` running on the different hosts, the `program.txt` file would look like:
```
gcc
make
python
``` 

