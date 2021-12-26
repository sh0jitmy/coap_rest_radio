from bottle import route, run 
from bottle import post, get, put, delete, request, response
from bottle import install 
import restcontroller
import json

@get('/status')
def read_radio():
	response.headers['Content-Type'] = 'application/json'
	response.headers['Cache-Control'] = 'no-cache'
	
	res = cont.read_radio()
	print("read_radio:",res)
	return json.dumps(res)


@get('/monitor')
def read_radio():
	response.headers['Content-Type'] = 'application/json'
	response.headers['Cache-Control'] = 'no-cache'
	
	res = cont.read_monitor()
	print("read_monitor:",res)
	return json.dumps(res)

@put('/control')
def update_radio():
        request_dict = json.loads(request.json)
        print("req",request_dict) 
        res = cont.update_radio(request_dict,False)
        if res == True : 
            return request.json
        else :
            response.status = 504 
            return {}

@get('/register')
def read_register():
	response.headers['Content-Type'] = 'application/json'
	response.headers['Cache-Control'] = 'no-cache'
	return json.dumps(cont.read_register())

'''
@put('/radio')
def update_radio():
        request_dict = json.loads(request.json)
        print("req",request_dict) 
        res = cont.update_radio(request_dict,False)
        if res == True : 
            return request.json
        else :
            response.status = 504 
            return {}
'''
@put('/register')
def update_register():
        request_dict = json.loads(request.json)
        print("req",request_dict) 
        res = cont.update_register(request_dict,False)
        if res == True : 
            return request.json
        else :
            response.status = 504 
            return {}

cont = restcontroller.RestController()
run (host='localhost', port=28081, debug=True, reloader=True)
