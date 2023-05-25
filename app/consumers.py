from channels.generic.websocket import AsyncJsonWebsocketConsumer
from app.models import Message
from django.contrib.auth.models import User
# from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

class ChatAsyncWebsocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.groupname = ""
        receiver = self.scope['url_route']['kwargs']['receiver']
        if str(self.scope['user']) > receiver:
            self.groupname = str(self.scope['user']) + receiver
        else:
            self.groupname = receiver + str(self.scope['user'])
        # print(self.groupname)
        # print(self.channel_name)
        await self.channel_layer.group_add(
            self.groupname, 
            self.channel_name
        )

        await self.accept()
        # print("ok")
    
    async def receive_json(self, content, **kwargs):
        # print("first", content)

        content['sender'] = str(self.scope['user'])

        if self.scope['user'].is_authenticated:
            message = await database_sync_to_async(Message)()
            message.msg = content['msg']
            message.sender = await database_sync_to_async(User.objects.get)(username=content['sender'])
            message.receiver = await database_sync_to_async(User.objects.get)(username=content['receiver'])
            await database_sync_to_async(message.save)()

            await self.channel_layer.group_send(
                self.groupname,
                {
                    'type': 'chat.msg',
                    'message': content
                }
            )
        else:
            await self.send_json({
                'message': "Login Required"
            })

    async def chat_msg(self, event):
        # event['message']['sender'] = str(self.scope['user'])
        # print("test",event)
        await self.send_json(event['message'])
    
    async def disconnect(self, code):
        print("Disconnect -", code)
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )