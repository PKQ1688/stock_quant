#!/usr/bin/env python
# -*- coding: UTF-8 -*-'''
# @Project : stock_quant 
# @Date    : 2022/2/10 19:38
# @Author  : Adolf
# @File    : dele_telegrame.py
from telethon import TelegramClient, events, sync

api_id = ""
api_hash = ""

placeholder_msg = "ph"
ignored_chat_ids = []

client = TelegramClient("session", api_id, api_hash)
client.start()

print(client.get_me().stringify())
print("\n")

print("All messages you sent in the following groups will be deleted: ({CHAT_ID}|{GROUP_NAME})")
for dialog in client.iter_dialogs():
    if dialog.is_channel and dialog.is_group:
        if not dialog.entity.id in ignored_chat_ids:
            print(str(dialog.entity.id)+"|"+dialog.entity.title)
print("\n")

if input("Continue? (y/N)")=="y":
    placeholder_file = client.upload_file('placeholder.png')
    print("Uploaded placeholder picture")
    for dialog in client.iter_dialogs():
        if dialog.is_channel and dialog.is_group:
            if not dialog.entity.id in ignored_chat_ids:
                for message in client.iter_messages(dialog.entity.id, from_user="me"):
                    if message.forward or message.via_bot or message.sticker or message.contact or message.poll or message.game or message.geo:
                        pass
                    elif message.text or message.voice:
                        if not message.text == placeholder_msg:
                            try:
                                message.edit(placeholder_msg)
                            except:
                                pass
                    elif message.document or message.photo or message.file or message.audio or message.video or message.gif:
                        if placeholder_file:
                            if not message.text == placeholder_msg:
                                try:
                                    message.edit(placeholder_msg, file=placeholder_file)
                                except:
                                    pass
                    else:
                        if not message.text == placeholder_msg:
                            try:
                                message.edit(placeholder_msg)
                            except:
                                pass
                    try:
                        message.delete()
                        print("Deleted \"{}\":\"{}\"".format(dialog.entity.title, message.text))
                    except:
                        print("Failed to Delete \"{}\":\"{}\"".format(dialog.entity.title, message.text))