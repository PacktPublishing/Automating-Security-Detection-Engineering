#!/usr/bin/env python3
from flask import Flask, Response
app = Flask(__name__)

@app.route("/")
def servefile():
  handle = open('cisa_domain_dnsbl.txt', 'r')
  file = handle.read()
  return Response(file, mimetype="text/plain")

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=443, ssl_context='adhoc')
