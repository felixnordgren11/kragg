
from gpiozero import Button

pin_a = Button(2)                      # Rotary encoder pin A connected to GPIO2
pin_b = Button(3)                      # Rotary encoder pin B connected to GPIO3

def pin_a_rising():                    # Pin A event handler
    if pin_b.is_pressed: print("-1")   # Pin A rising while A is active is an anti-clockwise turn

def pin_b_rising():                    # Pin B event handler
    if pin_a.is_pressed: print("1")    # Pin B rising while A is active is a clockwise turn

pin_a.when_pressed = pin_a_rising      # Register the event handler for pin A
pin_b.when_pressed = pin_b_rising      # Register the event handler for pin B

while True:
    message = eventq.get()
    print(message)