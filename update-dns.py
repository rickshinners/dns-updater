#!/usr/bin/env python

import os
from ipgetter2 import ipgetter1 as ipgetter
from crontab import CronTab
from time import sleep
from string import Template
from subprocess import check_output, call
from netaddr import IPNetwork, IPAddress
import logging

def get_logging_level(level):
    return {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
    }[level.upper()]

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(get_logging_level(os.getenv('LOG_LEVEL', 'INFO')))
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.debug('Startup')
logger.info("AWS_ACCESS_KEY_ID=%s" % os.getenv('AWS_ACCESS_KEY_ID'))
logger.info("AWS_HOSTED_ZONE_ID=%s" % os.getenv('AWS_HOSTED_ZONE_ID'))
logger.info("DNS_NAME=%s" % os.getenv('DNS_NAME'))
logger.info("DNS_TTL=%s" % os.getenv('DNS_TTL', 300))
logger.info("CRON=%s" % os.getenv('CRON', '*/5 * * * *'))
logger.info("BLACKLIST=%s" % os.getenv('BLACKLIST'))
logger.info("CIDRMASK=%s" % os.getenv('CIDRMASK'))
logger.info("LOG_LEVEL=%s" % os.getenv('LOG_LEVEL', 'INFO'))

def check_required_environment_variables():
    required_env = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_HOSTED_ZONE_ID', 'DNS_NAME']
    for env in required_env:
        if(os.getenv(env) == None):
            raise Exception("The environment variable %s must be set" % env)

def get_changebatch(dnsname, ipaddress, ttl):
    template = Template("""
{
    "Comment": "Updating $dnsname A record to $ipaddress with a $ttl second TTL",
    "Changes": [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": "$dnsname",
                "Type": "A",
                "TTL": $ttl,
                "ResourceRecords": [
                    {
                        "Value": "$ipaddress"
                    }
                ]
            }
        }
    ]
}""")
    d = {'dnsname':dnsname, 'ipaddress': ipaddress, 'ttl': ttl}
    return template.substitute(d)

def get_current_dns_ip():
    return check_output(['aws', 'route53',
        'test-dns-answer',
        '--hosted-zone-id', os.getenv('AWS_HOSTED_ZONE_ID'),
        '--record-name', os.getenv('DNS_NAME'),
        '--record-type', 'A',
        '--query', 'RecordData[0]',
        '--output', 'text']).decode('utf-8').strip()

def is_ip_in_blacklist(ip):
    if(os.getenv('BLACKLIST') is None):
        return False
    blacklist = os.getenv('BLACKLIST').split(',')
    return ip in blacklist

def is_ip_in_cidrmask(ip):
    if(os.getenv('CIDRMASK') is None):
        return True
    return IPAddress(ip) in IPNetwork(os.getenv('CIDRMASK'))

def check_dns_and_update():
    myip = ipgetter.myip()
    if is_ip_in_blacklist(myip):
        logger.info("Current ip (%s) is blacklisted, skipping update" %(myip))
        return
    if not is_ip_in_cidrmask(myip):
        logger.info("Current ip (%s) is not in the provided CIDR mask, skipping update" %(myip))
        return
    currentdnsip = get_current_dns_ip()
    logger.debug('current external ip: %s' % myip)
    logger.debug('%s resolves to %s' %(os.getenv('DNS_NAME'), currentdnsip))
    if(myip != currentdnsip):
        changebatch = get_changebatch(os.getenv('DNS_NAME'), myip, os.getenv('DNS_TTL',300))
        change_message = check_output(['aws', 'route53',
            'change-resource-record-sets',
            '--hosted-zone-id', os.getenv('AWS_HOSTED_ZONE_ID'),
            '--change-batch', changebatch,
            '--query', 'ChangeInfo.Comment',
            '--output', 'text']).decode('utf-8').strip()
        logger.info(change_message)

check_required_environment_variables()
check_dns_and_update()

schedule = CronTab(os.getenv('CRON', '*/5 * * * *'))
while(True):
    try:
        sleep(schedule.next(default_utc=True))
        check_dns_and_update()
    except KeyboardInterrupt:
        logger.debug("Exiting after KeyboardInterrupt")
        exit(0)