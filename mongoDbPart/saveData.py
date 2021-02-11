# PBD_1: Richard DROGO & Audric MERLEY.
# This script is used to read the summaries matching results calculated by AWS EC2 and store them in a mongoDb Database.
# The MongoDb Server must be running before this program gets executed!
# The MongoDb Server can be lauched executing "C:\Program Files\MongoDB\Server\4.4\bin\mongod.exe" with "4.4" to be replaced by your version.


# BEGIN: IMPORTS
from pymongo import MongoClient # To connect with the MongoDb Server. [INSTALLATION] pip install pymongo
import json		                # To parse the AWS results into a json object.
import pandas as pd             # To parse the CSV and do basic operations. [INSTALLATION] pip install pandas
# END: IMPORTS


# BEGIN: CONFIGURATION
HOSTNAME = 'localhost'
PORT = 27017
DATABASE_NAME = "bigDataProjectDb"
COLLECTION_NAME = "summaryMatchingResults"
RESULTS_RELATIVE_PATH = "results.csv" # With this value, we assume that the result file is in the same directory.
RATES_COLUMN_NAME = "Rates"
MESSAGE_ERROR = "Something got wrong..."
MESSAGE_SUCCESS = "Success."

ROUNDED_AT_DECIMAL = 4
# END: CONFIGURATION


# BEGIN: PROCESS
success = False
with open(RESULTS_RELATIVE_PATH) as resultFile:
    resultsDf = pd.read_csv(resultFile)     # We read the file
    resultsDf[resultsDf.columns[1:resultsDf.columns.size]] = resultsDf[resultsDf.columns[1:resultsDf.columns.size]] * 100
    resultsDf = round(resultsDf,ROUNDED_AT_DECIMAL)
    
    # We create a list in which we store for each row, the corresponding JSON document.
    matchingResults = []
    for row in range(resultsDf.shape[0]):
        matchingResult = {}
        matchingResult[resultsDf.columns[0]] = resultsDf[resultsDf.columns[0]][row]
        rates = {}
        for column in resultsDf.columns[1:resultsDf.columns.size]:
            rates[column] = resultsDf[column][row]
        matchingResult[RATES_COLUMN_NAME] = rates
        matchingResults.append(matchingResult)

    client = MongoClient(HOSTNAME, PORT)    # We connect to the MongoDb Server
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    for summaryMatchingResult in matchingResults: # We insert all the data.
        collection.insert_one(summaryMatchingResult)
    success = True
# END: PROCESS


# BEGIN: DISPLAY
if(success):
    print(MESSAGE_SUCCESS)
else:
    print(MESSAGE_ERROR)
# END: DISPLAY