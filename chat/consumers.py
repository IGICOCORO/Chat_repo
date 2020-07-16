from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import *

User = get_user_model()

class MainConsumer(WebsocketConsumer):

    def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['id_user']
        self.room_name = "broadcast"
        self.room_group_name = f'chat_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        message = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': message["type"],
                'message': text_data
            }
        )

    def chat_message(self, event):
        message = json.loads(event['message'])
        if(str(self.scope["user"].id) == str(message['destination'])):
            self.send(text_data=json.dumps(message))

    def deletion(self, event):
        message_dict = json.loads(event['message'])
        message_id = message_dict["message"]
        message = Message.objects.get(id=message_id)
        message_dict["source"] = message.source.id
        message_dict["destination"] = message.destination.id
        message.delete()

        print(f"user = {str(self.scope['user'].id)}\nsource = {message_dict['source']}\ndestionation{message_dict['destination']}")
        if(str(self.scope["user"].id) in (str(message.source.id), str(message.destination.id))):
            self.send(text_data=json.dumps(message_dict))