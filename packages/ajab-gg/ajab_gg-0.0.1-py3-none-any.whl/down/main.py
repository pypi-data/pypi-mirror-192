import os
from encryption import encryption
from ujson import loads, dumps
from requests import post, get
from rubiran import *
os.system("clear")

auth: str = "ewnxlwzdpnqnpzftfdykwnprnatfdrrz"

bot = rubiran(auth)

enc: encryption = encryption(auth)

android: dict = lambda: {"app_name" : "Main","app_version" : "2.9.8","platform" : "Android","package" : "ir.resaneh1.iptv","lang_code" : "en"}	
url: str = "https://messengerg2c64.iranlms.ir/"

def getLinkInfo(link_post: str) -> dict:
	Json = {"api_version" : "5" , "auth" : auth , "data_enc" : enc.encrypt(dumps({"method" : "getLinkFromAppUrl" , "input" : {"app_url": link_post} , "client" : android()}))}
	while 1:
		try:
			return loads(enc.decrypt(post(url=url, json=Json).json().get("data_enc")))["data"]["link"]["open_chat_data"]
			break
		except: ...

def getMessagesInfo(chat: str, msg_id: str) -> dict:
	Json = {"api_version" : "5" , "auth" : auth , "data_enc" : enc.encrypt(dumps({"method" : "getMessagesByID" , "input" : {"object_guid": chat,"message_ids": [msg_id]} , "client" : android()}))}
	while 1:
		try:
			return loads(enc.decrypt(post(url=url, json=Json).json().get("data_enc")))["data"]["messages"]
		except: ...

def download(linkpost: str, save:bool=True, saveAs:str=None) -> bytes:
	result:bytes = b""
	message = getMessagesInfo(getLinkInfo(linkpost)["object_guid"], str(getLinkInfo(linkpost)["message_id"]))[0]
	
	size = message["file_inline"]["size"]
	dc_id = str(message["file_inline"]["dc_id"])
	fileID = str(message["file_inline"]["file_id"])
	filename = saveAs or message["file_inline"]["file_name"]
	accessHashRec = message["file_inline"]["access_hash_rec"]

	header = {'auth': auth, 'file-id':fileID, "start-index": "0", "last-index": str(size), 'access-hash-rec':accessHashRec}
	server = f'https://messenger{str(dc_id)}.iranlms.ir/GetFile.ashx'

	while True:
		try:
			if size <= 1000000:
				result += get(url=server,headers=header).content
			else:
				for i in range(0,size,1000000):
					header["start-index"], header["last-index"] = str(i), str(i+131072 if i+131072 <= size else size)
					result += get(url=server,headers=header).content
			break
		except: ...

	if save: open(filename.split('/')[-1], "wb").write(result)
	return size,filename

links = "https://rubika.ir/upload_film_27/ECJDDEHFGBCEFFA"
OK = 0
guid_admin = "u0DcvH901ee3b9ffb3ac3251f278738d"
send_id = bot.sendMessage(guid_admin,"started")["data"]["message_update"]["message_id"]

while 1:
	sizo = download(save=False, linkpost=links)
	size = sizo[0]
	fillename = sizo[1]
	OK +=1
	Size = int(size)
	if Size / 1048576 > 1:
		size_true = size / 1048576
		size_ko = size_true * OK
		sizes = f"{size_true} MB"
		size_kol = f"{size_ko} MB"
    elif size / 1024 > 1:
    	size_true = size / 1024
    	size_ko = size_true * OK
    	sizes = f"{size_true} KB"
    	size_kol = f"{size_ko} KB"
    else:
    	size_ko = Size * OK
        sizes = f"{size} B"
        size_kol = f"{size_ko} B"
    pm_Down = f"""「𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐏𝐀𝐍𝐍𝐄𝐋」


[‼️] - 𝐍𝐚𝐦𝐞 : {fillename}

[⚙️] - 𝐒𝐢𝐳𝐞  : {sizes}

[🌐] - 𝐋𝐢𝐧𝐤 : {links}


‹ 𝐍𝐮𝐦𝐛𝐞𝐫 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 › : [ {OK} ]

‹ 𝐀𝐥𝐥 𝐃𝐨𝐰𝐧 𝐒𝐢𝐳𝐞 : {size_kol}"""
	hep = bot.editMessage(guid_admin,pm_Down,send_id)
	print("New Message")