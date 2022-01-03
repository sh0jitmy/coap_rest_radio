import json
import radiorepos 


REG_KEY = 0
REG_VALUE =1 


class RadioController(object):
	def __init__(self):
		self.repos = radiorepos.Repositry("radiorepos.json") 
	def set_control(self,dictdata):
		res_dict = self.repos.update(dictdata)	
		return  res_dict 
	
	def get_status(self):
		dictdata = self.repos.find("status")	
		return dictdata

	def get_monitor(self):
		dictdata = self.repos.find("monitor")	
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

