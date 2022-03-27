import paho.mqtt.client as mqtt
from config import config
from random import randint
from time import sleep

class device():
    def __init__(self, client_id = None):
        self.broker = config['broker']
        self.port = config['port']
        self.home_topic = config['home_topic']

        if not client_id:
            self.client_id = f'python-mqtt-{randint(0, 1000)}'
        else:
            self.client_id = client_id


        self.client = mqtt.Client(self.client_id)
        
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        
        self.client.connect(self.broker, self.port)
        
        self.client.subscribe(self.home_topic)
        self.client.loop_start()

        self.run()

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = str(msg.payload.decode())
        print(topic.center(70,'='), '\n', payload, '\n', '-'*70)

    def on_connect(self, client, obj, flags, rc):
        print(obj, flags, rc)
        
    def on_disconnect(self, client, obj, rc):
        print(obj, flags, rc)

    def run(self):
        while True:
            self.client.publish(self.home_topic, f'{randint(0,100)}')
            sleep(1)

a = device()

