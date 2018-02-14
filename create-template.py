#!/usr/bin/python
import boto3
import json
import distutils.util
import argparse

parser = argparse.ArgumentParser(description='Required Inputs to create template')
parser.add_argument('--instance-id', nargs=1, required=True)
parser.add_argument('--template-name', nargs=1, required=True)
args = parser.parse_args()
instanceId = args.instance_id[0]
templateName = args.template_name[0]
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
privateIpAddress = ec2Dict['PrivateIpAddress']
keyName = ec2Dict['KeyName']
subnetId = ec2Dict['SubnetId']
instanceType = ec2Dict['InstanceType']
instanceProfile = ec2Dict['IamInstanceProfile']['Arn']
securityGroups = []
for sg in ec2Dict['SecurityGroups']:
   securityGroups.append(sg['GroupId'])
tags = []
for x  in ec2Dict['Tags']:
   if not x['Key'].startswith('aws:'):
      tags.append(x)
   if x['Key'] == "Name":
      NameTag =  x['Value']

response = ec2Client.create_launch_template(
    LaunchTemplateName=templateName,
    LaunchTemplateData={
        'EbsOptimized': ebsOptimized,
        'DisableApiTermination': True,
        'IamInstanceProfile': {
            'Arn': instanceProfile,
        },
        'InstanceType': instanceType,
        'KeyName': keyName,
        'Monitoring': {
            'Enabled': True
        },
        'InstanceInitiatedShutdownBehavior': 'stop',
        'NetworkInterfaces': [
            {
                'PrivateIpAddress': privateIpAddress,
                'SubnetId': subnetId
            },
        ],
        'TagSpecifications': [
            {
                'ResourceType': 'volume',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': NameTag
                    },
                ]
            },
            {
                'ResourceType': 'instance',
                'Tags': tags
            }
        ],
        'SecurityGroupIds': securityGroups
    }
)
