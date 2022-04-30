from paho.mqtt.client import Client
from config import config
import json
import time
from threading import Thread


def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()



class MQTTClient:
    def __init__(self, name, room):
        
        self.config = config
        
        self.home_topic = config['home_topic']
        
        self.topic = f'{self.home_topic}/{room}/{name}'
        
        self.mqtt = Client()


        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_message = self.on_message        
        self.mqtt.on_disconnect = self.on_disconnect
        
        self.connect()
        
        self.mqtt.subscribe(self.home_topic)
        self.mqtt.subscribe(self.topic)
        
        self.data = {'name': name,
                'room': room,
                'topic': self.topic,
                'return': None}
        
        self.initialize()

    def connect(self):
        """Connect to the MQTT broker defined in the configuration."""
        # Set up MQTT authentication.
        if self.config.get('username') and self.config.get('password'):
            self.mqtt.username_pw_set(self.config['username'],
                                      self.config['password'])

        self.mqtt.connect(self.config['broker'], self.config['port'])

    def initialize(self):
        """Initialize the MQTT client."""
        pass
    
    def start(self):
        """Start the event loop to the MQTT broker so the audio server starts
        listening to MQTT topics and the callback methods are called.
        """
        self.mqtt.loop_forever()
        
    def stop(self):
        """Disconnect from the MQTT broker and terminate the audio connection.
        """
        self.mqtt.disconnect()

    def on_connect(self, client, userdata, flags, result_code):
        self.data['return'] = 'connected'
        self.mqtt.publish(self.home_topic, json.dumps(self.data))

    def on_disconnect(self, client, userdata, flags, result_code):
        self.data['return'] = 'disconnect'
        self.mqtt.publish(self.home_topic, json.dumps(self.data))
     
    def on_message(self, client, userdata, msg):
        
        decoded_message = msg.payload.decode()

        try:
            msg_data = json.loads(decoded_message)
        except:
            msg_data = str(decoded_message)

        if msg.topic == self.topic and 'cmd' in msg_data:
            self.message_handler(msg_data)
        elif 'annonce' == msg_data:
            self.data['return'] = 'annonce'
            self.mqtt.publish(self.home_topic, json.dumps(self.data))
    
    def message_handler(self, message):
        print(message)
        print('='*20)


class Lamp(MQTTClient):
    def initialize(self):
        self.data['info'] = {
                'enable': True,
                'intensive': 0,
                'RGB': (255, 255, 255)
                }

    def message_handler(self, message):
        match message['cmd'].split():
            case 'on':
                self.data['info']['enable'] = True
            case 'off':
                self.data['info']['enable'] = False
            case 'intensive', x:
                self.data['info']['intensive'] = int(x)
            case 'rgb', r, g, b:
                self.data['info']['RGB'] = (int(r), int(g), int(b))
        self.mqtt.publish(self.home_topic, json.dumps(self.data))

class TV(MQTTClient):
    def initialize(self):
        self.data['info'] = {
                'enable': True,
                'channel': 0,
                'volume': 0
                }

    def message_handler(self, message):
        match message['cmd'].split():
            case 'on':
                self.data['info']['enable'] = True
            case 'off':
                self.data['info']['enable'] = False
            case 'channel', x:
                self.data['info']['channel'] = int(x)
            case 'volume', x:
                self.data['info']['volume'] = int(x)

        self.mqtt.publish(self.home_topic, json.dumps(self.data))



class Teapot(MQTTClient):
    def initialize(self):
        self.data['info'] = {
                'enable': True,
                'channel': 0,
                'volume': 0,
                'temp': 20
                }

    def message_handler(self, message):
        match message['cmd'].split():
            case 'on', :
                self.data['info']['enable'] = True
                Thread(target=self.run).start()
            case 'off', :
                self.data['info']['enable'] = False
            case 'channel', x:
                self.data['info']['channel'] = int(x)
            case 'volume', x:
                self.data['info']['volume'] = int(x)

        self.mqtt.publish(self.home_topic, '='*10)

    def run(self):
        while self.data['info']['temp'] < 100:
            self.data['info']['temp'] += 1
            time.sleep(0.5)
            self.mqtt.publish(self.home_topic, json.dumps(self.data))

a1 = Teapot('t11', 'room3')
a1.start()
