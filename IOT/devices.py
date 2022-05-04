from paho.mqtt.client import Client
from config import config
import json
import time
from threading import Thread



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
                'enable': False,
                'intensive': 0,
                'RGB': (255, 255, 255)
                }

    def message_handler(self, message):
        match message['cmd'].split():
            case 'on', :
                self.data['info']['enable'] = True
            case 'off', :
                self.data['info']['enable'] = False
            case 'intensive', x:
                self.data['info']['intensive'] = int(x)
            case 'rgb', r, g, b:
                self.data['info']['RGB'] = (int(r), int(g), int(b))
                
        self.mqtt.publish(self.topic, json.dumps(self.data['info']))

class TV(MQTTClient):
    def initialize(self):
        self.data['info'] = {
                'enable': False,
                'channel': 0,
                'volume': 0
                }

    def message_handler(self, message):
        match message['cmd'].split():
            case 'on', :
                self.data['info']['enable'] = True
            case 'off', :
                self.data['info']['enable'] = False
            case 'channel', x:
                self.data['info']['channel'] = int(x)
            case 'volume', x:
                self.data['info']['volume'] = int(x)

        self.mqtt.publish(self.topic, json.dumps(self.data['info']))



class Teapot(MQTTClient):
    def initialize(self):
        self.data['info'] = {
                'enable': False,
                'volume': 0,
                'temp': 20
                }

    def message_handler(self, message):
        match message['cmd'].split():
            case 'on', :
                self.data['info']['enable'] = True
                self.thr_run = Thread(target=self.run)
                self.thr_run.start()
            case 'off', :
                self.data['info']['enable'] = False
            case 'volume', x:
                self.data['info']['volume'] = int(x)

        self.mqtt.publish(self.topic, json.dumps(self.data['info']))

    def run(self):
        while self.data['info']['temp'] < 100:
            self.data['info']['temp'] += 1
            time.sleep(0.5)
            self.mqtt.publish(self.topic, json.dumps(self.data['info']))
            
            if not self.data['info']['enable']:
                break
            
        self.data['info']['enable'] = False
        
        while self.data['info']['temp'] > 100:
            self.data['info']['temp'] -= 1
            time.sleep(0.9)
            self.mqtt.publish(self.topic, json.dumps(self.data['info']))



class CoffeeMachine(MQTTClient):
    def initialize(self):
        self.data['info'] = {
                'enable': False,
                'CoffeeType': 'Russiano',
                'coffee': 20,
                'water': 30,
                'milk': 10
                }

    def message_handler(self, message):
        match message['cmd'].split():
            case 'on', :
                self.data['info']['enable'] = True
                self.thr_run = Thread(target=self.run)
                self.thr_run.start()
            case 'off', :
                self.data['info']['enable'] = False
            case 'CoffeeType', x:
                self.data['info']['CoffeeType'] = x
            case 'coffee', x:
                self.data['info']['coffee'] = int(x)
            case 'water', x:
                self.data['info']['water'] = int(x)
            case 'milk', x:
                self.data['info']['milk'] = int(x)

        self.mqtt.publish(self.topic, json.dumps(self.data['info']))

    def run(self):
        while (self.data['info']['coffee'] < 100) and (self.data['info']['water'] > 0) and (self.data['info']['milk'] > 0):
            self.data['info']['coffee'] += 1
            self.data['info']['water'] -= 1
            self.data['info']['milk'] -= 1
            time.sleep(0.5)
            self.mqtt.publish(self.topic, json.dumps(self.data['info']))

            if not self.data['info']['enable']:
                break



class Humidifier(MQTTClient):
    def initialize(self):
        self.data['info'] = {
                'enable': False,
                'water': 100,
                'humidity': 20
                }

    def message_handler(self, message):
        match message['cmd'].split():
            case 'on', :
                self.data['info']['enable'] = True
                self.thr_run = Thread(target=self.run)
                self.thr_run.start()
            case 'off', :
                self.data['info']['enable'] = False
            case 'water', x:
                self.data['info']['water'] = int(x)
            case 'humidity', x:
                self.data['info']['humidity'] = int(x)

        self.mqtt.publish(self.topic, json.dumps(self.data['info']))

    def run(self):
        while self.data['info']['humidity'] < 100 and self.data['info']['water'] > 0:
            self.data['info']['humidity'] += 1
            self.data['info']['water'] -= 1
            time.sleep(0.5)
            self.mqtt.publish(self.topic, json.dumps(self.data['info']))
            
            if not self.data['info']['enable']:
                break
            
        self.data['info']['enable'] = False
        
        while self.data['info']['humidity'] > 0:
            self.data['info']['humidity'] -= 1
            time.sleep(0.9)
            self.mqtt.publish(self.topic, json.dumps(self.data['info']))


class Conditioner(MQTTClient):
    def initialize(self):
        self.data['info'] = {
                'enable': False,
                'temp': 30,
                'time': 20,
                'mode': 'Frost'
                }

    def message_handler(self, message):
        match message['cmd'].split():
            case 'on', :
                self.data['info']['enable'] = True
                self.thr_run = Thread(target=self.run)
                self.thr_run.start()
            case 'off', :
                self.data['info']['enable'] = False
            case 'temp', x:
                self.data['info']['temp'] = int(x)
            case 'mode', x:
                self.data['info']['mode'] = x

        self.mqtt.publish(self.topic, json.dumps(self.data['info']))

    def run(self):
        while self.data['info']['time'] > 0:
            if self.data['info']['mode'] == 'Frost':
                self.data['info']['temp'] -= 1
            elif self.data['info']['mode'] == 'Warm':
                self.data['info']['temp'] += 1
            
            self.data['info']['time'] -= 1

            self.mqtt.publish(self.topic, json.dumps(self.data['info']))
            
            time.sleep(60)
            
            if not self.data['info']['enable']:
                break
            
        self.data['info']['enable'] = False
        
class Music(MQTTClient):
    def initialize(self):
        self.data['info'] = {
                'enable': False,
                'volume': 0
                }

    def message_handler(self, message):
        match message['cmd'].split():
            case 'on', :
                self.data['info']['enable'] = True
            case 'off', :
                self.data['info']['enable'] = False
            case 'volume', x:
                self.data['info']['volume'] = int(x)
                
        self.mqtt.publish(self.topic, json.dumps(self.data['info']))
