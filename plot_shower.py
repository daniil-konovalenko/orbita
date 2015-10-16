import json
from matplotlib import pyplot as plt

with open('telemetry.json') as json_file:
    data = json.load(json_file)
    time = data['time']
    angle = data['angle']
    temp = data['temp']
    P = data['P']
    qc = data['qc']
    charge = data['charge']
    plt.figure(1)
    plt.plot(angle, temp, 'g')
    plt.title('Temperature / angle')
    plt.figure(2)
    plt.plot(angle, P, 'r')
    plt.title('P / angle')
    plt.figure(3)
    plt.plot(time, charge)
    plt.title('Charge / time')
    plt.show()
