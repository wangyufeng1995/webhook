#!/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/10/16 15:13
# @Author  : Wang

import requests
import json
import datetime

def init_messages(key,**kwargs):
    token = key
    timestamp = kwargs["timestamp"]
    sign = kwargs['sign']
    url = "https://oapi.dingtalk.com/robot/send?access_token=%s&timestamp=%s&sign=%s" % (token,timestamp,sign)

    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    alert_info = kwargs['message']
    Alert_start_time = alert_info['Alert_Start_Time']
    Alert_status = alert_info['status']
    Alert_summary = alert_info['summary']
    Alert_description = alert_info['description']
    Alert_host = alert_info['host']

    slice1 = "**新增报警信息<font color=\'warning\'>" + nowtime + "</font>，请相关同事注意.** \n" \
    ">###### 开始时间 : <font color=#FF0000>" + Alert_start_time + "</font> \n" \

    slice2 = ">###### 告警状态 : <font color=#FF0000>" + Alert_status + "</font> \n" \
    ">###### 告警描述 : <font color=#FF0000>" + Alert_summary + "</font> \n" \
    ">###### 告警详情 : <font color=#FF0000>" + Alert_description + "</font> \n" \
    ">###### 告警主机 : <font color=#FF0000>" + Alert_host + "</font> "

    if 'Alert_Stop_Time' in alert_info.keys():
        Alert_Stop_Time = alert_info['Alert_Stop_Time']
        slice3 = ">###### 结束时间 : <font color=#FF0000>" + Alert_Stop_Time + "</font> \n"
        messages = slice1 + slice3 + slice2
    else:
        messages = slice1 + slice2

    return messages,url

def send_message(url,message):

    headers = {'content-type': "application/json"}
    body = {
        "msgtype": "markdown",
        "markdown": {
            "title": "报警信息",
            "text": message
        },
        "at": {
            "isAtAll": "true"
        }
    }
    #请求接口使用POST方式
    response = requests.post(url = url, headers = headers , json = body, timeout=5)
    # 返回信息
    #print (response.text)
    if response.status_code == 200:
        # 返回响应头
        #print (response.status_code)
        try:
            response_txt = response.text
            #转换返回的消息类型
            info = json.loads(response_txt)
            print (info)
            #return
        except OSError as e:
            return json.dumps({"status": 1, "info": "post-boot failed", "data": str(e)})
    else:
        return ("服务器未知错误")
