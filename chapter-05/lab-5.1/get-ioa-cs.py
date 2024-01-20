#!/usr/bin/env python3
import os, json
from falconpy import APIHarnessV2

CLIENT_ID = os.getenv('CS_CLIENT_ID')
CLIENT_SECRET = os.getenv('CS_CLIENT_SECRET')

# Do not hardcode API credentials!
falcon = APIHarnessV2(client_id=CLIENT_ID,
                      client_secret=CLIENT_SECRET
                      )

BODY = {
  "ids": ["1"]
}

response = falcon.command("get_rules_get", body=BODY)
#print(type(response))
json_response = json.dumps(response)
print(json_response)