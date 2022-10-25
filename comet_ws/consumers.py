import hashlib
import schedule
import time

from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from comet_problem.aws.ServiceManager import ServiceManager

from comet_auth.helpers import get_or_create_user_information_async, save_user_info_async
from comet_auth.models import UserInformation



class CometConsumer(AsyncJsonWebsocketConsumer):
    scheduler = schedule.Scheduler()
    sched_stopper = None
    kill_event = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    async def connect(self):
        """
            Called when the websocket is handshaking as part of initial connection.
        """

        # --> 1. Accept connection
        print('--> ACCEPTING WEBSOCKET CONNECTION')
        await self.accept()

        # --> 2. Get UserInformaiton
        session = self.scope['session']
        user = self.scope['user']
        user_information: UserInformation = await get_or_create_user_information_async(session, user)
        print('--> WEBSOCKET DETAILS:', user, session, session.session_key)

        # --> 3. Save channel
        user_information.channel_name = self.channel_name
        await save_user_info_async(user_information)

        # --> 3. Add hash-key and channel name to channel groups
        key = self.scope['path'].lstrip('api/')
        hash_key = hashlib.sha256(key.encode('utf-8')).hexdigest()
        print('--> MORE DETAILS:', hash_key, self.channel_name)
        await self.channel_layer.group_add(hash_key, self.channel_name)


    async def receive_json(self, content, **kwargs):
        """
            Called when we get a text frame. Channels will JSON-decode the payload
            for us and pass it as the first argument.
        """

        # --> 1. Get user_info
        session = self.scope['session']
        user = self.scope['user']
        user_info: UserInformation = await get_or_create_user_information_async(session, user)
        if user_info is None:
            return


        # --> 2. Get key and hash-key
        key = self.scope['path'].lstrip('api/')
        hash_key = hashlib.sha256(key.encode('utf-8')).hexdigest()


        # --> 3. Handle message based on: msg_type
        # - ping
        if content.get('msg_type') == 'ping':
            print("Ping received")
            await self.send_json({
                'type': 'ping'
            })
        elif content.get('msg_type') == 'ping_services':
            if user_info.user is not None:
                await self.ping_services(user_info, content)
        elif content.get('msg_type') == 'resource_msg':
            await self.resource_msg(user_info, content)



    async def disconnect(self, code):
        """
            Called when the WebSocket closes for any reason.
        """

        # --> 1. Get key and hash-key
        key = self.scope['path'].lstrip('api/')
        hash_key = hashlib.sha256(key.encode('utf-8')).hexdigest()

        # --> 2. Remove from channel name / hash-key from channel group
        await self.channel_layer.group_discard(hash_key, self.channel_name)




    async def resource_msg(self, user_info, content):
        command = content.get('command')
        request_id = content.get('request_id')
        instance_ids = content.get('instance_ids')
        service_manager = ServiceManager(user_info)
        await service_manager.gather()
        results = await service_manager.resource_msg(instance_ids, command, blocking=True)
        await self.send_json({
            'type': 'resource_msg_response',
            'request_id': request_id,
            'results': results
        })


    async def ping_services(self, user_info: UserInformation, content):
        print('\n--> PINGING SERVICES')
        start_time = time.time()
        service_manager = ServiceManager(user_info)
        result = await service_manager.gather()
        print('--> GATHER TOOK', time.time() - start_time, 'seconds')
        if result is True:
            survey = await service_manager.ping_services()
            payload = {
                'type': 'ping',
                'status': survey
            }
            if 'ping_id' in content:
                payload['ping_id'] = content['ping_id']
            await self.send_json(payload)
            print('--> PING FULFILLED', time.time() - start_time, 'seconds')







