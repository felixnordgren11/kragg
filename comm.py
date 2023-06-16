
from gpiozero import Button

pin_a = Button(2)                      # Rotary encoder pin A connected to GPIO2
pin_b = Button(3)                      # Rotary encoder pin B connected to GPIO3
pin_c  = Button(4, pull_up=False)
pin_d  = Button(23, pull_up=False)
pin_e  = Button(24, pull_up=False)


def pin_a_rising():   
    print("hello")                 # Pin A event handler
    if pin_b.is_pressed: print("-1")   # Pin A rising while A is active is an anti-clockwise turn

def pin_b_rising():                    # Pin B event handler
    if pin_a.is_pressed: print("1")    # Pin B rising while A is active is a clockwise turn

def pin_c_rising():                    # Pin A event handler
    if pin_c.is_pressed: print("Spänning")  # Pin A rising while A is active is an anti-clockwise turn

def pin_d_rising():                    # Pin B event handler
    if pin_d.is_pressed: print("Vänster")    # Pin B rising while A is active is a clockwise turn

def pin_e_rising():                    # Pin A event handler
    if pin_e.is_pressed: print("Höger")   # Pin A rising while A is active is an anti-clockwise turn


pin_a.when_pressed = pin_a_rising      # Register the event handler for pin A
pin_b.when_pressed = pin_b_rising      # Register the event handler for pin B
pin_a.when_pressed = pin_c_rising      # Register the event handler for pin A
pin_b.when_pressed = pin_d_rising      # Register the event handler for pin B
pin_a.when_pressed = pin_e_rising      # Register the event handler for pin A
 


# Freezes program to wait for interrupts:
input("Vrid och Tryck!")