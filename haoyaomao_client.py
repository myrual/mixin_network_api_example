import json
import csv
import requests
import jwt
import datetime
import calendar
import hashlib
import base64
import Crypto
from Crypto.PublicKey import RSA
import time
import uuid
import mixin_config
from mixin_api import MIXIN_API
from mixin_api import transferTo
from mixin_api import transferToFromPub

import mixin_asset_list

from prompt_toolkit import prompt


pubkey = """AAAAB3NzaC1yc2EAAAADAQABAAACAQDSieUCEkxcAHSDePuxl7IR7KORH+1BTP/x0bVwxJyLPaw1tmD7jrYhbePUYpMdkKGVlUxLn6q8N7uFSALvV32f2P218dbVIZT50JGMPI/U21G+XMmqEHN0tzGc+CIVoXHe3FtjFqhV/qRmNuVR3c0iWeOn3As9sq5VmyFRhTB+tA7zQbZXpG2bwew47OL0nfpXyHgQf3FFRommWh9RnyNqtEx4Td0V7Kzyein6NgTTpfk52i3TczyMQJYcLr5IP4WfJ4Ekro8tacPrSsyxsqZVPUl7tzQYV+Tm/HB/rTpmaX6GJteV7r/j+2oh9H4JQib0ExVuJexG3jWlfYEozIUG1heFawEMGFS2n5Ri99SnT92IXqOcEYa24RYyFzHcXfm2J+cjYkgj4XYCoEQ4DYMNcLU2YgpISG+cc2oi8gKTUZHDDSWSEks+2bRa2nZ3g+nWLavWZnYME06WbJu0Q+RmoIEATCqd61PVNJw80kwzZ3IQcmOBknRpzTb1TXzNGafY5tMFCdjbJ9clzYAZyB+sqOa+zbo6MW4Ho7YVLTdyvhgee6jpk8AhEu7IgQG/TrHCjEYUIR0AFVtKMumMgAJ01mpoxrQivX0ZVJ4LCp41mXFInFO+8M++d3o4o9ZxATTxR7d3S+JzUR3hho0/ixICJY4GWSTCraV4r2VoYNoDTQ=="""
def createUser(robot, config, user_pubkey):
    body = {'full_name': 'bnet bot user example', 'session_secret':user_pubkey}
    body_in_json = json.dumps(body)

    encoded = robot.genPOSTJwtToken('/users', body_in_json, config.mixin_client_id)

    r = requests.post('https://api.mixin.one/users', json = body , headers = {"Authorization":"Bearer " + encoded, "Mixin-Device-Id":config.admin_uuid})
    print(r.status_code)

    r.raise_for_status()

    result_obj = r.json()
    print(result_obj)
def readAssetUser(robot, config):
    encoded = robot.genGETJwtToken_extConfig('/assets', "", config)

    r = requests.get('https://api.mixin.one/assets', headers = {"Authorization":"Bearer " + encoded, "Mixin-Device-Id":config.deviceID})
    print(r.status_code)

    r.raise_for_status()

    result_obj = r.json()
    print(result_obj)
def createPin(robot, config):
    encrypted_pin = robot.genEncrypedPin_extConfig(config)
    body = {'old_pin': "", 'pin':encrypted_pin}
    body_in_json = json.dumps(body)

    encoded = robot.genPOSTJwtToken_extConfig('/pin/update', body_in_json, config)
    r = requests.post('https://api.mixin.one/pin/update', json = body, headers = {"Authorization":"Bearer " + encoded})

    print(r.status_code)

    r.raise_for_status()

    result_obj = r.json()
    print(result_obj)
def verifyPin(robot, config):
    encrypted_pin = robot.genEncrypedPin_extConfig(config)
    body = {'pin':encrypted_pin}
    body_in_json = json.dumps(body)

    encoded = robot.genPOSTJwtToken_extConfig('/pin/verify', body_in_json, config)
    r = requests.post('https://api.mixin.one/pin/verify', json = body, headers = {"Authorization":"Bearer " + encoded})

    print(r.status_code)

    r.raise_for_status()

    result_obj = r.json()
    print(result_obj)

