from math import sqrt

from orbita import density, g

file = open('wshieldplanet.txt')


lines = file.readlines()

data = lines[9:-2]

T = []
X = []
H = []
Vx = []
Vy = []

for i in range(len(data)-1):
    splitted = data[i].split(' ')
    time = splitted[0].split('=')[1]
    minutes = int(time.split(':')[1])
    seconds = int(time.split(':')[2])
    T.append(minutes * 60 + seconds)

    X.append(float(splitted[1].split('=')[1]))
    H.append(float(splitted[2].split('=')[1]))
    Vx.append(float(splitted[3].split('=')[1]))
    Vy.append(float(splitted[4].split('=')[1]))

V = [sqrt(Vx[i]**2 + Vy[i]**2) for i in range(len(T))]

for i in range(len(V)):
    if V[i] < 500:
        print(V[i])
        print(''.join(data[i:]))
        break

time = T.index(248)
print('Mass=1027.61 Area=203.1415 H={} X={} Vx={} Vy={} V={}'.format(H[time], X[time], Vx[time], Vy[time], V[time]))

def stokes(v, height, area):
    return 0.47 * v**2 * density(height) * area / 2

Asx = stokes(Vx[time], H[time], 203.1415) / (1305.55 - 150)
Asy = stokes(Vy[time], H[time], 203.1415) / (1305.55 - 150)

A = sqrt((Asy - g(H[time]))**2 + Asx**2 )
print(A)

