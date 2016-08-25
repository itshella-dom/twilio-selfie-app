#!/usr/bin/env python3

import json
import requests
import base64
import re
import config

from twilio.rest import TwilioRestClient
from flask import Flask, render_template, request, Response, session, abort, jsonify, url_for, make_response

client = TwilioRestClient(config.TWILIO_CREDS['ACCOUNT_SID'], config.TWILIO_CREDS['AUTH_TOKEN'])

app = Flask(__name__)
app.config['DEBUG'] = True



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)
