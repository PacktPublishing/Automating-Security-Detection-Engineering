#!/bin/bash

#variable
RULE_NAME='ET EXPLOIT Possible Zerologon NetrServerAuthenticate'
RULE_FILE='./rules/test-exploit-zerologon.rules'
TEST_PCAP='./tests/cve-2020-1472-exploit.pcap'

#cleanup logs
rm -rf ./logs/*.log
rm ./*.log

#run suricata tests against pcaps
suricata -c ./suricata-config.yml -r $TEST_PCAP -S $RULE_FILE

#search for alerts
RESULTS=$(grep -i "$RULE_NAME" ./fast.log | wc -l)

if [[ $RESULTS -ge 1 ]]; then
    echo "TEST PASSED: $RULE_NAME matches $TEST_PCAP";
    exit 0 #exits clean
else
    echo "TEST FAILED: $RULE_NAME does NOT match $TEST_PCAP";
    exit 1 #raises its own error
fi

#cleanup logs
rm -rf ./logs/*.log
rm ./*.log


