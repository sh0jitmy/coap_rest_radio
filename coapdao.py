import logging
import asyncio
import json 

from aiocoap import *

class CoapDao(object):
	def __init__(self,address,port):
		self.URL = "coap://" + address + ":" + port + "/"
		self.radiodata = {}	
	def  get(self,path) :
		asyncio.run(self.int_get(path))
		return self.radio

	async def int_get(self,path):
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
			self.radio = decoded 
	async def int_update(self,path,req):
		self.proto = await Context.create_client_context()
		request = Message(code=PUT,payload=req,uri=self.URL+path) 
		response = await protocol.request(request).response
		print('Result: %s\n%r'%(response.code,response.payload))	
		return true
