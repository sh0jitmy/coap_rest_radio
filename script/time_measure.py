#-*- using:utf-8 -*-
import time
import requests

headers = {
	'Accept': 'application/json',
}

def measure_func():
	response = requests.get("http://localhost:28081/status",headers=headers)	
	print(response.text)

if __name__ == '__main__':
	start = time.time()
	measure_func()	   	 
	elapsed_time = time.time() - start
	print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