def readMyAsset(robot, config):
    encoded = robot.genGETJwtToken_extConfig('/assets', "", config)
    r = requests.get('https://api.mixin.one/assets', headers = {"Authorization":"Bearer " + encoded, "Mixin-Device-Id":config.mixin_client_id})
    print(r.status_code)
    if r.status_code != 200:
        error_body = result_obj['error']
        print(error_body)

    r.raise_for_status()

    result_obj = r.json()
    print(result_obj)
    assets_info = result_obj["data"]
    asset_list = []
    for singleAsset in assets_info:
        if singleAsset["balance"] != "0":
            asset_list.append((singleAsset["symbol"], singleAsset["balance"]))
    return asset_list

def searchSnapShot(robot, config, in_snapshort_id):
    print("searchSnapShot")
    encoded = robot.genGETJwtToken_extConfig('/network/snapshots/' + in_snapshort_id, "", config)
    r = requests.get('https://api.mixin.one/network/snapshots/' + in_snapshort_id, headers = {"Authorization":"Bearer " + encoded, "Mixin-Device-Id":config.mixin_client_id})
    r.raise_for_status()

    result_obj = r.json()
    userInfo = result_obj["data"]
    snap_user_uuid = userInfo["type"]
    snap_created_at = userInfo["created_at"]
    snap_source = userInfo["source"]
    snap_amount = userInfo["amount"]
    snap_id = userInfo["snapshot_id"]
    snap_asset = userInfo["asset"]
    snap_asset_id = snap_asset["asset_id"]
    snap_asset_name = snap_asset["name"]
    snap_asset_icon_url = snap_asset["icon_url"]
    snap_asset_symbol = snap_asset["symbol"]
    snap_asset_chain_id = snap_asset["chain_id"]
    snap_asset_type    = snap_asset["type"]

    return userInfo



def readTransferTraceID(robot, config, in_trace_id):
    print("readTransferTraceID")
    encoded = robot.genGETJwtToken_extConfig('/transfers/trace/' + in_trace_id, "", config)
    r = requests.get('https://api.mixin.one/transfers/trace/' + in_trace_id, headers = {"Authorization":"Bearer " + encoded, "Mixin-Device-Id":config.mixin_client_id})
    print(r.status_code)
    r.raise_for_status()

    result_obj = r.json()
    trace_obj = result_obj["data"]
    trace_asset_id = trace_obj["asset_id"]
    trace_counter_user_id = trace_obj["counter_user_id"]
    trace_memo = trace_obj["memo"]
    trace_trace_id= trace_obj["trace_id"]
    trace_amount = trace_obj["amount"]
    trace_snapshot_id = trace_obj["snapshot_id"]
    trace_type = trace_obj["type"]
    trace_created_at = trace_obj["created_at"]
    print(trace_obj)
    return trace_obj


def searchUser(robot, config, userid):

    encoded = robot.genGETJwtToken_extConfig('/users/' + userid, "", config)
    r = requests.get('https://api.mixin.one/users/' + userid, headers = {"Authorization":"Bearer " + encoded, "Mixin-Device-Id":config.mixin_client_id})
    print(r.status_code)
    if r.status_code != 200:
        error_body = result_obj['error']
        print(error_body)

    r.raise_for_status()

    result_obj = r.json()
    print(result_obj)
    userInfo = result_obj["data"]
    user_uuid = userInfo["user_id"]
    return user_uuid 

