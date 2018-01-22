#!/usr/bin/env python

import argparse
import json
import os
from string import Template
from subprocess import call

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config")
    parser.add_argument("-i", "--ip")
    return parser.parse_args()

def get_changebatch(dnsname, ipaddress):
    template = Template("""
{
    "Comment": "Updating dns entries to $ipaddress",
    "Changes": [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": "$dnsname",
                "Type": "A",
                "TTL": 300,
                "ResourceRecords": [
                    {
                        "Value": "$ipaddress"
                    }
                ]
            }
        }
    ]
}""")
    d = {'dnsname':config['dnsname'], 'ipaddress': args.ip}
    return template.substitute(d)

args = parse_args()
if args.config is None or not os.path.isfile(args.config):
    raise Exception("You must provide a config file")
if args.ip is None:
    raise Exception("You must provide an ip address")
config = json.load(open(args.config))
changebatch = get_changebatch(config['dnsname'], args.ip)

aws_env = os.environ.copy()
aws_env['AWS_ACCESS_KEY_ID'] = config['accesskeyid']
aws_env['AWS_SECRET_ACCESS_KEY'] = config['secretaccesskey']
call(['aws', 'route53', 'change-resource-record-sets', '--hosted-zone-id', config['hostedzoneid'], '--change-batch', changebatch], env=aws_env)