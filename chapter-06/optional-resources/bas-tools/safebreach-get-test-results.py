import http.client
conn = http.client.HTTPSConnection("url")

### Run an existing simulation plan you made in console ###
headers = {
    'accept': "application/json",
    'x-apitoken': "REPLACE_KEY_VALUE"
    }

conn.request("POST", "/api/orch/v2/accounts/%7Baccount_id%7D/queue", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

### add logic here to retry and wait for specific amounts of time until a response returns 2XX ###

### Get Test Results Summaries to Parse ###
conn.request("GET", "/api/data/v1/accounts/%7Baccount_id%7D/testsummaries/%7BtestId%7D", headers=headers)
res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


### add logic here parse the results and ensure the detections fired exit with error or exit clean when part of CI ###