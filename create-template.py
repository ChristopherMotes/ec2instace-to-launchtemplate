#!/usr/bin/python
import boto3
import json
import argparse

parser = argparse.ArgumentParser(description='Required Inputs to create template')
parser.add_argument('--instance-id', nargs=1, required=True)
args = parser.parse_args()

ec2Client = boto3.client('ec2')

