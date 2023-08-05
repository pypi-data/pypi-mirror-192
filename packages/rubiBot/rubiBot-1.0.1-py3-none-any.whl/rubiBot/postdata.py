import aiohttp
from .config import encryption
import json
from json import dumps, loads

async def http(sesion,auth,getjson):
	enc = encryption(auth)
	
	async with aiohttp.ClientSession() as session:
		async with session.post(sesion, data = dumps({"api_version":"5","auth": auth,"data_enc":enc.encrypt(dumps(getjson))}) , headers = {'Content-Type': 'application/json'}) as response:
			response =  await response.text()
			return response

async def httpfiles(session,data,head):
	async with aiohttp.ClientSession() as session:
		async with session.post(session, data = data  , headers = head) as response:
			response =  await response.text()
			return response