#!/bin/bash

#set your desired test variables up here or through buildspec files
RULES=(
  #'./rules/rule1.rules' 'Rule 1 Name'
  #'./rules/rule2.rules' 'Rule 2 Name'
  './rules/test-exploit-zerologon.rules' 'ET EXPLOIT Possible Zerologon NetrServerAuthenticate'
)

PCAPS=(
  #'./tests/pcap1.pcap'
  #'./tests/pcap2.pcap'
  '/tests/cve-2020-1472-exploit.pcap'
)

#iterate through everything
for i in "${!RULES[@]}"; do
  RULE_FILE=${RULES[$i]}
  RULE_NAME=${RULES[$i+1]}  
  for PCAP in "${PCAPS[@]}"; do
    
    #actual test execution
    suricata -c suricata.yaml -r $PCAP -S $RULE_FILE > /dev/null
    
    #validate the test
    RESULTS=$(grep -i "$RULE_NAME" fast.log | wc -l)  
    if [[ $RESULTS -ge 1 ]]; then
      echo "PASSED: $RULE_NAME matched $PCAP"
    else
      echo "FAILED: $RULE_NAME did not match $PCAP"
    fi

  done
done

