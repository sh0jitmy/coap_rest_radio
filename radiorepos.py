import pyregdao
import json


class Repositry(object):
	def __init__(self,jsonpath):
		self.jsonpath = jsonpath
		f = open(jsonpath,'r')
		daoconf = json.load(f)
		regpath = daoconf["regpath"]
		contconf = daoconf["contconf"]
		regconf = daoconf["regconf"]
		transconf = daoconf["get_trans"]
		update_transconf = daoconf["update_trans"]
		self.dao = pyregdao.RegDao(regpath,contconf,regconf,transconf,update_transconf) 		
	def update(self,dictdata):
		dictdata,error = self.dao.update(dictdata)
		if not error :
			return {"status":"OK","res":dictdata}
		else :
			return {"status":"NG","res":dictdata}
		 
	def find(self,typename):
		print("repos find call")
		dictdata = self.dao.find(typename)
		return dictdata
