#!/bin/sh

CONFIG_DIR=/config
PREVIOUS_IP_FILE=$CONFIG_DIR/previous-ip
CONFIG_FILE=$CONFIG_DIR/config.json
ROUTE53_UPDATE_SCRIPT=/update-route53.py

date

CURRENT_IP=`python -m ipgetter`
echo "Current IP:" $CURRENT_IP

if [ -f $PREVIOUS_IP_FILE ]; then
    PREVIOUS_IP=$(head -n 1 $PREVIOUS_IP_FILE)
    if [ "$CURRENT_IP" = "$PREVIOUS_IP" ]; then
        echo "Previous IP is the same as current, exiting"
        exit 0
    fi
fi

echo "Updating DNS..."
$ROUTE53_UPDATE_SCRIPT --config $CONFIG_FILE --ip $CURRENT_IP

echo $CURRENT_IP > $PREVIOUS_IP_FILE