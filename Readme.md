# DNS-Updater
This docker container finds the external IP of the current container and updates a configured AWS Route 53 DNS entry.

## Setup
The image requires a `config.json` file to be mounted in the `/config` mount point.  You can see an example config file at `config.json.example`

## Quick start
1. `docker build . -t dns-updater`
2. `mkdir config`
3. `cp config.json.example config/config.json`
4. `# Fill out config.json`
2. `docker run --rm -v ./config:/config dns-updater`