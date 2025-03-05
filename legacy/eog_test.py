import serial
import matplotlib.pyplot as plt
import numpy as np
import keyboard
from collections import deque

# Set up the serial port and parameters
serial_port = 'COM7'  # Replace with your Arduino's serial port (e.g., '/dev/ttyUSB0' on Linux or 'COM3' on Windows)
baud_rate = 230400
ser = serial.Serial(serial_port, baud_rate)
history = 200
update_rate = 1

# Setup the plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
x_data = deque(maxlen=history)  # Store the last 100 data points
y_data = deque(maxlen=history)
line, = ax.plot([], [], 'r-')  # Red line
ax.set_xlim(0, history)
ax.set_ylim(0, 1000000)  # Assuming the sensor reads between 0 and 1023

# for i in range(200):
#     x_data.append(i)
#     y_data.append(i)

# Function to update the plot
def update_plot():
    line.set_xdata(np.arange(len(x_data)))  # X-axis
    line.set_ydata(np.array(y_data))  # Y-axis
    plt.draw()


# Read and plot data in real-time
readings = 0
update = history // update_rate

# update_plot()

while True:
    if ser.in_waiting > 0:
        try:
            data = ser.readline().decode('utf-8').strip().replace(',','')  # Read and decode data from serial
            print(int(data))
            # data = float(data)
            # x_data.append(data)
            # print(ser.in_waiting)
            if data.isdigit():  # Ensure the data is numeric
                value = int(data)
                # print(value)
                x_data.append(len(x_data))
                y_data.append(value)
                readings += 1
            if readings > update:
                update_plot()
                readings = 0
                plt.pause(1)
            # if (y_data[-1] < 600):
            #     pass
                # keyboard.press('space')
                # keyboard.release('space')
        except UnicodeDecodeError:
            pass
    if keyboard.is_pressed('q'):
            # keyboard.release('space')
            break

ser.close()
plt.ioff()  # Turn off interactive mode
plt.show()  # Keep the plot open after program finishes