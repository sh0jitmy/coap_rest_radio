import json
import coapdao


REG_KEY = 0
REG_VALUE =1 


class RestController(object):
	def __init__(self):
		self.coap = coapdao.CoapDao("localhost","59311") 
	
	def read_register(self):
		return self.coap.get("register")
	
	def read_radio(self):
		data = self.coap.get("status")
		print("coap.get",data)
		return data
	
	def read_monitor(self):
		data = self.coap.get("monitor")
		print("coap.get",data)
		return data

	def update_register(self,req,async_en):
		return self.coap.update("register",req)	
	
	def update_radio(self,req,async_en):
		return self.coap.update("control",req)	

	

'''	
	def get_status(self):
		status = {}
	        with open(read_path)	as f:
			sarray = f.readlines()
			print(s)
		for reg_and_value in sarray :
			register = reg_anv_value.split(':')
			status[register[REG_KEY]] = gen_extdata(resiter)
		#status = [
	 	#    {"freq":0},
		#    {"power":0}
		#]
		return status
	def set_request(self,req,async_req):	
		result = False
		for name , value in req.items() :
			result = set_devdata(name,value)
			if result == False :
				return result
		return 	result

	
	def gen_extdata(register):
		return int(register(REG_VALUE)) 
	
	def gen_devdata(regname,value):
		writedata = regname + ":" + str(value)	
		return writedata 
	
	def set_devdata(regname,regvalue):
		writedata = gen_devdata(regname,regvalue)
		with open(write_path) as f :
			f.writeline(writedata)
		return True 
'''

