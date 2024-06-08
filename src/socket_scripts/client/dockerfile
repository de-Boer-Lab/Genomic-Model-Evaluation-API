# Get the latest base image for python
FROM python:latest
# Put files at the image '/client/' folder.
ADD ipc-client.py /client/
# '/server/' is base directory
WORKDIR /client/
# execute the command
CMD [ "python3", "/client/ipc-client.py" ]
