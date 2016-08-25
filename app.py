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

codes = {}

@app.route('/')
def index():
  return render_template('picture.html')


@app.route('/picture')
def picture():
  with open("picture.png","rb") as f:
    image_binary = f.read()
  response = make_response(image_binary)
  response.headers['Content-Disposition'] = 'attachment; filename=picture.png'
  response.headers['Content-Type'] = 'image/png'
  return response


@app.route('/send', methods=['POST'])
def send_message():

  imgdata = request.form.get('base64img')
  imgdata = re.match('data:image/(png|jpeg);base64,(.*)$', imgdata).group(2)
  imgdata = base64.b64decode(imgdata)

  ph = request.form.get('phone')

  with open('static/' + ph + '.png', 'wb') as fh:
    fh.write(imgdata)

  # send MMS
  print('url: ' + url_for('static', filename=str(ph) + '.png', _external=True))
  imgur = url_for('static', filename=str(ph) + '.png', _external=True)
  imgur = imgur.replace('http://0.0.0.0:8000', config.SERVER['NGROK'])
  print(imgur)

  payload = {'To': ph, 'From': '894546', 'MediaUrl': imgur}
  # verify that the url is supposed to be for end-user or for account owner
  sms = requests.post('https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json'.format(config.TWILIO_CREDS['ACCOUNT_SID']),
                      data=payload, auth=(config.TWILIO_CREDS['ACCOUNT_SID'], config.TWILIO_CREDS['AUTH_TOKEN']))

  return '{"success": true}'



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)
