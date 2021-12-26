import datetime
import logging

import asyncio

import aiocoap
import aiocoap.resource as resource
import json
import radiocontroller

cont = radiocontroller.RadioController()

class ControlStatus(resource.Resource):
    """Example resource which supports the GET and PUT methods. It sends large
    responses, which trigger blockwise transfer."""

    def __init__(self):
        super().__init__()

    async def render_get(self, request):
        logging.info("aiocap server get") 
        data = cont.get_status()
        return aiocoap.Message(code=aiocoap.CONTENT,
			content_format=aiocoap.numbers.media_types_rev.get('application/json'),
			payload=json.dumps(data).encode('utf8'))

    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        req_data = json.loads(request.payload)	
        data = cont.set_control(req_data)
        return aiocoap.Message(code=aiocoap.CONTENT,
			content_format=aiocoap.numbers.media_types_rev.get('application/json'),
			payload=json.dumps(data).encode('utf8'))

class Monitor(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.handle = None

    async def render_get(self, request):
        data = cont.get_monitor()
        return aiocoap.Message(code=aiocoap.CONTENT,
			content_format=aiocoap.numbers.media_types_rev.get('application/json'),
			payload=json.dumps(data).encode('utf8'))


class Register(resource.ObservableResource):
    """Example resource that can be observed. The `notify` method keeps
    scheduling itself, and calles `update_state` to trigger sending
    notifications."""

    def __init__(self):
        super().__init__()

        self.handle = None

    async def render_get(self, request):
        payload = datetime.datetime.now().\
                strftime("%Y-%m-%d %H:%M").encode('ascii')
        return aiocoap.Message(payload=payload)

# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(['register'], Register())
    root.add_resource(['control'], ControlStatus())
    root.add_resource(['status'], ControlStatus())
    root.add_resource(['monitor'], Monitor())

    #await aiocoap.Context.create_server_context(root)
    logging.info("aiocap server start") 
    await aiocoap.Context.create_server_context(root,bind=("localhost",59311))

    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    
    asyncio.run(main())
