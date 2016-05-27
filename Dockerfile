FROM empiricalresults/minimal-python3:latest


RUN mkdir /code
WORKDIR /code

ADD setup.py /code
#RUN pip install -e .
RUN python3 setup.py develop

ADD aiobeanstalk /code/aiobeanstalk