mixin_api_robot = MIXIN_API()
mixin_api_robot.appid = mixin_config.mixin_client_id
mixin_api_robot.secret = mixin_config.mixin_client_secret
mixin_api_robot.sessionid = mixin_config.mixin_pay_sessionid
mixin_api_robot.private_key = mixin_config.private_key
mixin_api_robot.asset_pin = mixin_config.mixin_pay_pin
mixin_api_robot.pin_token = mixin_config.mixin_pin_token
#http://travistidwell.com/jsencrypt/demo/
private_key = """-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQDnfy/s9NjXQK3knnsr9+vuB1XQQUeKoWCFcEBO7iD4KRbJ2mwC
Bx92iOEVpaVMxS2bykbczXGnnG6NnQBwPx4cx3Z+N/ibG+YkDakAg1F00D9JvPcb
oRFy/GRAvtm+dj3GBa74c1S1J4XbXq5H1nqlraZh/hrhCs3pV+H2ooCUpQIDAQAB
AoGAB2zG5ry7r7u9WBXVMYXUJWBK2lEdsE6Yv+7nwSBWIl9/AZ5l1HLSCYU+Yulb
MekpG1QTjcVxHcUgrp4Yg4EiwA3tNuSTnjomph696HaA04aX7JRWpJX7lPNIbBGL
2QUkOo5uoyrvqAgLJq4dvcpWBzOwI/yJACS4kqMukjY3jUECQQD8qLb+g8Ar/Ezp
70/dYkcdEDbT8p6XlEAI8R3X+L5itcgDl6RMinPXIzXcRIGTZzoTeFXZzvr3XC+6
7nf/P3y9AkEA6o7V3VJps6ShoG8CMlJPoL0uKK+cYeMk9jSdqzZtUnc435nvXMOP
ifgdcFZMtReeDrClBrQRORyNEXpEU6IaCQJADDmRmSEA1GABzLPilmCh9jsJnBm6
KLVon8Yi3odPlvEau2nD7lwonLk8aur5pgsxmS2SYdaM+BkCyjWtorEMtQJBAJwS
3wudwufeLA3sz7FcQ8/ZEdXQxGX+FqIc8Kz0UloFKrreWv+GwQQ1LKGLSw9U3782
mxiSyMMP1G5ExSJBQsECQGH23xD7awu+cQg6mY60kjk7aGBUz60gt9SDehWSjDpp
RHcyDyovJXWurun4N5lRZ2ftgSpGUX12aoB/vHzU3jI=
-----END RSA PRIVATE KEY-----"""

user_id = "bdc7167b-1f46-37a1-9200-8b4a3463df78"
session_id = 'f749263a-978f-470c-8184-aa2812f5cd1c'
pin_token = 'Px+wx/rI1bTr4fJ2FOs/V2A0gmPZLOgC+szb2GkSsY6s/qbvzdwTYiA9+QgWY/6kkY1iY7ED+TBz6GNyNGcZLQFtWOFM7R69KcAsjy6lkYi8qwQBKuYClbH0ucVddFwMYdgHbfYgsle3eicbTsRZVJXL/yFfzlx4PVVUXS6K2ps='

