import paho.mqtt.client as mqtt
from config import config
from random import randint
from time import sleep

class device():
    def __init__(self, home_topic, room, name, broker='broker.hivemq.com', port=1883, username='test', password='test'):
        self.home_topic = home_topic
        self.room = room
        self.name = name
        self.topic = f'{home_topic}/{room}/{name}'

        self.client_id = f'python-mqtt-{randint(0, 1000)}'


        self.client = mqtt.Client(self.client_id)
        self.client.username_pw_set(username, password)
        
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        
        self.client.connect(broker, port)
        
        self.client.subscribe(self.home_topic)
        self.client.subscribe(self.topic)
        self.client.loop_start()

        self.run()

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = str(msg.payload.decode())
        
        if 'annonce' == payload:
            data = {'name': self.name,
                    'room': self.room,
                    'topic': self.topic,
                    'return': 'annonce'}
            self.client.publish(self.home_topic, str(data)) 
        
        self.message_handler(payload)    


    def on_connect(self, client, obj, flags, rc):
        data = {'name': self.name,
                'room': self.room,
                'topic': self.topic,
                'return': 'connected'}
        self.client.publish(self.home_topic, str(data)) 
        
    def on_disconnect(self, client, obj, rc):
        data = {'name': self.name,
                'room': self.room,
                'topic': self.topic,
                'return': 'disconnected'}
        self.client.publish(self.home_topic, str(data)) 

    def run(self):
        while True:
            pass
    
    
a = device('home1', 'room4', 'dev1')

