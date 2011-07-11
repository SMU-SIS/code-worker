#!/usr/bin/env python
# analysis.py
# Author: Philip Pang
# This script will be run to analyse the repo downloaded to server



import os, sys, json
import subprocess
import getopt

JSON_OUTPUT_FILE = "job-results.json"
ANALYSIS_OUTPUT = {}


def main(argv):
    

    target = ""
    
    # Getopt method to read the argument and execute the relevant functions
    try:                                
        opts, args = getopt.getopt(argv, "", ["help", "target=", "type=", "master="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == "--help":
            usage()
        elif opt == "--target":
            # Store the targeted repo to be analyze in target variable
            target = arg
        elif opt == "--master":
            print "master"
            print " " + arg
        elif opt == "--type":
            
            # check the command to see what type of analysis is requested
            if arg.lower() == "pep8":
                
                run_pep8_count(target)
                run_pep8_style(target)
                
    # Output from analysis were output to job-results.json
    output_to_json_file(ANALYSIS_OUTPUT)


def run_pep8_style(target, path="tasks\\pep8"):
    print os.path.abspath(path)
    pep_style = subprocess.Popen("python " + os.path.abspath(path) + "\\pep8.py --ignore=E111,E501 --filename=*.py " + target, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    style = pep_style.communicate()[0]
    ANALYSIS_OUTPUT['PEP8-Style'] = style


def run_pep8_count(target, path="tasks\\pep8"):
    pep_count = subprocess.Popen("python "  + os.path.abspath(path) +  "\\pep8.py --ignore=E111,E501 --count -qq --filename=*.py  " + target, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    count = pep_count.communicate()[1]
    ANALYSIS_OUTPUT['PEP8-Issues'] = count


def output_to_json_file(json_data, json_file=JSON_OUTPUT_FILE, permission='a', path=''):
    with open(os.path.abspath(path+json_file), permission) as fp:
        json.dump(json_data, fp, indent=2)
    print json_file + ' updated'

    
def load_from_json_file(json_file=JSON_OUTPUT_FILE, path='json\\'):
    with open(os.path.abspath(path+json_file), permission) as fp:
        data_string = json.load(fp)
    print 'JSON Output:' + data_string
    return data_string

    
def usage():
    usage = '''
    --help                 Prints this
    --target               Specify the target folder
    --type                 Chose from a list of things to do
    --master               ???
    '''
    print usage


if __name__ == "__main__":
    
    # Display help menu to user if no argument was found
    if len(sys.argv) == 1:
        usage()
    # Read all the arguments from the command prompt and run in the main method
    main(sys.argv[1:])
    
    