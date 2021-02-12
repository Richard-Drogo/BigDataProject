#!/bin/sh
if [ $# -gt 0 ]
then
	ssh -t $1@$2 'curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && sudo ./aws/install && sudo rm awscliv2.zip'
	ssh -t $1@$2 'sudo mkdir ./.aws/ && sudo aws configure set aws_access_key_id ASIARHMD34J322VUCS7G && sudo aws configure set aws_access_key_id region "us-east-1"'
	scp $3/* $1@$2:./
	ssh -t $1@$2 'sudo mv config ./.aws/config && sudo mv credentials ./.aws/credentials'
	
else

  echo "No argument provided to the script."

fi