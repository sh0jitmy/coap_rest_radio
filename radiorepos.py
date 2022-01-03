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
		transconf = daoconf["transmodule"]
		self.dao = pyregdao.RegDao(regpath,contconf,regconf,transconf) 		
	def update(self,dictdata):
		error = self.dao.update(dictdata)
		if not error :
			return {"status":"OK","msg":"success"}
		else :
			return {"status":"NG","msg":error}
		 
	def find(self,typename):
		print("repos find call")
		dictdata = self.dao.find(typename)
		return dictdata
