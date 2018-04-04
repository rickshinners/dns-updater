#!/usr/bin/env python

# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# HOSTED_ZONE_ID
# DNS_NAME
# DNS_TTL: Default 300
# CRON: Default every minute (UTC times)

import os
import ipgetter
from crontab import CronTab
from time import sleep

required_env = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'HOSTED_ZONE_ID', 'DNS_NAME']
for env in required_env:
    if(os.getenv(env) == None):
        raise Exception("The environment variable %s must be set" % env)

# print(ipgetter.myip())

schedule = CronTab(os.getenv('CRON', '* * * * *'))
while(True):
    sleep(schedule.next(default_utc=True))
    print("Check IP")