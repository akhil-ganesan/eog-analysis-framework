import serial
import matplotlib.pyplot as plt
import numpy as np
import keyboard
from collections import deque

# Set up the serial port and parameters
serial_port = 'COM6'  # Replace with your Arduino's serial port (e.g., '/dev/ttyUSB0' on Linux or 'COM3' on Windows)
baud_rate = 230400
ser = serial.Serial(serial_port, baud_rate)
history = 500
update_rate = 10
a = 0.5
baseline = 500

# Setup the plot
# plt.ion()  # Turn on interactive mode
# fig, ax = plt.subplots()
x_data = deque(maxlen=history)  # Store the last 100 data points
y_data = deque(maxlen=history)
# line, = ax.plot([], [], 'r-')  # Red line
# ax.set_xlim(0, history)
# ax.set_ylim(0, 1000)  # Assuming the sensor reads between 0 and 1023

# for i in range(200):
#     x_data.append(i)
#     y_data.append(i)

# Function to update the plot
# def update_plot():
#     line.set_xdata(np.arange(len(x_data)))  # X-axis
#     line.set_ydata(np.array(y_data))  # Y-axis
#     plt.draw()


# Read and plot data in real-time
readings = 0
update = history // update_rate

# update_plot()

# Use 15 kOhm gain
# 495 for QL Chip
def detectBlinks():
    if y_data[-1] < 400 <= y_data[-2]:
        print("Blink")
        keyboard.press('space')
        return True
    else:
        keyboard.release('space')
        return False

# Use 15 kOhm gain
def detectUpDown():
    if y_data[-1] < 495 <= y_data[-2]:
        print("Up")
        keyboard.press('space')
    elif y_data[-1] > 535 >= y_data[-2]:
        print("Down")
        keyboard.press('space')
    else:
        keyboard.release('space')


def detectRightLeft():
    if y_data[-1] < 480 <= y_data[-2]:
        print("Left")
        keyboard.release('right')
        keyboard.press('left')
    if y_data[-1] > 550 >= y_data[-2]:
        print("Right")
        keyboard.release('left')
        keyboard.press('right')
    else:
        keyboard.release('left')
        keyboard.release('right')

while True:
    if ser.in_waiting > 0:
        try:
            data = ser.readline().decode('utf-8').strip().split(',')[0]  # Read and decode data from serial
            # print(int(data))
            # data = float(data)
            # x_data.append(data)
            # print(ser.in_waiting)
            # if data.isdigit():  # Ensure the data is numeric
            value = int(data)
            # if y_data:
            #     value = value * a + (1 - a) * y_data[-1]
            # print(value)
            x_data.append(len(x_data))
            y_data.append(value)
            readings += 1
            if readings > 2:
                # print("Check", y_data[-2], y_data[-1])
                # detectRightLeft()
                detectBlinks()
                # if not detectBlinks():
                #    baseline = np.average(y_data)

            # if readings > update:
            #     # update_plot()
            #     readings = 0
                # plt.pause(0.01)
            # if (y_data[-1] < 600):
            #     pass
            #     keyboard.press('space')
            #     keyboard.release('space')
        except ValueError:
            pass
        except UnicodeDecodeError:
            pass
    if keyboard.is_pressed('q'):
            # keyboard.release('space')
            break

# ser.close()
# plt.ioff()  # Turn off interactive mode
# plt.show()  # Keep the plot open after program finishes