#!/bin/sh
# get data from hadoop
# $1 ht eusername of the remote machine
# $2 the ip address of the remote machine
# $3 the path to aws cli credentials. BCFL to the / and \ => exemple : "C:/Users/Audric/.aws" work but "C:\Users\Audric\.aws" doesn't
./import_data.sh
# set credentiels on the remote machine
./aws_handler.sh $1 $2 $3
# send data models and server file on the remote machine
./send_data_Vm.sh $1 $2