#!/usr/bin/env python3
import csv, os, time, glob
#original pcaps oulled from https://github.com/CERTCC/PoC-Exploits/blob/master/cve-2020-1472/cve-2020-1472-exploit.pcap
#parse buildspec.csv
#format required: '/path/to/rule/file.rules','NAME OF RULE TO TEST','/path/to/pcap/test.pcap'
csv_handle = open('buildspec.csv')
reader = csv.reader(csv_handle)
for row in reader:
    rule_file = row[0]
    rule_name = row[1]
    pcap = row[2]

    #touch equivalent fast.log even if one isnt generated so we can make it to the validation logic
    file_handle = open('fast.log', 'w')
    file_handle.close()

    # Run suricata 
    cmd = f"suricata -c suricata-config.yml -r {pcap} -S {rule_file}"
    os.system(cmd)

    #let file system catch up
    time.sleep(1)
    
    #validation logic
    file_handle = open('fast.log', 'r', encoding='UTF-8')
    content = file_handle.read()
    rule_name = rule_name.replace("'", '')
    try:
        if rule_name in content:
            print(f"PASSED: {rule_name} found in {pcap}") 
        else:
            print(f"FAILED: {rule_name} not detected with {pcap}")
            file_handle.close()
            exit(1)
    except ValueError:
       print('Test failed, exiting')
       file_handle.close()
       exit(1)

#clean up old files if this is self-hosted
for logfile in glob.glob('./*.log'):
    print('Deleting: ' + str(logfile))
    os.remove(logfile)