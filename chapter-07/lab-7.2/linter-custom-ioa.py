#!/usr/bin/env python3
import jsonschema, json

#raw openapi spec
#https://assets.falcon.us-2.crowdstrike.com/support/api/swagger-mav.json

#2023-dec-28 us-2 falcon
custom_ioa_schema = {
  "comment": "string",
  "description": "string",
  "disposition_id": 0,
  "field_values": [
    {
      "final_value": "string",
      "label": "string",
      "name": "string",
      "type": "string",
      "value": "string",
      "values": [
        {
          "label": "string",
          "value": "string"
        }
      ]
    }
  ],
  "name": "string",
  "pattern_severity": "string",
  "rulegroup_id": "string",
  "ruletype_id": "string"
}

try:
    #imported sample use case
    file_handle = open('test-rule-import.json', 'r')

    use_case_payload = json.load(file_handle)

    results = jsonschema.validate(instance=use_case_payload,
                                schema=custom_ioa_schema)
    #print(results)
    if 'None' in str(results):
        print('Custom use case payload VALIDATED')
    elif str(results) != 'None':
        print('ERROR: Custom IOA payload does not meet schema spec for Dec 2023.' +
              'See: https://assets.falcon.us-2.crowdstrike.com/support/api/swagger-us2.html#/custom-ioa/create-rule')
        exit(1)
except:
    exit(1)
