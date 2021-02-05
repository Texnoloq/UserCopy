#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os, sys
import csv
import traceback
import time
import random

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

def banner():
    print(f"""
        UserCopy
        Versiya : v1.0
        t.me/Texnoloq
        """)

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(re+"[!] Əvvəlcə bu əmri daxil edin :  python3 qurulum.py ! \n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input(gr+'[+] Kodu daxil edin : '+re))
 
os.system('clear')
banner()
input_file = sys.argv[1]
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)
 
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
 
i=0
for group in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - '+group.title)
    i+=1

print(gr+'[+] İstifadəçilərin hansı qrupa daşınacağını seçin :')
g_index = input(gr+"[+] Qrup nömrəsini daxil edin : "+re)
target_group=groups[int(g_index)]
 
target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
 
print(gr+"[1] User İD ilə daşı \n[2] İstifadəçi adı ilə daşı ")
mode = int(input(gr+"Input : "+re)) 
n = 0
 
for user in users:
    n += 1
    if n % 50 == 0:
	    time.sleep(1)
	    try:
	        print (" Daşınır {}".format(user['id']))
	        if mode == 1:
	            if user['username'] == "":
	                continue
	            user_to_add = client.get_input_entity(user['username'])
	        elif mode == 2:
	            user_to_add = InputPeerUser(user['id'], user['access_hash'])
	        else:
	            sys.exit(re+"[!] Yalnış mod seçildi. Xaiş olunur təkrar yoxlayın.")
	        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
	        print(gr+"[+] 1-5 saniyə gözlənilir..")
	        time.sleep(random.randrange(1, 5))
	    except PeerFloodError:
	        print(re+"[!] Telegram flood xətası . \n[!] Skript dayandırıldı. \n[!] Xaiş olunur biraz sonra yenidən yoxlayın. ")
	    except UserPrivacyRestrictedError:
	        print(re+"[!] Gizlilik ayarları səbəbi ilə istifadəçi daşına bilmədi. Keçilir...")
	    except:
	        traceback.print_exc()
	        print(re+"[!] Gözlənilməyən xəta")
	        continue
