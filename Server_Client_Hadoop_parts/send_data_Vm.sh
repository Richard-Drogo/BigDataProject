#!/bin/sh
#if param exist
if [ $# -gt 0 ]
then
# create two dir on the remote machine : data and models
	ssh -t $1@$2 'mkdir data && mkdir models'
# import data and models to the newly created directories
	scp import/* $1@$2:data/
	scp models/* $1@$2:models/
# import files used to launch server 
	scp serverFiles/* $1@$2:./
# check and install every libraries needed to run BigDataServer.py
	ssh -t $1@$2 './python_import.sh'
# launch server (doesn't wokr)
	ssh -t $1@$2 'python3 BigDataServer.py'
else

  echo "No argument provided to the script."

fi