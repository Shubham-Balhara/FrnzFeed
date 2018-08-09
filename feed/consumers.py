from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Clients, Messages

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        obj=Clients.objects.filter(name=self.room_name).delete()
        obj = Clients.objects.create(name=self.room_name,ch_name=self.channel_name)
        obj.save()
        self.room_group_name = ''
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        Clients.objects.filter(name=self.room_name).delete()
        if self.room_group_name != '':
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
        self.close()

    def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver = text_data_json['receiver']
        async_to_sync(self.channel_layer.send)(
            self.channel_name,{
                'type':'test.message',
                'sender':self.room_name,
                'message':message,
            })
        obj = Clients.objects.filter(name=receiver).count()
        if obj>0:
            obj = Clients.objects.get(name=receiver)
            async_to_sync(self.channel_layer.send)(
                obj.ch_name,{
                    'type':'test.message',
                    'sender':self.room_name,
                    'message':message,
                })
        obj = Messages.objects.create(to=receiver,frm=self.room_name,message=message)
        obj.save()

    def test_message(self,event):
        message = event['message']
        sender = event['sender']
        self.send(text_data=json.dumps({
            'value':0,
            'sender':sender,
            'message':message
            }))