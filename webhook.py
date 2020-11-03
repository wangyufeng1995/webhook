# -*- coding:utf-8 -*-
from flask import Flask, request
import requests
import json
import time, datetime
from dingding import *
app = Flask(__name__)


@app.route('/send', methods=['POST'])
def send():
  try:
    data = json.loads(request.data)   #转换从alertmanager获得的json数据为dict类型
    for info in data['alerts']:
      alert_info = {}
      '''
      UTC转换LTZ
      '''
      UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
      # datetime数据类型转换字符串
      start_utc = (info['startsAt'])
      start_utc = (start_utc[0:26] + "Z")
      start_utcTime = datetime.datetime.strptime(start_utc, UTC_FORMAT)
      start_LZT = start_utcTime + datetime.timedelta(hours=8)
      start_LZT = start_LZT.strftime("%Y-%m-%d %H:%M:%S")
      alert_info['Alert_Start_Time'] = start_LZT


      if info['status'] == 'resolved': 
        stop_utc = (info['endsAt'])
        stop_utc = (stop_utc[0:26] + "Z")
        stop_utcTime = datetime.datetime.strptime(stop_utc, UTC_FORMAT)
        stop_LZT = stop_utcTime + datetime.timedelta(hours=8)
        stop_LZT = stop_LZT.strftime("%Y-%m-%d %H:%M:%S")
        alert_info['Alert_Stop_Time']  = stop_LZT

      alert_info['status'] = info['status'] 

      alert_info['alertname'] = info['labels']['alertname']
      host = (info['labels']['instance']).split(":")
      alert_info['host'] = host[0]
      
      annotations = info['annotations']
      alert_info['description'] = annotations['description']
      alert_info['summary'] = annotations['summary']
	
      message=alert_info
      try:
        key = "fb18b75b3ddda7e388a5203d74cbe78a0528ebb490ba69c111f01b2ef741ce9e"
        response,url = init_messages(key,message=message)
        send_message(message=response,url=url)
      except Exception as e:
        print (e)
  except Exception as e:
    print(e)
  return 'ok'

if __name__ == '__main__':
  app.run(debug=False,host='0.0.0.0',port=5000)
