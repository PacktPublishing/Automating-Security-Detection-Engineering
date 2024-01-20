#!/usr/bin/env python3
from falconpy import APIHarnessV2
import argparse, json

#Ref: https://www.falconpy.io/Usage/Basic-Uber-Class-usage.html#import-and-authentication


def uploadioa(ioc_body):
  BODY = ioc_body               
  response = falcon.command("create_rule",
                            retrodetects=False,
                            ignore_warnings=True,
                            body=BODY
                            )
  #print(response)
  return response

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
                    prog='custom-ioa-cs',
                    description='Takes JSON formatted payload for a custom IOA',
                    epilog='Usage: python3 custom-ioa-cs.py -id "<CLIENT_ID>" -secret "<CLIENT_SECRET>"'
                    )   
  parser.add_argument('-id', type=str, help='Crowdstrike Falcon API CLIENT_ID')
  parser.add_argument('-secret', type=str, help='Crowdstrike Falcon API CLIENT_SECRET')
  args = parser.parse_args()

  #assign secrets from env variables or arguments from CLI
  CLIENT_ID = args.id
  CLIENT_SECRET = args.secret


  #client setup do outside of function so you arent using against call quotas each post
  falcon = APIHarnessV2(client_id=CLIENT_ID,
                          client_secret=CLIENT_SECRET
                          )      
  
  #construct body read from external file like a real CI
  file_handle = open('test-rule-import.json', 'r')
  BODY = json.loads(file_handle.read())
  #print(type(BODY))
  #print(BODY)

  #call function with parameters
  
  response = uploadioa(BODY)
  json_response = json.dumps(response)
  print(json_response)


  exit()