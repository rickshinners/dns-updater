# DNS-Updater
This docker container finds the external IP of the current container and updates a configured AWS Route 53 DNS entry.  The update process runs once at startup and continues based on a cron-like schedule.

# Usage
```
docker create \
-e AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> \
-e AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> \
-e AWS_HOSTED_ZONE_ID=<AWS_HOSTED_ZONE_ID> \
-e DNS_NAME=<DNS_NAME> \
rickshinners/dns-updater
```

# Parameters
* *AWS_ACCESS_KEY_ID* Your AWS access key id
* *AWS_SECRET_ACCESS_KEY* Your AWS secret access key
* *AWS_HOSTED_ZONE_ID* The AWS hosted zone id that contains the target dns name
* *DNS_NAME* DNS name to set to the running instance's external IP
* *CRON* The cron schedule on which to run. Defaults to every 5 minutes. Time is in UTC
* *DNS_TTL* TTL in seconds for the DNS record.  Defaults to 300
* *LOG_LEVEL* Logging level [CRITICAL, ERROR, WARNING, INFO, DEBUG] Defaults to INFO