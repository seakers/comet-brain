import hashlib
import schedule


from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncJsonWebsocketConsumer



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
        print('--> TRYING TO ACCEPT WEBSOCKET CONNECTION')
        await self.accept()

        # --> 2. Save ws channel name in user_info
        # user_information: UserInformation = await _get_or_create_user_information(session, user, self.daphne_version)


        # --> 3. Add hash-key and channel name to channel groups
        key = self.scope['path'].lstrip('api/')
        hash_key = hashlib.sha256(key.encode('utf-8')).hexdigest()
        await self.channel_layer.group_add(hash_key, self.channel_name)


    async def receive_json(self, content, **kwargs):
        """
            Called when we get a text frame. Channels will JSON-decode the payload
            for us and pass it as the first argument.
        """

        # --> 1. Get user_info
        # user_info: UserInformation = await _get_or_create_user_information(self.scope['session'], self.scope['user'])
        # if user_info is None:
        #     return


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



    async def disconnect(self, code):
        """
            Called when the WebSocket closes for any reason.
        """

        # --> 1. Get key and hash-key
        key = self.scope['path'].lstrip('api/')
        hash_key = hashlib.sha256(key.encode('utf-8')).hexdigest()

        # --> 2. Remove from channel name / hash-key from channel group
        await self.channel_layer.group_discard(hash_key, self.channel_name)
