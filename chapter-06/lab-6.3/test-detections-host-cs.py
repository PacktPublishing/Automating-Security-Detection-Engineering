#!/usr/bin/env python3
import os, json, statistics
from datetime import datetime, timedelta
from falconpy import APIHarnessV2

#secrets must be injected at test time from the CI runner
CS_CLIENT_ID = os.environ.get('CS_CLIENT_ID')
CS_CLIENT_SECRET = os.environ.get('CS_CLIENT_SECRET')


def getDetections(tested_host_name, num_hours_lookback):
    #type cast the user input
    host_name = str(tested_host_name)
    num_hours = int(num_hours_lookback)

    #construct the API client
    falcon = APIHarnessV2(client_id=CS_CLIENT_ID, client_secret=CS_CLIENT_SECRET)

    #strtime fmt requirement lookback for cs timestamps
    current_time = datetime.now()
    last_hrs = current_time - timedelta(hours=num_hours)
    lookup_time = last_hrs.strftime("%Y-%m-%dT%H:%M:%SZ")
    #print(lookup_time)

    filter_query = f"last_behavior:<='{lookup_time}', device.hostname:'{host_name}'"
    #filter_query = f"device.hostname:'{host_name}'"

    response = falcon.command("QueryDetects", 
                            offset=0, 
                            limit=50, 
                            sort="last_behavior|desc",
                            filter=filter_query
                            )

    #print(type(response))
    detectid_values_list = response['body']['resources']

    BODY = {
        "ids": detectid_values_list
    }

    response = falcon.command("GetDetectSummaries", body=BODY)
    #returned json sometimes has non complianct chars need to scrub them
    response = json.dumps(response) #converts to string
    response = json.loads(response) #converts back to json compatible dictionary
    #print(type(response))

    #aggregate multiple detections where applicable
    cmdline_list = []
    tactic_id_list = []
    display_name_list = []
    severity_list = []
    confidence_list = []

    if response['status_code'] in range(200,299): #in case they add 2XX additional states in future
        for resource in response['body']['resources']:
            for behavior in resource['behaviors']:
                cmdline = behavior['cmdline']
                tactic_id = behavior['tactic_id']
                display_name = behavior['display_name']
                severity = behavior['severity']  # integer
                confidence = behavior['confidence']  # integer
                #add to respective lists for return later
                cmdline_list.append(cmdline)
                tactic_id_list.append(tactic_id)
                display_name_list.append(display_name)
                severity_list.append(severity)
                confidence_list.append(confidence)
    #return cmdline, tactic_id, display_name, severity, confidence #use for first or single detections
    return cmdline_list, tactic_id_list, display_name_list, severity_list, confidence_list #returns position tuples

#driver main
if __name__ == '__main__': 
    #for the lab we are running the self hosted runner on the same 'test' host
    #in prod you should separate these and execute via ssh keys remotely
    ### TEST PARAMETER SPECIFICS ###
    host_name = "dc-ubuntu"
    results = getDetections(host_name, 4)

    ### TEST CRITERIA ###
    #print if you want to debug exceptions in the CI logs easier
    print(results)

    #example if your overrall detections are based on ML or fuzzy you can use averages pending EDR
    if statistics.mean(results[4]) >=80:
        print('EDR confidence score disposition ok')
        if 'CurlWgetMalwareDownload' in results[2]:
            print('end-to-end test successful')
    else: 
        print('test did not meet requirement spec')
        exit(1)

#setting job on eval to continue on error try other lolbins