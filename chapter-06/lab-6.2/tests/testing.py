#!/usr/bin/env python3
import boto3

# Create a CloudWatch client
cloudwatch = boto3.client('cloudwatch')

# Define the parameters for the metric query
namespace = 'AWS/Events'
metric_name = 'MatchedEvents'
rule_name = 'iam-access-key-generated-rule'

# Query the metric data
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
                'Period': 300,  # 5 minutes
                'Stat': 'Sum',  # You can change this to other statistics like 'Average', 'Maximum', etc.
                'Unit': 'Count'
            }
        }
    ],
    StartTime='2024-01-17T00:00:00Z',
    EndTime='2024-01-17T23:59:59Z'
)

# Process the response
try:
    if 'MetricDataResults' in response:
        for result in response['MetricDataResults']:
            #print(type(result))
            print(f"Result output: ", result['Values'][0])
            if result['Values'][0] > 0:
                print('Test Pass')
            if result['Values'][0] == "":
                print('Test Failed, no results')
                exit(1)                
            else:
                print('Test failed')
                exit(1)
except ValueError:
    print("Test Failed")