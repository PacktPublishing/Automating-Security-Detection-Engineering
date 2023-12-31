#!/usr/bin/env python3
from falconpy import APIHarnessV2
import argparse

#Ref: https://www.falconpy.io/Usage/Basic-Uber-Class-usage.html#import-and-authentication

#In a CI runner make these from the env variables at build time from a secrets manager!
#CLIENT_ID='<REDACTED>'
#CLIENT_SECRET='<REDACTED>'

def uploadioc(ioc_body, id, secret):
  #assign arguments to variables
  BODY = ioc_body
  CLIENT_ID = id
  CLIENT_SECRET = secret

  #client setup
  falcon = APIHarnessV2(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET
                        )                     
  response = falcon.command("indicator_create_v1",
                            retrodetects=False,
                            ignore_warnings=True,
                            body=BODY
                            )
  #print(response)
  return response

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
                    prog='custom-ioc-crowdstrike',
                    description='Takes JSON formatted payload for a custom IOC',
                    epilog='Usage: python3 custom-ioc-crowdstrike.py -id "<CLIENT_ID>" -secret "<CLIENT_SECRET>"'
                    )   
  parser.add_argument('-id', type=str, help='Crowdstrike Falcon API CLIENT_ID')
  parser.add_argument('-secret', type=str, help='Crowdstrike Falcon API CLIENT_SECRET')
  args = parser.parse_args()

  #construct the IOC body required example SHA256
  #in the real world you would pull this from a folder or file in the CI runner in a loop
  BODY = {
  "comment": "this is a test if falconpy sdk",
  "indicators": [
    {
      "action": "detect",
      "applied_globally": True,
      "description": "testing custom iocs in sdk",
      "expiration": "2024-10-22T10:40:39.372Z",
      #"host_groups": host_group_list,
      #"metadata": {
      #  "filename": "string"
      #},
      #"mobile_action": "string",
      "platforms": ['windows', 'linux'],
      "severity": "low",
      #"source": "string",
      "tags": ['falconpytest', 'test-cti'],
      "type": "sha256",
      "value": "8b8cdeb0540ebe562747fd7c618ed07eb1fbc5e98ed3b372672e045bae203925"
    }
  ]
}
  #define arguments to variables for main
  api_id = args.id
  api_secret = args.secret

  #call function with parameters
  response = uploadioc(BODY, api_id, api_secret)
  print(response)


  exit()