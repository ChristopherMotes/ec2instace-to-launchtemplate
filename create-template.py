#!/usr/bin/python
import boto3
import json
import argparse

parser = argparse.ArgumentParser(description='Required Inputs to create template')
parser.add_argument('--instance-id', nargs=1, required=True)
args = parser.parse_args()
instanceId = args.instance_id[0]
ec2Client = boto3.client('ec2')
ec2Dict = ec2Client.describe_instances(
    InstanceIds=[
        instanceId
    ],
) 
ec2Dict = ec2Dict['Reservations'][0]['Instances'][0]
monitoringState = ec2Dict['Monitoring']['State']
ebsOptimized = ec2Dict['EbsOptimized']
vpcId = ec2Dict['VpcId']
keyName = ec2Dict['KeyName']
print monitoringState
print ebsOptimized
print vpcId
print keyName
