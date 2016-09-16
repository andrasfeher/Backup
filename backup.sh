#! /bin/bash

if [ `./directory_digest.py /home/andras/Dropbox/Python` == "1" ]
then
  echo 'Changed'
else
  echo 'Not changed'
fi
