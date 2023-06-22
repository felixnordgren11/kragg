import can


channel = 'can0'
bustype = 'socketcan'

bus = can.Bus(channel = channel, interface = bustype)
