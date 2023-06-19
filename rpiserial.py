import serial

s = serial.Serial(port = '/dev/ttyAMA4', baudrate = 500000)

msg = ''

while msg != 'q':
    msg = input('Send: ').encode()
    s.write(msg)
    print(f"Ans: {s.read()}")
