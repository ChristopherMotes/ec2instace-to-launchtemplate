#!/usr/bin/python
import boto3
import json
import distutils.util
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
privateIpAddress = ec2Dict['PrivateIpAddress']
keyName = ec2Dict['KeyName']
securityGroups = ec2Dict['SecurityGroups']
subnetId = ec2Dict['SubnetId']
instanceType = ec2Dict['InstanceType']
instanceProfile = ec2Dict['IamInstanceProfile']['Arn']
tags = ec2Dict['Tags']

response = ec2Client.create_launch_template(
    LaunchTemplateName='testtemplate',
    LaunchTemplateData={
        'EbsOptimized': ebsOptimized,
        'IamInstanceProfile': {
            'Arn': instanceProfile,
        },
        'InstanceType': instanceType,
        'KeyName': keyName,
        'Monitoring': {
        },
        'InstanceInitiatedShutdownBehavior': 'stop',
        'NetworkInterfaces': [
            {
                'Groups': [
                    'sg-1c499461',
                ],
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
                        'Value': 'motes'
                    },
                ]
            },
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Motes'
                    },
                ]
            }
        ],
        'SecurityGroupIds': [
            'sg-1c499461',
        ]
    }
)
