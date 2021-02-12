Client side READ ME:
In this repertory, you will find 6 files :
	> 3 Python scripts 
		>> DataBaseClient.py
			The most important, it represents the client. Run it to communicate with the server
		>> AWSHandler.py
			Class that will handle everything that is connected to aws. Create new SQS Queues/Bucket if needed
		>> saveData.py
			Class that will handle the connection between the predicted csv retrieved and the project front (fill a mongoDB dataBase)
	> test.csv 
		Can be used as a csv exemple to send to the server
	> configure.txt
		Use to configure the bucket if needed. Inside is the name of the last bucket retreieve (manually)
	> the READ-ME

How to use them:
> Just need to run' python DataBaseClient.py file_name.csv
with file_name representing the description : 1 column header = "Summary"

> In the end, it will stock a test_predict.csv on the current repentory and transfer the data to the mongoDB
> If everything went alright, a success message is send.