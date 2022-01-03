import logging
import json 
import time 
import threading 
from importlib import import_module
from pathlib import Path


#TODO Config JSON 
LSINDEX_DEF = 30
DEMILITER = "         "
POLL_INTERVAL = 0.5 

def parsejson_todict (jsonpath) :
	json_data = open(jsonpath,'r')
	json_dict = json.load(json_data)
	return json_dict	


class RegDao(object):
	def __init__(self,regpath,c_json,r_json,modpath):
		self.lsindex = LSINDEX_DEF 
		self.namedmlit = DEMILITER 
		self.pactive = False 
		self.poll_interval = POLL_INTERVAL 
		self.transformer = None 
	
		#reg proc path	
		self.regpath = regpath
		
		#regconf & control props
		self.register = parsejson_todict(r_json)  
		print(self.register)

		self.control_prop = parsejson_todict(c_json)  
		
		#find return dicts	
		self.status_prop = {}  
		self.monitor_prop = {}  
		
		#mutex
		self.paclock = threading.Lock()
		self.cplock = threading.Lock()
		self.splock = threading.Lock()
		self.mnlock = threading.Lock()

		#import modpath
		self.loadExModule(modpath)

		#create thread (auto run)
		self.createThread()

	def  loadExModule(self,modpath):
		if(modpath != "") :	
			path = Path(modpath)
			if path.is_file() :	
				mod = import_module(modpath)
				transformer = mod.TransFormer()
				if (hasattr(transformer, 'checkRegister') and callable(getattr(transformer, 'checkRegister'))
				and  hasattr(transformer, 'transRegister') and callable(getattr(transformer, 'transRegister'))):
					print("transformer:%s" % modpath)		
					self.transformer = transformer 
			else :
				self.transformer = None
		else :
			self.transformer = None

	def  update(self,writedata) :
		writedict,err = transprops_toregs(self,"control",writedata)	
		if err != "":
			return False,err
		errcode = True
		for key,value in writedict,items():
			err = writeregiseter(key,value)	
			if err != "" :
				errcode = False
		return	errcode 

	def  find(self,typename) :
		#print("find call:",typename)
		#Need Deep Copy ?
		if typename == "control" : 
			self.cplock.acquire()
			bret,dictdata =	True,self.control_prop
			self.cplock.release()
		#elif typename == RegType.STATUS :
		elif typename == "status" :
			print("status find")
			self.splock.acquire()
			bret,dictdata =	True,self.status_prop
			self.splock.release()
		elif typename == "monitor" : 
			print("monitor find")
			self.mnlock.acquire()
			bret,dictdata =	True,self.monitor_prop
			self.mnlock.release()
		else :
			return None
		return dictdata
		
	def  poll(self) :
		while (self.pollActiveGet() == True):
			self.readregister()
			time.sleep(self.poll_interval)
	
	def  createThread(self) :
		self.thread = threading.Thread(target=self.poll)
		self.pollActiveSet(True)	
		self.thread.start()

	def  deleteThread(self) :	 
		self.pollActiveSet(False)	
		self.thread.join()

	def pollActiveSet(self,flag) :
		self.paclock.acquire()
		self.pactive = flag 
		self.paclock.release()
	
	def pollActiveGet(self) :
		self.paclock.acquire()
		flag = self.pactive 
		self.paclock.release()
		return flag

	def  readregister(self) :
		with open(self.regpath) as f :
			for line in f:
				(regname,rawval,err) = self.getRegNameAndValue(line) 
				if err == "" :
					reginfo,err = self.getRegisterInfo(regname)
					if err == "":
						#If transform Register , call transform 
						if self.transformCheck(regname) :
							self.transData(regname,reginfo,rawval)	
						#If not Transform Register , parse from json config
						else :
							self.calcAndSet(regname,reginfo,rawval)	
					#else :
						#print(err + " regname:" +regname) 
		return
	def transformCheck(self,regname) :
		if self.transformer is None :
			return False
		if self.transformer.checktrans(regname) :
			return True
		else :
			return False


	def  writeregister(self,regname,value) :
		cmd = "echo " + regname + "=" + value
		syscmd = cmd + ">" + self.regpath
		ret,err = system_execute(syscmd)
		if (err !="") :
			print(err)
		return err
	
	def system_execute(self,cmdstr) :
		cp = subprocess.run(cmdstr)
		if cp.returncode != 0 : 
			return false,cp.stderr
		return true,"" #success nil return	

	def  transprops_toregs(self,typename,dictdata):	
		return 

	def getRegNameAndValue(self,rpline):
		validstr = rpline[:self.lsindex]	
		result = validstr.split(self.namedmlit)
		#print(result)
		if (len(result) < 2) :
			return "","","Format is Invalid"	
		return result[0],result[1],""	
	
	def getRegisterInfo(self,regname):
		if(regname in self.register):	
			return self.register[regname],""#return dict	
		return None,"Not Found Register"	

	def calcAndSet(self,regname,reginfo,rawval):
		err = "" 
		#regmask and bitfield calculate
		#print("rawval:0x%X regmask:0x%X shift:%d" % (int(rawval,0),int(reginfo["regmask"],0),reginfo["bitshift"]))
		if ("regmask" in reginfo) and ("bitshift" in reginfo)  :
			calcvalue = (int(rawval,0) & int(reginfo["regmask"],0)) >> reginfo["bitshift"]

		elif ("regmask" in reginfo) and (not ("bitshift" in reginfo) )  :
			calcvalue = (int(rawval,0) & int(reginfo["regmask"],0)) 
		else :
			calcvalue = int(rawval,0)
	
		if reginfo["type"] == "status" :
			#print("update status")
			self.status_prop[reginfo["propname"]] = calcvalue
		elif reginfo["type"] == "monitor" : 
			self.monitor_prop[reginfo["propname"]] = calcvalue
		else :
			err = "invalid type" 
		
		return err

	def transData(regname,reginfo,calcvalue) :
		self.transformer.transRegister(regname,reginfo,calcvalue) 
			 
