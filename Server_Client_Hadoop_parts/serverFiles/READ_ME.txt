Server side READ ME:
In this repertory, you will find 6 files :
	> 3 Python scripts 
		>> DataBaseServer.py
			The most important, it represents the server. Once running,it will retrieve message and process them.
		>> AWSHandler.py
			Class that will handle everything that is connected to aws. Create new SQS Queues/Bucket if needed
		>> predicator.py
			Class that will handle the prediction with the model
	> python_import.sh
		Lots of import must be done on the server. To reduce the time, execute it on the server Machine, it will do basic install command to import everything needed
		To use it: >python_import.sh
	> configure.txt
		Use to configure the bucket if needed. Inside is the name of the last bucket retrieve (manually)
	> the READ-ME

How to use them:
On the server machine :
	> python_import.sh
	> python DataBaseServerfile.py

If everything went alright, the server is waiting for processing incoming request.(aws cli credentials must be used before)