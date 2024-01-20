#!/usr/bin/env python3
import re, os, argparse

#runtime args
parser = argparse.ArgumentParser()
parser.add_argument('-dir', type=str, help='Provide the relative directory path of the snort rules to validate.')
args = parser.parse_args()

if not args.dir:
   print('Please provide directory for the *.rule files')

#file and directory handles
directory = os.fsencode(args.dir)
for file in os.listdir(directory):
  file_handle = os.fsdecode(file)
  if file_handle.endswith(".rule"):
    full_path = (str(args.dir) + '/' +str(file_handle))
    file_bin = (open(full_path, 'r'))
    #snort_rule = file_bin.readline()

    #simple test if PAN-OS 10.x compliant content pattern length
    #https://docs.paloaltonetworks.com/pan-os/u-v/custom-app-id-and-threat-signatures/custom-application-and-threat-signatures/create-a-custom-threat-signature/create-a-custom-threat-signature-from-a-snort-signature
    #https://docs.paloaltonetworks.com/pan-os/u-v/custom-app-id-and-threat-signatures/custom-application-and-threat-signatures/custom-signature-pattern-requirements
    
    for snort_rule in file_bin:
        counter = 0
        content_sections = re.findall(r'content:"(.*?)";', snort_rule)
        for section in content_sections:
            num_chars = len(section) - section.count('|')
            print(f"Content Section: {section}")
            print(f"Total Characters: {num_chars}")
            print()
            try:
                if num_chars <= 127:
                    print('Payload pattern is likely PAN-OS compliant')
            except ValueError:
                print('Payload pattern length too long for PAN-OS')
                exit(1)

file_bin.close() #ensure close file handle for each file iteration
