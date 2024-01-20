#!/usr/bin/env/python3
import os, re, requests
from pathlib import Path

#python requires more stuff for relative path
current_dir = Path.cwd()
relative_path = Path('tests/testspec.txt')
absolute_path = current_dir / relative_path

#use a test build spec from a github repo
file_handle = open(absolute_path, 'r')
test_spec = file_handle.read()

payload_match = re.search('payload: (.{3,128})', test_spec)
payload = payload_match.group(1)

file_path_match = re.search("file_path: (.{2,100}\\.yaral)", test_spec)
file_path = file_path_match.group(1)

file_handle.close()

#test criteria needed
#payload_match = 'fsodp9ifjaposdfjhgosurijfaewrwergwea'
#file_path = 'wannacry_killswitch_domain.yaral'

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
    if payload in content:
      print('Check 1/2: Found payload IOC/IOA in Content Ref:')
      #print(url)
      #print(content)
      try:
        if payload in yara_rule: #modified to use the payload and not payload_match new var
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
