from math import sqrt, pi, acos, degrees, cos, sin, radians, log2
from matplotlib import pyplot as plt
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

G = 6.6742e-11
Me = 5.9726e24
R = 6371032
horb = 648000
m = 2.4
w0 = 1
vorb = sqrt(G * Me / (R + horb))
T = 2 * pi * (R + horb) / vorb

w = 360 * sqrt(G * Me/(R + horb)) / (2 * pi * (R + horb))

angle = 0
full_angle = 0
alpha = degrees(acos(R / (R + horb)))
alpha_start = 255 - alpha
alpha_stop = 255 + alpha

# Тепловые параметры
sigma = 5.67e-8
A_sb = 0.95
A_rad = 0.2
eps_sb = 0.4
eps_rad = 1
T0 = 290
Tmin = 263
Tmax = 313
c = 800
a = 0.1032
S = a ** 2 * 6
S_sb = S * 4 / 6
S_rad = S * 2 / 6 * 0.62

# Энергетические параметры

def Pe():
    return 0.298 * S_sb / 4 * qc() - Qin()

def qc():
    if 0 <= angle <= 180:
        return 1400
    else:
        return 0

def Qin():
    Q = 3.8
    if alpha_start <= angle <= alpha_stop:
        Q += 0
    return Q

def dT_dt():
    Q_outer = ((S_sb * A_sb / 4 + S_rad * A_rad / 4) * qc() -
    (S_sb * eps_sb + S_rad * eps_rad) * sigma * temp**4)
    Q_inner = Qin()
    return (Q_outer + Q_inner) / (c * m)

time = 0
dt = 1 / 500
temp = T0

max_charge = 41.8 * 3600
charge = max_charge

temp_list = [T0]
time_list = [0]
angle_list = [angle]
P_list = [dT_dt()]
qc_list = [qc()]
charge_list = [charge]
Pe_list = [Pe()]

while time <= 3600:

    angle += w * dt
    full_angle += w * dt
    angle = angle % 360
    temp += dT_dt() * dt
    charge += Pe() * dt
    charge = min(charge, max_charge)

    if int(time) / 5 == round(time / 5 , 3):
        temp_list.append(temp)
        time_list.append(time)
        qc_list.append(qc())
        P_list.append(dT_dt() * c * m)
        angle_list.append(full_angle)
        charge_list.append(charge)
        Pe_list.append(Pe())

    time += dt

    if int(time) == round(time, 3):
        logging.info('T={:.1f} Angle={:.3f} Temperature={:.2f} Q={:.3f} Pe={:.3f} Chrg={:.2f} qc={}'.format(time, angle, temp, dT_dt() * c * m, Pe(), charge, qc()))


logging.info('Max temp: {:.2f} Min temp: {:.2f}'.format(max(temp_list), min(temp_list)))

data = {
    'angle': angle_list,
    'temp': temp_list,
    'P': P_list,
    'time': time_list,
    'qc': qc_list
}
with open('telemetry.json', 'w', encoding='utf8') as fout:
    json.dump(data, fout)
    logging.info('DUMPED')

plt.figure(1)
plt.plot(time_list, temp_list, 'b')
plt.title('Temperature / time')
plt.figure(2)
plt.plot(angle_list, temp_list, 'g')
plt.title('Temperature / angle')
plt.figure(3)
plt.plot(angle_list, P_list, 'r')
plt.title('P / angle')
plt.figure(4)
plt.plot(time_list, charge_list)
plt.title('Charge / time')
plt.show()
