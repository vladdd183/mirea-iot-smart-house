from devices import Lamp, TV, Teapot, CoffeeMachine, Humidifier, Conditioner, Music

from threading import Thread

lmp1 = Lamp('Lamp1', 'room1')
lmp2 = Lamp('Lamp2', 'room3')

tv1 = TV('TV1', 'room2')
tv2 = TV('TV2', 'room1')

tea1 = Teapot('Teapot1', 'room2')
tea2 = Teapot('Teapot2', 'room1')

coffee1 = CoffeeMachine('Coffee1', 'room3')
coffee2 = CoffeeMachine('Coffee2', 'room1')


humd1 = Humidifier('Humd1', 'room1')
humd2 = Humidifier('Humd2', 'room2')

cond1 = Conditioner('Cond1', 'room3')
cond2 = Conditioner('Cond2', 'room1')

Music1 = Music('Music1', 'room3')
Music2 = Music('Music2', 'room1')


Thread(target= lmp1.start).start()
Thread(target= lmp2.start).start()

Thread(target= tv1.start).start()
Thread(target= tv2.start).start()

Thread(target= tea1.start).start()
Thread(target= tea2.start).start()

Thread(target= coffee1.start).start()
Thread(target= coffee2.start).start()


Thread(target= humd1.start).start()
Thread(target= humd2.start).start()

Thread(target= cond1.start).start()
Thread(target= cond2.start).start()


Thread(target= Music1.start).start()
Thread(target= Music2.start).start()

