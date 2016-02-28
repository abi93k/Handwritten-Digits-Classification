import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from os import listdir
from os.path import isfile, join, isdir
import sys

def switch_row(x):
    return {
        '4': 8,
        '8': 9,
        '12': 10,
        '16': 11,
        '20': 12,
    }[x]

def switch_col(x):
    return {
    	'0.0': 'B',
        '0.1': 'C',
        '0.2': 'D',
        '0.3': 'E',
        '0.4': 'F',
        '0.5': 'G',
        '0.6': 'H',
        '0.7': 'I',
        '0.8': 'J',
        '0.9': 'K',
        '1.0': 'L',
    }[x]    

def panic(message):
	print "setup failed..."
	print message
	print "exiting..."
	exit()

print "setting up..."
if(len(sys.argv)!=2):
	panic("usage: python tabulate.py <path_to_log_directory>")

results_path = sys.argv[1]

if(not isdir(results_path)):
	panic("invalid log directory")

results = [f for f in listdir(results_path) if isfile(join(results_path, f))]

if(len(results)==0):
	panic("no log files found in "+results_path)	

api_keys_file = 'google_api_keys.json'

if(not isfile(api_keys_file)):
	panic("api keys file "+api_keys_file+" not found")

json_key = json.load(open(api_keys_file))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

gc = gspread.authorize(credentials)

wks = gc.open("Programming Assignment I - Report Graphs").sheet1

print "working..."
for result in results:
	f=open(results_path+result,'r')
	print "tabulating results in "+result+"..."
	values = f.readline().split(",")

	training_row = int(switch_row(values[0]))
	col = switch_col(values[1])

	validation_row = int(switch_row(values[0])) + 9

	testing_row = int(switch_row(values[0])) + 18

	time_row = int(switch_row(values[0])) + 27

	training_cell = str(col)+str(training_row)
	validation_cell = str(col)+str(validation_row)
	testing_cell = str(col)+str(testing_row)
	time_cell = str(col)+str(time_row)

	wks.update_acell(training_cell, values[2]+"%")
	wks.update_acell(validation_cell, values[3]+"%")
	wks.update_acell(testing_cell, values[4]+"%")
	wks.update_acell(time_cell, values[5])

	f.close()

print "done..."



