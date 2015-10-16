__author__ = 'Daniil Konovalenko'
from math import sqrt, pi, acos, degrees, cos, sin, radians, log2
from numpy import arange
G = 6.6742e-11
Me = 5.9726e24
R = 6371032
horb = 619000
m = 5.5
w0 = 1
vorb = sqrt(G * Me / (R + horb))
T = 2 * pi * (R + horb) / vorb
we = 360 / T
Mmax = 0.000023
a = 0.1503
I = 1 / 12 * 2 * a**2 * m
epsmax =  Mmax / I
# G1 =
# G2 =
# P1 =
k = 1.38064852e-23
w = -360 * sqrt(G * Me/(R + horb)) / (2 * pi * (R + horb))
t = 2*270 / (w0 - w)
M0 = (w - w0) * I / t
print('w = {} t = {} M0 = {}'.format(w, t, M0))

alpha = degrees(acos(R / (R + horb)))

# Время видимости
t_tr = 2 * alpha / we

# Расчет радиообмена

# Кооординаты НИП
def bandwidth(x_y):
    x = x_y[0]
    y = x_y[1]
    x_gmp = R * cos(radians(195))
    y_gmp = R * sin(radians(195))
    M = 4
    G_1 = 1
    G_2 = 16
    P1 = 5
    l = 299792458 / 435e6 # Длина волны
    L_gmp = sqrt((x_gmp - x) ** 2 + (y_gmp - y) ** 2)
    L_12 = (4 * pi * L_gmp / l) ** 2
    P_2 = G_1 * G_2 * P1 / L_12
    T_2 = 1000

    return 1 / 100 * P_2 * log2(M) / (1.2 * k * T_2)

def xy(alpha, r=R+horb):
    if alpha > 90:
        x = r * cos(radians(450 - alpha))
        y = r * sin(radians(450 - alpha))
    else:
        x = r * cos(radians(90 - alpha))
        y = r * sin(radians(90 - alpha))
    return (x, y)

alpha_start = 255 - alpha
alpha_stop = 255 + alpha

dt = 1e-3
dalpha = we * dt
angles = arange(alpha_start, alpha_stop+0.01, dalpha)
data_transmitted = 0

for angle in angles:
    data_transmitted += bandwidth(xy(angle)) * dt

print(data_transmitted)
