#!/usr/bin/env python3
from datetime import datetime, timedelta
import boto3, time

#sleeping up to 3 minutes for event detection catchup
print("Sleeping for 1 minute for AWS CloudWatch Metrics to Catch Up...")
time.sleep(60)

#api client construct and assumes you have STS token active
cloudwatch = boto3.client('cloudwatch')

#set variables for your test
namespace = 'AWS/Events'
metric_name = 'MatchedEvents'
rule_name = 'security-iam-access-key-generated'

#aws requires start/end time in strtime UTC format
end_time = datetime.utcnow()
start_time = end_time - timedelta(minutes=15) #obviously change this to something reasonable ~5-20 min

start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
end_time = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

print("Checking Start Time:", start_time)
print("Checking End Time:", end_time)

#use cloudwatch metric query to evaluate results
response = cloudwatch.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'metric_query',
            'MetricStat': {
                'Metric': {
                    'Namespace': namespace,
                    'MetricName': metric_name,
                    'Dimensions': [
                        {
                            'Name': 'RuleName',
                            'Value': rule_name
                        }
                    ]
                },
                'Period': 300,  #use 5 minute intervals as the metric
                'Stat': 'Sum',  #you can change this based on the console
                'Unit': 'Count'
            }
        }
    ],
    StartTime=start_time,
    EndTime=end_time
)

#actual test logic
try:
    if 'MetricDataResults' in response:
        for result in response['MetricDataResults']:
            #print(type(result))
            print(result)
            print(f"Result output: ", result['Values'][0])
            if result['Values'][0] > 0:
                print('Test Pass')           
            else:
                print('Test failed')
                exit(1)
except ValueError:
    print("Test Failed")
    exit(1)