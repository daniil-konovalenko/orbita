from math import sqrt, pi, acos, degrees, cos, sin, radians, log2, tan
from matplotlib import pyplot as plt
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
devices = json.load(open('devices.json'))

G = 6.6742e-11
Me = 5.9726e24
R = 6371032
k = 1.38064852e-23
horb = 650000
m = sum([devices[device]['m'] for device in devices.keys()])
w0 = 1
vorb = sqrt(G * Me / (R + horb))
a = 0.5
I = 1 / 12 * 2 * a ** 2 * m
T = 2 * pi * (R + horb) / vorb
w = 360 * sqrt(G * Me / (R + horb)) / (2 * pi * (R + horb))

GMP = 216
target = 81
angle = 0
full_angle = angle
alpha = degrees(acos(R / (R + horb)))

radio_start_angle = GMP - alpha
radio_stop_angle = GMP + alpha


# Тепловые параметры
sigma = 5.67e-8
A_sb = devices["Accumulator"]["A_sb"]
A_rad = devices["Heating"]["A_rad"]
eps_sb = devices["Accumulator"]["eps_sb"]
eps_rad = devices["Heating"]["eps_rad"]
T0 = 290
Tmin = max([devices[device]['T_min'] for device in devices.keys()])
Tmax = min([devices[device]['T_max'] for device in devices.keys()])
c = 800
Q = 0
for device in devices.keys():
    if devices[device]['a_init']:
        Q += devices[device]["Q"]

S = a ** 2 * 6
S_sb = S * 4 / 6 * 0.75
S_rad = S * 2 / 6

# Энергетические параметры

max_charge = devices['Accumulator']["Cap"] * 3600
charge = max_charge

# Параметры камеры

camera_start_angle = target - 1
camera_stop_angle = target + 1
shot = False


def camera_is_on():
    if camera_start_angle <= full_angle <= camera_stop_angle and not shot:
        return True
    else:
        return False


def heat_on():
    if qc() == 0:
        return True
    else:
        return False


def stabilization():
    w = -360 * sqrt(G * Me / (R + horb)) / (2 * pi * (R + horb))
    t = 2 * 270 / (w0 - w)
    M0 = (w - w0) * I / t
    print('w = {} t = {} M0 = {}'.format(w, t, M0))


# Переход с орбиты радиусом R1 на орбиту радиуса R2
def dV(R1, R2):
    V1 = sqrt(G * Me / R1) * (sqrt(2 * R2 / (R1 + R2)) - 1)
    V2 = sqrt(G * Me / R2) * (1 - sqrt(2 * R1 / (R1 + R2)))
    return V1 + V2


def Pe():
    return devices["Accumulator"]["n"] * S_sb / 4 * qc() - Qin()


def qc():
    if 0 <= angle <= 180:
        return 1400
    else:
        return 0


def Qin():
    Q = 0
    for device in devices.keys():
        if devices[device]['a_init']:
            Q += devices[device]['Q']
    if radio_start_angle <= angle <= radio_stop_angle:
        Q += devices['Radio']['P']
    if camera_is_on():
        Q += devices['Camera']['P']
    return Q


def dT_dt():
    Q_outer = ((S_sb * A_sb / 4) * qc() -
                (S_sb * eps_sb + S_rad * eps_rad) * sigma * temp**4)
    Q_inner = Qin()
    return (Q_outer + Q_inner) / (c * m)


def D():
    return (2 * horb * tan(devices["Camera"]['teta_max'] / 2) /
            (devices["Camera"]['d']))


def xy(alpha, r=R + horb):
    if alpha > 90:
        x = r * cos(radians(450 - alpha))
        y = r * sin(radians(450 - alpha))
    else:
        x = r * cos(radians(90 - alpha))
        y = r * sin(radians(90 - alpha))
    return (x, y)


def bandwidth(x_y):
    x = x_y[0]
    y = x_y[1]
    x_gmp = R * cos(radians(195))
    y_gmp = R * sin(radians(195))
    M = 4
    G_1 = 1
    G_2 = 16
    P1 = 5
    l = 299792458 / 435e6  # Длина волны
    L_gmp = sqrt((x_gmp - x) ** 2 + (y_gmp - y) ** 2)
    L_12 = (4 * pi * L_gmp / l) ** 2
    P_2 = G_1 * G_2 * P1 / L_12
    T_2 = 1000

    return 1 / 100 * P_2 * log2(M) / (1.2 * k * T_2)


time = 0
dt = 1 / 500
temp = T0

temp_list = [T0]
time_list = [0]
angle_list = [angle]
P_list = [dT_dt()]
qc_list = [qc()]
charge_list = [charge]
Pe_list = [Pe()]

while time <= 6 * 3600:

    angle += w * dt
    full_angle += w * dt
    angle = angle % 360
    temp += dT_dt() * dt
    charge += Pe() * dt
    charge = min(charge, max_charge)

    if int(time) / 5 == round(time / 5, 3):
        temp_list.append(temp)
        time_list.append(time)
        qc_list.append(qc())
        P_list.append(dT_dt() * c * m)
        angle_list.append(full_angle)
        charge_list.append(charge)
        Pe_list.append(Pe())

    time += dt

    if int(time) == round(time, 3):
        logging.info(
            'T={:.1f} Angle={:.3f} Temperature={:.2f} Q={:.3f} Pe={:.3f} Chrg={:.2f} qc={}'.format(
                time, angle, temp, dT_dt() * c * m, Pe(), charge, qc()))

logging.info(
    'Max temp: {:.2f} Min temp: {:.2f}'.format(max(temp_list), min(temp_list)))

data = {
    'angle': angle_list,
    'temp': temp_list,
    'P': P_list,
    'time': time_list,
    'qc': qc_list,
    'charge': charge_list,
    'Pe': Pe_list
}
with open('telemetry.json', 'w', encoding='utf8') as fout:
    json.dump(data, fout)
    logging.info('DUMPED')

plt.figure(1)
plt.plot(angle_list, temp_list, 'g')
plt.title('Temperature / angle')
plt.figure(2)
plt.plot(angle_list, P_list, 'r')
plt.title('P / angle')
plt.figure(3)
plt.plot(time_list, charge_list)
plt.title('Charge / time')
plt.show()
