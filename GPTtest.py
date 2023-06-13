import tkinter as tk

class PowerSupplyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Power Supply GUI")

        # Create labels
        self.voltage_label = tk.Label(master, text="Voltage (V):")
        self.current_label = tk.Label(master, text="Current (A):")

        # Create entry fields
        self.voltage_entry = tk.Entry(master)
        self.current_entry = tk.Entry(master)

        # Create buttons
        self.set_button = tk.Button(master, text="Set", command=self.set_power)
        self.on_button = tk.Button(master, text="Turn On", command=self.turn_on)
        self.off_button = tk.Button(master, text="Turn Off", command=self.turn_off)

        # Grid layout
        self.voltage_label.grid(row=0, column=0, sticky=tk.E)
        self.current_label.grid(row=1, column=0, sticky=tk.E)
        self.voltage_entry.grid(row=0, column=1)
        self.current_entry.grid(row=1, column=1)
        self.set_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.on_button.grid(row=3, column=0, columnspan=2, pady=5)
        self.off_button.grid(row=4, column=0, columnspan=2, pady=5)

    def set_power(self):
        voltage = self.voltage_entry.get()
        current = self.current_entry.get()
        print("Setting power supply: Voltage =", voltage, "V, Current =", current, "A")

    def turn_on(self):
        print("Turning power supply on")

    def turn_off(self):
        print("Turning power supply off")

# Create the main window
root = tk.Tk()

# Create an instance of the PowerSupplyGUI class
gui = PowerSupplyGUI(root)

# Start the GUI event loop
root.mainloop()