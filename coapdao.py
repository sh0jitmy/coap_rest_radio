import logging
import asyncio
import json 
import uuid
import copy 

from aiocoap import *

class CoapDao(object):
	def __init__(self,address,port):
		self.URL = "coap://" + address + ":" + port + "/"
		self.radio = {}	
		self.res = {}	
	def  get(self,path) :
		upath = str(uuid.uuid4()) + path
		asyncio.run(self.int_get(path,upath))
		res = copy.copy(self.radio[upath])
		del self.radio[upath]
		return res
	
	def  update(self,path,req) :
		uuid_str = str(uuid.uuid4()) 
		asyncio.run(self.int_update(path,req,uuid_str))
		self.req = req
		res =  self.res[uuid_str]
		del self.res[uuid_str]
		return res

	async def int_get(self,path,upath):
		protocol = await Context.create_client_context()
		request = Message(code=GET,uri=self.URL+path)
		#request = Message(code=GET,uri='coap://localhost/time')
		try:
			response = await protocol.request(request).response
			print('Fetch resouce',response)
		except Exception as e:
			print('Failed to Fetch resouce',self.URL+path)
			print(e)
		else:
			print('Result: %s\n%r'%(response.code,response.payload))	
			decoded = json.loads(response.payload)	
			self.radio[upath] = decoded 
	async def int_update(self,path,req,uuid_str):
		protocol = await Context.create_client_context()
		request = Message(code=PUT,payload=json.dumps(req).encode('utf8'),uri=self.URL+path) 
		try:
			response = await protocol.request(request).response
		except Exception as e:
			print('Failed to Fetch resouce',self.URL+path)
			print(e)
		else:
			print('Result: %s\n%r'%(response.code,response.payload))	
			decoded = json.loads(response.payload)	
			self.res[uuid_str] = decoded 
