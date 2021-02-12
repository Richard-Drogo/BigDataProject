# BigDataProject
Repository of TSE's S9 BigData Project using Hadoop, AWS EC2, AWS S3 and MongoDb

## FR


### Setup the MongoDb
You need to have python downloaded: https://www.python.org/downloads/
You need to have the following modules:
	* pip install pymongo
	* pip install pandas
	
You need to have a mongoDB: https://www.mongodb.com/try/download/community
Launch your mongoDb on Windows according to your {VERSION}: "C:\Program Files\MongoDB\Server\{VERSION}\bin\mongod.exe
Create a database with name: bigDataProjectDb
Create a collection: summaryMatchingResults


### Setup the nodeJs Express server to see the results
You need to have nodeJs installed: https://nodejs.org/en/download/
Go to the "front" folder, and do the command: node index.js
You will then be able to show the results on localhost:3000 upon arrival.


### Send csv data to be analyzed for matching