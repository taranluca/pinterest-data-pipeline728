# pinterest-data-pipeline728

## Scope
Pinterest crunches billions of data points every day to decide how to provide more value to their users.
The purpose of this project is to create a similar system using the AWS cloud.


## Contents

### db_creds.yaml
necessary credential file included in the .gitignore to run the scripts

#### There are three Python scripts that collect the pinterest data in different ways.

### 1. user_posting_emulation.py
This is a batch processing unit it requires a configures AWS EC2 instance and uses Apache Kafka Client machine
This data is then sent to Databrick for processing where it is cleaned and then able to be queried using SQL

### 2. user_posting_emulation_streaming.py
This is a streaming process using Kinesis and AWS API proxy integration
This data is then set up to be streamed into Databrick for processing where it is cleaned and then able to be queried using SQL

### 3. 0afffbed4f09_day.py
This is a Python script that is a DAG used for a scheduled airflow task. This DAG runs a Databricks notebook once a day at midnight



## System Requirements
1. You will need a machine and software capable of running Python scripts such as VSC
2. You need to be able to run Bash commands as well if you are on windows make sure you have git Bash or similar

## Installation
1. Download the entire repository on your local machine
2. Opening the python scripts there are a list of modules that need to be installed into a virtual environment
    #### 3. Running the Rest Proxy
    1. Working in Git Bash navigate to the directory where you have downloaded this repo
    2. Run this code in Git Bash terminal
    ssh -i "0afffbed4f09-key-pair.pem" ec2-user@ec2-54-81-162-124.compute-1.amazonaws.com
    3. Once run sucesfully you should have this new base [ec2-user@ip-172-31-32-252 ~]
    4. run the following command
    cd confluent-7.2.0/bin
    5. Then run the command
    ./kafka-rest-start /home/ec2-user/confluent-7.2.0/etc/kafka-rest/kafka-rest.properties
    6. This will activate the Proxy and it will await a response from the user_posting_emulation.py

4. Keeping the proxy open the user_posting_emulation.py script can then be run. You will see the proxy injesting data
5. Closing the proxy the user_posting_emulation_streaming.py can be run

## Information about the collected data
The dataset pinterest_data that is taken from pinterest is split up into three separate datasets
### 1. pin data
This contains data about posts being updated to Pinterest
### 2. geo data
This contains data about the geolocation of each Pinterest post
### 3. user data
This contains data about the user that has uploaded each post

