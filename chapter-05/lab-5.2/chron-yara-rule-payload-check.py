#!/usr/bin/env python3
import os, re, requests

#test criteria needed
payload_match = 'fsodp9ifjaposdfjhgosurijfaewrwergwea'
file_path = 'wannacry_killswitch_domain.yaral'

#set user agent in case WAF rules
ua_header = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

#read file from directory
file_handle = open(file_path, "r")
yara_rule = file_handle.read()  #reads as giant serialized string

#re.search find the first instance serialized but returs re.match
url_match = re.search('reference\s\=\s"(\S{10,100})"', yara_rule)
url = url_match.group(1)
try:
  if url != "":
    print('ok')
    response = requests.get(url, headers=ua_header)
    #print(type(response.content))
    content = str(response.content)
    #print(content)
    if payload_match in content:
      print('Check 1/2: Found payload IOC/IOA in Content Ref:')
      #print(url)
      #print(content)
      try:
        if payload_match in yara_rule:
          print('Check 2/2: Found expected payload in yara rule')
      except ValueError:
        print('error: did not find expected payload in rule')
        file_handle.close()
        exit(1)
except ValueError:
  print('error: reference filled missing or non-url')
  file_handle.close()
  exit(1)

#exit close
file_handle.close()
