#!/usr/bin/env python3
import requests, json, re, argparse


#cisa_feed = requests.get("https://www.cisa.gov/sites/default/files/2023-09/AA23-263A%20%23StopRansomware%20Snatch%20Ransomware.stix_.json")
#cisa_feed = requests.get("https://www.cisa.gov/sites/default/files/2023-12/aa23-347a-russian-foreign-intelligence-service-svr-exploiting-jetbrains-teamcity-cve-globally.json")

#print(type(cisa_feed.json()))
#json_payload = cisa_feed.json()

def ioc_extract(url_arg):
  cisa_feed = requests.get(url_arg)
  json_payload = cisa_feed.json()

  filename_list = []
  domain_list = []
  email_list = []
  ipv4_list = []
  md5_list = []
  sha256_list = []
  url_list = []

  for obj in json_payload["objects"]:
    if obj["type"] == "indicator":
      try:  
        pattern = obj["pattern"]
        if 'email-message:' in pattern:
          email_match = re.search("\.value = '(\S{1,100}@\S{1,100}\.\S{1,6})']", pattern)
          if email_match:
              email = email_match.group(1)
              email = str(email).strip("'").strip(']').strip("'")
              #print(email)
              email_list.append(email)
        if "file:name" in pattern:
          filename_match = re.search("file:name = '(\S{1,20})'", pattern)
          if filename_match:
            filename = filename_match.group(1)
            #print(filename)
            filename_list.append(filename)
        if "SHA-256" in pattern:
          sha256_match = re.search("'SHA-256' = '([A-Fa-f0-9]{64})'", pattern)
          if sha256_match:
            sha256 = sha256_match.group(1)
            #print(sha256)
            sha256_list.append(sha256)
        if "MD5" in pattern:
          md5_match = re.search("MD5 = '([A-Fa-f0-9]{32})'", pattern)
          if md5_match:
            md5 = md5_match.group(1)
            #print(md5)
            md5_list.append(md5)
        if "domain-name" in pattern:
          domain_match = re.search("value = '(\S{3,255})'", pattern)
          if domain_match:
            domain = domain_match.group(1)
            #print(domain)
            domain_list.append(domain)
        if "ipv4-addr" in pattern:
          ipv4_match = re.search("value = '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'", pattern)
          if ipv4_match:
            ipv4 = ipv4_match.group(1)
            #print(ipv4)
            ipv4_list.append(ipv4)
        if "url:value" in pattern:
          url_match = re.search("value = '(\S{6,500})'", pattern)
          if url_match:
            url = url_match.group(1)
            #print(url)
            url_list.append(url)
      except KeyError:
        pass
  '''
  # standard out #
  print('### FQDN PARSED ###')
  print(domain_list)
  print('### EMAILS PARSED ###')
  print(email_list)
  print('### FILENAMES PARSED ###')
  print(filename_list)
  print('### IPv4 PARSED ###')
  print(ipv4_list)
  print('### SHA256 PARSED ###')
  print(sha256_list)
  print('### MD5 PARSED ###')
  print(md5_list)
  print('### URL PARSED ###')
  print(url_list)
  '''
  return domain_list, email_list, filename_list, ipv4_list, sha256_list, url_list

### Dunder statement main driver ###
if __name__ == '__main__':
  parser = argparse.ArgumentParser(
                    prog='cisa-stix2json-ioc-extract',
                    description='Takes CISA STIX2 JSON formatted feeds and parses IOCs',
                    epilog='Usage: python3 cisa-stix2json-ioc-extract.py -url "https://cisa.gov/foo/something.json"'
                    )   
  parser.add_argument('-url', type=str, help='use stix2json formatted url')
  args = parser.parse_args()
  
  #positional tuple grab domains_list from return
  domains = ioc_extract(args.url)[0]
  
  #write buffer to file
  file_handle = open('cisa_domain_dnsbl.txt', 'a')
  for i in domains:
    file_handle.write(i)
  file_handle.close()

  exit()


  '''
  python .\pfsense-custom-cisa-feed.py -url "https://www.cisa.gov/sites/default/files/2023-12/aa23-347a-russian-foreign-intelligence-service-svr-exploiting-jetbrains-teamcity-cve-globally.json"
  '''