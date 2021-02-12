# Represent the client
# it will open 2 sqs queues and will look at a bucket
# To use this python use : > python DataBaseClient file_to_predict


from joblib import dump, load
import os
from os import path
from AWSHandler import AWSHandler
from AWSHandler import ParamException
import random
import sys
import saveData import SaveDate

# represents the client
class Client:
    def __init__(self,bucket_name):
        #handle connections with aws : 
        self.awsHandler = AWSHandler(bucket_name,False)
    
    def receive_response(self,ID):
        # wait for the answer (with good Id)
        while True :
            for m in self.awsHandler.request_queue.receive_messages(MessageAttributeNames=['ID']):
                if ID == m.message_attributes['ID']['StringValue'] :
                    response = m.body
                    self.awsHandler.removeMessage(m) # remove the message from the queue
                    return response

    # Use to communicate with the server : will save the file (filename) in the bucket, then send a request to the server
    # When the server is finished with the csv copied on the bucket, the client will retrived an answer with the filename of the predict file saved  on the bucket. 
    # Client will then save it and transfert it on the base     
    def launch_nlp_processing(self,filename):
        if path.exists(filename) :
            #upload file to bucket
            name = self.awsHandler.upload_file_to_bucket(filename)
            # send message to server to start processing
            ## creation of ID :
            ID = str(random.randrange(0,4000,1))
            self.awsHandler.send_message(name,ID,"-predictCsv")
            response = self.receive_response(ID)
            if "FAIL|" in response :
                print(response)
            else :
                values = response.split(' ')
                if len(values) == 2 :
                    predict_filename = values[1]
                    # download the predicted file on the system with the name result.csv
                    self.awsHandler.download_file_from_bucket(predict_filename,"results.csv")
                    saver = SaveDate()
                    # transfert it to the mongoDB base
                    re = saver.transfert("result.csv")
                    if re :
                        print("Data send to the database")
                    else :
                        print("Error while load/sending data to the database")
                    # handle mongodb fill database
                else :
                    raise ParamException("Error while getting the answer : "+response)
        else :
            raise ParamException(" The file doesn't exist")


def main(filename):
    # initial bucket
    bucket_name = "bucketBigDataProject123"
    try :
        # tries to retrieve a bucket's name in the file configure.txt.
        with open("configure.txt","r") as f:
            line = f.readline()
            if not line is None and line != "":
                bucket_name = line 
    except :
        print("bucket not generated bcs file configure.txt not found")
    client = Client(bucket_name)
    client.launch_nlp_processing(filename)

if __name__ == "__main__" :
    argument1 = sys.argv[1]
    main(argument1)