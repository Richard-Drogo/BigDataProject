import os
from os import path
import boto3

class ParamException(Exception):
    pass

class AWSHandler :
    def __init__(self,bucket_name,server_mode = True):
        self.sqs_client = boto3.client('sqs',region_name="us-east-1") # Init sqs_client : used to list ,create SQS queue and delete messages. 
        self.bucket_client = boto3.client('s3',region_name="us-east-1")# Init bucket_client : used to list ,create bucket and uploading log files. 
        self.sqs = boto3.resource('sqs',region_name="us-east-1") # Init sqs : used to get SQS queue by the url/name.
        self.request_queue = None # Queue used to send request to server.
        self.response_queue = None # Queue used to get answer from the server.
        self.bucket = bucket_name #Bucket name where csv values and results will be saved.
        self.init_queues(server_mode) # Init of requestQueue and responseQueue.
        self.init_bucket() # Init of bucket

    # Function init_queues
    # Test if SQS queues BigDataRequest and BigDataResponse already exist.
    # If they don't, it will create them.
    def init_queues(self,serverMode = True):
        queues =  self.sqs_client.list_queues(QueueNamePrefix='BigDataRe')
        response_queue_created = False
        request_queue_created = False
        if("QueueUrls" in queues):
            for url in queues['QueueUrls'] :
                response_queue_created = response_queue_created or (url == 'BigDataResponse')
                request_queue_created = request_queue_created or (url == 'BigDataRequest')
                if(response_queue_created and request_queue_created) :
                    break
        if (not response_queue_created) :
            self.sqs_client.create_queue(QueueName='BigDataResponse')
        if(not request_queue_created) :
            self.sqs_client.create_queue(QueueName='BigDataRequest')
        if(serverMode) :
            self.request_queue = self.sqs.get_queue_by_name(QueueName='BigDataRequest')
            self.response_queue = self.sqs.get_queue_by_name(QueueName='BigDataResponse')
        else :
            self.request_queue = self.sqs.get_queue_by_name(QueueName='BigDataResponse')
            self.response_queue = self.sqs.get_queue_by_name(QueueName='BigDataRequest')

    # Function init_bucket
    # Test if bucket BigDataBucket already exists.
    # If it doesn't, it will create it.
    def init_bucket(self):
        buckets = self.bucket_client.list_buckets()
        bucket_created = False
        for bucket in buckets['Buckets']:
            if(bucket["Name"] == self.bucket) :
                bucket_created = True
                break
        if(not bucket_created):
            self.bucket_client.create_bucket(Bucket=self.bucket)
              
    # Function send_message  
    # PARAM |
    # content [REQUIRED]: string with the answer to send back.
    # ID [REQUIRED]: number used to link the request with this answer.
    # EXAMPLE |
    # self.create_response(self.create_response("predict done",5)
    def send_message(self,content,ID,cmd = ""):
        attributes = {'ID': {
            'StringValue': str(ID),
            'DataType': 'String'
        }}
        if cmd != "" :
            attributes['cmd'] = {
                'StringValue': cmd,
                'DataType':'String'
            }
        self.response_queue.send_message(MessageBody=content,MessageAttributes=attributes)

    # Function upload_file_to_bucket  
    # PARAM |
    # filename [REQUIRED]: file path on the computer.
    # dst_file : the name of the file in the bucket. By default it's the same as the filename
    def upload_file_to_bucket(self,filename,dst_file = ""):
        dst_file = filename if dst_file == "" else dst_file
        self.bucket_client.upload_file(filename,self.bucket,dst_file)

    # Function download_file_from_bucket  
    # PARAM |
    # filename [REQUIRED]: file name in the bucket. The file will be download with the same name on the computer. Repertory is the one of this file
    def download_file_from_bucket(self,filename):
        self.bucket_client.download_file(self.bucket, filename, filename)

    def removeMessage(self,message) :
        if not message is None:
            self.sqs_client.delete_message(QueueUrl = message.queue_url,ReceiptHandle = message.receipt_handle)