import json
import regdao


REG_KEY = 0
REG_VALUE =1 


class RadioController(object):
	def __init__(self):
		self.regdao = regdao.RegDao("procpath.txt","sts.json","monitor.json") 
	def set_control(self,dictdata):
		#return self.regdao.write_register(dictdata)
		return  {"errorcode" : "success","reason":"success"} 
	
	def get_status(self):
		#dictdata = self.regdao.read_stsregister()
		#dictdata = self.regdao.read_stsregister()
		dictdata =   {"errorcode" : "success","reason":"success"} 
		return dictdata

	def get_monitor(self):
		#dictdata = self.regdao.read_monregister(monreg_dict)
		dictdata =   {"monitor1" : "sample1","monitor2":"sample2"} 
		return dictdata
	

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

