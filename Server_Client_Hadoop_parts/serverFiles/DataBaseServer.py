# va devoir communiquer avec AWS : SQS
# va devoir dl sur le bucket

import os
from os import path
import boto3
from AWSHandler import AWSHandler
from AWSHandler import ParamException
from predicator import Predicator
import pandas as pd

class DataBaseServer:
    def __init__(self,bucket_name):
        self.awsHandler = AWSHandler(bucket_name,True)
        self.model_predicator = Predicator()

    def predictCsv(self, filename):
        self.awsHandler.download_file_from_bucket(filename)
        if path.exists(filename) :
            # predidction
            # send back the new csv
            print(filename)
            csv_values = pd.read_csv(filename)
            rs = self.model_predicator.prediction(csv_values.Summary.values)
            print(rs)
            result_file_name = filename.replace(".csv","_predict.csv")
            rs.to_csv(result_file_name,index = False)
            self.awsHandler.upload_file_to_bucket(result_file_name)
            return {"filename":result_file_name}
        else :
            raise ParamException(filename+"  wasn't download and found on the server")
    
    def get_check_paths_param(self,line,nbr_needed):
        paths = line.split(' ')
        if(len(paths) != nbr_needed):
            raise ParamException("Number of params isn't correct, needed: "+nbr_needed+" | found "+len(paths)+" for cmd line "+line)
        if("" in paths ) :
            raise ParamException("One of the param is null for " + str(paths))
        return paths

    # Function command_function
    # PARAM |
    # cmd [REQUIRED]: string line in the format '-cmd'.
    # content [REQUIRED]: string line with the param of the command.
    # RETURN |
    # Dictionnary in the format {key1 : value1,key2 : value2,....}.
    # EXAMPLE |
    # rep = self.command_function("-predictCSV","toPredict.csv")
    # rep will be {"filename":"resultPredict.csv"}
    def command_function(self,cmd,content):
        if cmd == "-predictCsv":
            filename = self.get_check_paths_param(content,1)
            return self.predictCsv(filename[0])
            #return self.grey_level(paths[0],paths[1])
        else :
            raise ParamException("Command "+content+"unknown")
    
    # Function receive_worker
    # Use infinite loop to check message on the SQS qeue BigDataRequest
    # One a message is caught, will make processing 
    # PARAM |
    # None
    # RETURN |
    # None
    def receive_worker(self):
        print("Waiting...")
        while True :
            for m in self.awsHandler.request_queue.receive_messages(MessageAttributeNames=['ID',"cmd"]):
                response = ""
                #Handle attributes.
                ID = m.message_attributes['ID']['StringValue'] # ID that will be used to link the request with the answer.
                try :
                    cmd = m.message_attributes['cmd']['StringValue']
                    content = m.body
                    print('Message receive :'+content)
                    #Process.
                    response = self.command_function(cmd,content)
                    #Answer back.
                    response = " ".join([k+" "+response[k] for k in response])
                    print("response : "+response)
                except ParamException as exp:
                    response = "FAILED | Error : "+str(exp.args[0])
                except Exception as e:
                    response = "FAILED | Error : "+str(e)
                finally:
                    self.awsHandler.send_message(response,ID)
                    self.awsHandler.removeMessage(m)

def main() :
    bucket_name = "bucketBigDataProject123"
    try :
        with open("configure.txt","r") as f:
            line = f.readline()
            if not line is None and line != "":
                bucket_name = line
    except :
        print("bucket not generated bcs file configure.txt not found")
    dataBaseServer = DataBaseServer(bucket_name)
    dataBaseServer.receive_worker()

if __name__ == "__main__" :
    main()