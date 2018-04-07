# DNS-Updater
This docker container finds the external IP of the current container and updates a configured AWS Route 53 DNS entry.

# Usage
```
docker create \
-e AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> \
-e AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> \
-e HOSTED_ZONE_ID=<HOSTED_ZONE_ID> \
-e DNS_NAME=<DNS_NAME> \
rickshinners/dns-updater-docker
```

# Parameters
* *AWS_ACCESS_KEY_ID* Your AWS access key id
* *AWS_SECRET_ACCESS_KEY* Your AWS secret access key
* *HOSTED_ZONE_ID* The AWS hosted zone id that contains the target dns name
* *DNS_NAME* DNS name to set to the running instance's external IP
* *CRON* The cron schedule on which to run. Defaults to every 5 minutes
* *DNS_TTL* TTL in seconds for the DNS record.  Defaults to 300
