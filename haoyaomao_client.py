import os
import random
import string
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
VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))
def generate_word(length):
    word = ""
    for i in range(length):
        if i % 2 == 0:
            word += random.choice(CONSONANTS)
        else:
            word += random.choice(VOWELS)
    return word


def createUser(robot, config, user_pubkey):
    body = {'full_name': generate_word(10), 'session_secret':user_pubkey}
    body_in_json = json.dumps(body)

    encoded = robot.genPOSTJwtToken_extConfig('/users', body_in_json, config)

    r = requests.post('https://api.mixin.one/users', json = body , headers = {"Authorization":"Bearer " + encoded, "Mixin-Device-Id":config.admin_uuid})
    print(r.status_code)

    r.raise_for_status()

    result_obj = r.json()
    print(result_obj)
    return result_obj
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

def depositAddress(robot, config, asset_id):
    encoded = robot.genGETJwtToken_extConfig('/assets/' + asset_id, "", config)
    r = requests.get('https://api.mixin.one/assets/' + asset_id, headers = {"Authorization":"Bearer " + encoded, "Mixin-Device-Id":config.mixin_client_id})
    print(r.status_code)
    if r.status_code != 200:
        error_body = result_obj['error']
        print(error_body)

    r.raise_for_status()

    result_obj = r.json()
    print(result_obj)
    return result_obj

def searchSnapShots(robot, config, offset, limit, order):
    finalURL = "/network/snapshots?offset=%s&order=ASC&limit=%d" % (offset, limit)
    encoded = robot.genGETJwtToken_extConfig("/network/snapshots", body_in_json , config)
    request_header = {"Authorization":"Bearer " + encoded, 'Content-Type': 'application/json', 'Content-length': '0'}
 
    r = requests.get('https://api.mixin.one/network/snapshots', json = body_in_json, headers = request_header)
    print(r.status_code)
    if r.status_code != 200:
        error_body = result_obj['error']
        print(error_body)

    r.raise_for_status()

    result_obj = r.json()
    snapshots = result_obj["data"]

    for singleSnapShot in snapshots:
        if "user_id" in singleSnapShot:
            print(singleSnapShot)
            print("It is me")
    return snapshots

def readMyAsset(robot, config):
    encoded = robot.genGETJwtToken_extConfig('/assets', "", config)
    r = requests.get('https://api.mixin.one/assets', headers = {"Authorization":"Bearer " + encoded, "Mixin-Device-Id":config.mixin_client_id})
    print(r.status_code)
    if r.status_code != 200:
        error_body = result_obj['error']
        print(error_body)

    r.raise_for_status()

    result_obj = r.json()
    assets_info = result_obj["data"]
    asset_list = []
    for singleAsset in assets_info:
        if singleAsset["balance"] != "0":
            asset_list.append((singleAsset["symbol"], singleAsset["asset_id"], singleAsset["balance"]))
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

def pubkeyContent(inputContent):
    contentWithoutHeader= inputContent[len("-----BEGIN PUBLIC KEY-----") + 1:]
    contentWithoutTail = contentWithoutHeader[:-1 * (len("-----END PUBLIC KEY-----") + 1)]
    contentWithoutReturn = contentWithoutTail[:64] + contentWithoutTail[65:129] + contentWithoutTail[130:194] + contentWithoutTail[195:]
    return contentWithoutReturn




if __name__ == '__main__':
    print(u"1: create 10 user from scratch")
    print(u"2: look balance and transfer to admin")
    print(u"3: search snapshots of account")

    answer = prompt(u'Give me some input: ')
    print(u'You said: %s' % answer)
    if answer == u"1":
        DevConfig  =                    mixin_config.user_mixin_config()
        DevConfig.mixin_client_id =     mixin_config.mixin_client_id 
        DevConfig.mixin_pay_sessionid = mixin_config.mixin_pay_sessionid
        DevConfig.mixin_pin_token =     mixin_config.mixin_pin_token
        DevConfig.private_key     =     mixin_config.private_key
        DevConfig.deviceID =            mixin_config.admin_uuid
        if os.path.isfile('rsa_account.csv') == False:
            with open('rsa_account.csv', 'a') as csvfile:
                fieldnames = ['eth_address', 'pub', 'private_key', 'user_id', 'session_id', 'pin_token', 'asset_pin']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        with open('rsa_account.csv', 'a') as csvfile:
            fieldnames = ['eth_address', 'pub', 'private_key', 'user_id', 'session_id', 'pin_token', 'asset_pin']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for i in range(10):
                key = RSA.generate(1024)
                pubkey = key.publickey()
                print(key.exportKey())
                print(pubkey.exportKey())
                private_key = key.exportKey()
                key2Mixin = pubkeyContent(pubkey.exportKey())
                print(key2Mixin)
                create_user_result = createUser(mixin_api_robot, mixin_config, key2Mixin)
                user_id = create_user_result['data']['user_id']
                session_id = create_user_result['data']['session_id']
                pin_token = create_user_result['data']['pin_token']
                myConfig  = mixin_config.user_mixin_config()
                myConfig.mixin_client_id = user_id 
                myConfig.mixin_pay_sessionid = session_id 
                myConfig.mixin_pin_token = pin_token
                myConfig.private_key = private_key
                myConfig.deviceID = myConfig.mixin_client_id
                myConfig.asset_pin = "123456"
                createPin(mixin_api_robot, myConfig)
                asset_depositAddress = depositAddress(mixin_api_robot, myConfig, mixin_asset_list.PRS_ASSET_ID)
                asset_public_key = asset_depositAddress['data']['public_key']
                writer.writerow({'eth_address':asset_public_key, 'pub': key2Mixin, 'private_key': private_key, 'user_id': user_id, 'session_id': session_id, 'pin_token':pin_token, 'asset_pin':myConfig.asset_pin})
    if answer == "2":
        with open('rsa_account.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                myConfig  = mixin_config.user_mixin_config()
                myConfig.mixin_client_id     = row["user_id"]
                myConfig.mixin_pay_sessionid = row["session_id"]
                myConfig.mixin_pin_token     = row["pin_token"]
                myConfig.private_key         = row["private_key"]
                myConfig.deviceID            = myConfig.mixin_client_id
                myConfig.asset_pin           = row["asset_pin"]
                assetListsOfThisAccount = readMyAsset(mixin_api_robot, myConfig)
                for eachAsset in assetListsOfThisAccount:
                    traceuuid = str(uuid.uuid1())
                    result_obj = transferToFromPub(mixin_api_robot, myConfig, mixin_config.admin_uuid, eachAsset[1],eachAsset[2],"hao yangmao", traceuuid)
                    print(result_obj)

    if answer == "3":
        with open('rsa_account.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                this_snap_shots = searchSnapShots(mixin_api_robot, mixin_config, '2018-11-19T09:53:27.461420444Z', 500, 'ASC')
		while len(this_snap_shots) == 500:
                    lasttime = this_snap_shots[-2]["created_at"]
                    print(lasttime)
