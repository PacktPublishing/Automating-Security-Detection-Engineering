#!/usr/bin/env python3
import os, json
from datetime import datetime, timedelta
from falconpy import APIHarnessV2

# Get API credentials from environment variables
CS_CLIENT_ID = os.environ.get('CS_CLIENT_ID')
CS_CLIENT_SECRET = os.environ.get('CS_CLIENT_SECRET')

# Set the time range for the detection alert query
current_time = datetime.now()
last4h = current_time - timedelta(hours=4)

lookup_time = last4h.strftime("%Y-%m-%dT%H:%M:%SZ")
#print(lookup_time)

# Do not hardcode API credentials!
falcon = APIHarnessV2(client_id=CS_CLIENT_ID, client_secret=CS_CLIENT_SECRET)

host_name = "dc-ubuntu"

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
#returned json sometimes has non complianct chars
response = json.dumps(response) #converts to string
response = json.loads(response) #converts back to json compatible dictionary
#print(type(response))

if response['status_code'] in range(200,299): #in case they add 2XX additional states in future
    for resource in response['body']['resources']:
        for behavior in resource['behaviors']:
            cmdline = behavior['cmdline']
            tactic_id = behavior['tactic_id']
            display_name = behavior['display_name']
            severity = behavior['severity']  # integer
            confidence = behavior['confidence']  # integer
            print('#### Detections Triggered ####')
            print(f'Cmdline: {cmdline}')
            print(f'Tactic ID: {tactic_id}')
            print(f'Display Name: {display_name}')
            print(f'Severity: {severity}')
            print(f'Confidence: {confidence}')

