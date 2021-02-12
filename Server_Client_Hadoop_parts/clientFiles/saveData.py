# PBD_1: Richard DROGO & Audric MERLEY.
# This script is used to read the summaries matching results calculated by AWS EC2 and store them in a mongoDb Database.
# The MongoDb Server must be running before this program gets executed!
# The MongoDb Server can be lauched executing "C:\Program Files\MongoDB\Server\4.4\bin\mongod.exe" with "4.4" to be replaced by your version.


# BEGIN: IMPORTS
from pymongo import MongoClient # To connect with the MongoDb Server. [INSTALLATION] pip install pymongo
import json		                # To parse the AWS results into a json object.
import pandas as pd             # To parse the CSV and do basic operations. [INSTALLATION] pip install pandas
# END: IMPORTS

class SaveDate :
    # BEGIN: CONFIGURATION
    self.RATES_COLUMN_NAME = "Rates"
    self.ROUNDED_AT_DECIMAL = 4
    def _init__(self,hostname = 'localhost',port = 27017,database_name = "bigDataProjectDb", collection_name = "summaryMatchingResults"):
        self.client = MongoClient(hostname, port)    # We connect to the MongoDb Server
        self.db = client[database_name]
        self.collection = db[collection_name]
    # END: CONFIGURATION
    

    def transfert(self,filename):
        succes = False
        try :
            with open(filename,encoding='utf-8') as resultFile:
                resultsDf = pd.read_csv(resultFile)     # We read the file
                resultsDf[resultsDf.columns[1:resultsDf.columns.size]] = resultsDf[resultsDf.columns[1:resultsDf.columns.size]] * 100
                resultsDf = round(resultsDf,self.ROUNDED_AT_DECIMAL)
                
                # We create a list in which we store for each row, the corresponding JSON document.
                matchingResults = []
                for row in range(resultsDf.shape[0]):
                    matchingResult = {}
                    matchingResult[resultsDf.columns[0]] = resultsDf[resultsDf.columns[0]][row]
                    rates = {}
                    for column in resultsDf.columns[1:resultsDf.columns.size]:
                        rates[column] = resultsDf[column][row]
                    matchingResult[self.RATES_COLUMN_NAME] = rates
                    matchingResults.append(matchingResult)
                
                for summaryMatchingResult in matchingResults: # We insert all the data.
                    self.collection.insert_one(summaryMatchingResult)
                success = True
        except:
            return False
        return succes
