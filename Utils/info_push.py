# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : stock_quant
# @Date    : 2022/1/18 23:29
# @Author  : Adolf
# @File    : info_push.py
# @Function:
import json
import logging

import requests


def post_msg_to_dingtalk(title="", msg="", token="", at=None, type="text"):
    if at is None:
        at = []
    url = "https://oapi.dingtalk.com/robot/send?access_token=" + token
    if type == "markdown":
        # 使用markdown时at不起作用，大佬们有空调一下
        data = {
            "msgtype": "markdown",
            "markdown": {"title": "[" + title + "]" + title, "text": "" + msg},
            "at": {},
        }
    if type == "text":
        data = {
            "msgtype": "text",
            "text": {"content": "[" + title + "]" + msg},
            "at": {},
        }
    data["at"]["atMobiles"] = at
    json_data = json.dumps(data)
    try:
        response = requests.post(
            url=url, data=json_data, headers={"Content-Type": "application/json"}
        ).json()
        assert response["errcode"] == 0
    except Exception as e:
        logging.getLogger().error("发送钉钉提醒失败，请检查；{}".format(e))
