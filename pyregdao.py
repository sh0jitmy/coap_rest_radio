import logging
import json 
import time 
import threading 
from importlib import import_module
from pathlib import Path
import copy


#TODO Config JSON 
LSINDEX_DEF = 30
DEMILITER = "         "
POLL_INTERVAL = 0.5 

def parsejson_todict (jsonpath) :
	json_data = open(jsonpath,'r')
	json_dict = json.load(json_data)
	return json_dict	


class RegDao(object):
	def __init__(self,regpath,c_json,r_json,get_modpath,update_modpath):
		self.lsindex = LSINDEX_DEF 
		self.namedmlit = DEMILITER 
		self.pactive = False 
		self.poll_interval = POLL_INTERVAL 
		self.get_transformer = None 
		self.rawregister_store = {} 
	
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
		self.rrlock = threading.Lock()

		#import get_modpath
		self.loadGetExModule(get_modpath)
		self.loadUpdateExModule(update_modpath)

		#create thread (auto run)
		self.createThread()

	def  loadGetExModule(self,get_modpath):
		if(get_modpath != "") :	
			path = Path(get_modpath)
			if path.is_file() :	
				mod = import_module(get_modpath)
				get_transformer = mod.TransFormer()
				if (hasattr(get_transformer, 'checkRegister') and callable(getattr(get_transformer, 'checkRegister'))
				and  hasattr(get_transformer, 'transRegister') and callable(getattr(get_transformer, 'transRegister'))):
					print("get_transformer:%s" % get_modpath)		
					self.get_transformer = get_transformer 
			else :
				self.get_transformer = None
		else :
			self.get_transformer = None
	
	def  loadUpdateExModule(self,update_modpath):
		if(update_modpath != "") :	
			path = Path(update_modpath)
			if path.is_file() :	
				mod = import_module(update_modpath)
				transformer = mod.TransFormer()
				if (hasattr(get_transformer, 'checkProperty') and callable(getattr(get_transformer, 'checkProperty'))
				and  hasattr(get_transformer, 'transProperty') and callable(getattr(get_transformer, 'transProperty'))):
					print("get_transformer:%s" % get_modpath)		
					self.update_transformer = get_transformer 
			else :
				self.update_transformer = None
		else :
			self.update_transformer = None

	def  update(self,writedata) :
		resdata = copy.copy(writedata)
		for key,value in writedata.items():
			errcode = False	
			regname,regvalue,err = self.transprops_toreg(key,value)	
			if err != "":
				errcode = True
			else :		
				err = self.writeregister(regname,regvalue)	
				if err != "" :
					errcode = True 
			if errcode is True : 
				del resdata[key]
		return	resdata 

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
		print("find dictdata",dictdata)
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
						if self.transformRegisterCheck(regname) :
							self.transRegData(regname,reginfo,rawval)	
						#If not Transform Register , parse from json config
						else :
							self.calcAndSet(regname,reginfo,rawval)	
					#else :
						#print(err + " regname:" +regname) 
				self.update_registerstore(regname,rawval)
		return
	
	def update_registerstore(self,regname,regval) :
		self.rrlock.acquire()
		self.rawregister_store[regname] = regval
		self.rrlock.release()
	
	def get_registerstore(self,regname) :
		self.rrlock.acquire()
		if regname in self.rawregister_store :  
			regvalue = self.rawregister_store[regname]  
		else :
			regvalue = 0
		self.rrlock.release()
		return regvalue

	def transformRegisterCheck(self,regname) :
		if self.get_transformer is None :
			return False
		if self.get_transformer.checktrans(regname) :
			return True
		else :
			return False
	
	def transformPropCheck(self,propname) :
		if self.update_transformer is None :
			return False
		if self.update_transformer.checktrans(propname) :
			return True
		else :
			return False


	def  writeregister(self,regname,value) :
		print("write register call %s:%x(%d)" % (regname,value,value))
		cmd = "echo " + regname + "=" + str(value)
		syscmd = cmd + " > " + self.regpath
		ret,err = self.system_execute(syscmd)
		if (err !="") :
			print(err)
		return err
	
	def system_execute(self,cmdstr) :
		print(cmdstr)	
		return True,""

		cp = subprocess.run(cmdstr)
		if cp.returncode != 0 : 
			return False,cp.stderr
		return True,"" #success nil return	


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
	
	def getControlInfo(self,propname):
		if(propname in self.control_prop):	
			return self.control_prop[propname],""#return dict	
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


	def  transprops_toreg(self,propname,propvalue):	
		exist = self.transformPropCheck(propname)
		if exist is True :
			regname,writeval,err = self.transPropData(propname,propvalue)	
		else : 
			continfo,err = self.getControlInfo(propname)
			if err != "" :
				return "",0,err
		
			if "regname" in continfo :
				regname = continfo["regname"] 
			else :
				return "",0,"Notfound Error"
					
			if ("regmask" in continfo) and ("bitshift" in continfo)  :
				maskval = int(continfo["regmask"],0)
				calcvalue = (int(propvalue,0) & maskval) >> continfo["bitshift"]

			elif ("regmask" in continfo) and (not ("bitshift" in continfo) )  :
				maskval = int(continfo["regmask"],0)
				calcvalue = (int(propvalue,0) & maskval) 
			else :
				maskval = int("0xFFFFFFFF",0)
				calcvalue = int(propvalue,0)
	
			storevalue = int(self.get_registerstore(regname),0)
			print("calcvalue:%x(%d),maskval:%x" % (calcvalue,calcvalue,maskval))
			print("calcvalue:%x(%d) maskval:%x" % (storevalue,storevalue,self.reverseBit(maskval)))
			writeval = calcvalue | ( storevalue & self.reverseBit(maskval))	

		return regname,writeval,err	

	
	def transRegData(propname,propvalue) :
		return	


	def transRegData(regname,reginfo,calcvalue) :
		return	
	
	def reverseBit(self,n):
		return ~n & 0xFFFFFFFF 