if __name__ == '__main__':
    print(u"1: create user from scratch")
    print(u"2: look balance")
    print(u"3: transfer money to admin")
    print(u"4: create my pin")
    print(u"5: verify my pin")
    print(u"6: read my asset")
    print(u"7: transfer CNB asset to ")
    print(u"71: search user uuid  ")
    print(u"8: show my CNB pay link asset to ")
    print(u"9: search snapshot ")
    answer = prompt(u'Give me some input: ')
    print(u'You said: %s' % answer)
    if answer == u"1":
        DevConfig  = mixin_config.user_mixin_config()
        DevConfig.mixin_client_id = mixin_config.mixin_client_id 
        DevConfig.mixin_pay_sessionid = mixin_config.mixin_pay_sessionid
        DevConfig.mixin_pin_token = mixin_config.mixin_pin_token
        DevConfig.private_key     = mixin_config.private_key
        DevConfig.deviceID = mixin_config.admin_uuid
        with open('rsa_account.csv', 'w') as csvfile:
            fieldnames = ['pub', 'private_key']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(2):
                key = RSA.generate(1024)
                pubkey = key.publickey()
                print(key.exportKey())
                print(pubkey.exportKey())
                writer.writerow({'pub': pubkey.exportKey(), 'private_key': key.exportKey()})
    if answer == "3":
        myConfig  = mixin_config.user_mixin_config()
        myConfig.mixin_client_id = user_id 
        myConfig.mixin_pay_sessionid = session_id 
        myConfig.mixin_pin_token = pin_token
        myConfig.private_key = private_key
        myConfig.deviceID = myConfig.mixin_client_id
        readAssetUser(mixin_api_robot, myConfig)
    if answer == "4":
        myConfig  = mixin_config.user_mixin_config()
        myConfig.mixin_client_id = user_id 
        myConfig.mixin_pay_sessionid = session_id 
        myConfig.mixin_pin_token = pin_token
        myConfig.private_key = private_key
        myConfig.deviceID = myConfig.mixin_client_id
        myConfig.asset_pin = "090830"
        createPin(mixin_api_robot, myConfig)
    if answer == "5":
        myConfig  = mixin_config.user_mixin_config()
        myConfig.mixin_client_id = user_id 
        myConfig.mixin_pay_sessionid = session_id 
        myConfig.mixin_pin_token = pin_token
        myConfig.private_key = private_key
        myConfig.deviceID = myConfig.mixin_client_id
        myConfig.asset_pin = "090830"
        verifyPin(mixin_api_robot, myConfig)
    if answer == "6":
        myConfig  = mixin_config.user_mixin_config()
        myConfig.mixin_client_id = user_id 
        myConfig.mixin_pay_sessionid = session_id 
        myConfig.mixin_pin_token = pin_token
        myConfig.private_key = private_key
        myConfig.deviceID = myConfig.mixin_client_id
        myConfig.asset_pin = "090830"
        readMyAsset(mixin_api_robot, myConfig)

    if answer == "7":
        myConfig  = mixin_config.user_mixin_config()
        myConfig.mixin_client_id = user_id 
        myConfig.mixin_pay_sessionid = session_id 
        myConfig.mixin_pin_token = pin_token
        myConfig.private_key = private_key
        myConfig.deviceID = myConfig.mixin_client_id
        myConfig.asset_pin = "090830"

        userid = prompt(u'Give me user id: ')

        user_uuid = searchUser(mixin_api_robot, myConfig, userid)
        traceuuid = str(uuid.uuid1())
        result_obj = transferToFromPub(mixin_api_robot, myConfig, user_uuid, mixin_asset_list.CNB_ASSET_ID,"123","robot pay example", traceuuid)
        if 'error' in result_obj:
            error_body = result_obj['error']
            error_code = error_body['code']
            if error_code == 20119:
                print("to :" + to_user_id + " with asset:" + to_asset_id + " amount:" + to_asset_amount)
                print(result_obj)

            if error_code == 20117:
                print("You don't have enoug money")
                print(result_obj)

        else:
            result_data = result_obj["data"]
            snap_id = result_data["snapshot_id"]
            print("success, snap id is :" + snap_id)
            searchSnapShot(mixin_api_robot,myConfig, snap_id)
            readTransferTraceID(mixin_api_robot, myConfig, traceuuid)
    if answer == "71":
        myConfig  = mixin_config.user_mixin_config()
        myConfig.mixin_client_id = user_id 
        myConfig.mixin_pay_sessionid = session_id 
        myConfig.mixin_pin_token = pin_token
        myConfig.private_key = private_key
        myConfig.deviceID = myConfig.mixin_client_id
        myConfig.asset_pin = "090830"

        userid = prompt(u'Give me user id: ')

        user_uuid = searchUser(mixin_api_robot, myConfig, userid)
        print("searched uuid is " + user_uuid)

    if answer == "8":
        myConfig  = mixin_config.user_mixin_config()
        myConfig.mixin_client_id = user_id 
        myConfig.mixin_pay_sessionid = session_id 
        myConfig.mixin_pin_token = pin_token
        myConfig.private_key = private_key
        myConfig.deviceID = myConfig.mixin_client_id
        myConfig.asset_pin = "090830"
        payLink = "https://mixin.one/pay?recipient=" + myConfig.mixin_client_id + "&asset=" + mixin_asset_list.CNB_ASSET_ID + "&amount=10086.0" + '&trace=' + str(uuid.uuid1()) + '&memo=hello'

        print(payLink)
    if answer == "9":
        myConfig  = mixin_config.user_mixin_config()
        myConfig.mixin_client_id = user_id 
        myConfig.mixin_pay_sessionid = session_id 
        myConfig.mixin_pin_token = pin_token
        myConfig.private_key = private_key
        myConfig.deviceID = myConfig.mixin_client_id
        myConfig.asset_pin = "090830"
        snapshot_id = prompt(u'Give me snapshot id: ')
        print(searchSnapShot(mixin_api_robot, myConfig, snapshot_id))
