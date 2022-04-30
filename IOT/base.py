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

        self.data = {'name': name,
                     'room': room,
                     'topic': self.topic}

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
            self.data['return'] = 'annonce'
            self.client.publish(self.home_topic, str(self.data)) 
        
        self.message_handler(payload)    


    def on_connect(self, client, obj, flags, rc):
        self.data['return'] = 'connect'
        self.client.publish(self.home_topic, str(self.data)) 
        
    def on_disconnect(self, client, obj, rc):
        self.data['ruturn'] = 'disconnect'
        self.client.publish(self.home_topic, str(self.data)) 

    def run(self):
        while True:
            pass
    def message_handler(self, payload):
        pass

class home():
    pass

class room()

a = device('home1', 'room4', 'dev1')

