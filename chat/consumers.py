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
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data
            }
        )

    def chat_message(self, event):
        message = json.loads(event['message'])
        print(message)
        if(str(self.scope["user"].id) == str(message['destination'])):
            # contact = Contact.objects.get(user=message['destination'])
            # message["source_name"] = contact.user.first_name+" "+contact.user.last_name
            self.send(text_data=json.dumps(message))