from math import pi, e

def po (f):
    return 0.026 * e ** (-f/12500)

dt = 1/400
def sput (m, dvig = [88, 8888888], H = 6984.3, X = 0, vx = 457.3, vy = 279.3, tr = 0, mi = 8888888):
    global s
    t = 0
    sek = 1
    while True:
        v = (vx**2 + vy**2)**(1/2)
        g = G * M / (R + H)**2
        v1 = v 
        vx1 = vx
        vy1 = vy
        if mi < t:
            s = 200 + r**2 * pi
        
        aes = po(H) * koef * v1**2 * s/2 / m
        v1 = v1 - aes*dt
            
        if dvig[0] < t + dt < dvig[1]:
            v1 -= dv * dm / (m) * dt
            m -= dt * dm            
        
        if v > 0:
            vx1 = vx*v1/v
            vy1 = vy*v1/v
        
        
        vy1 += g*dt
        t += dt
        H = H - (vy + vy1) /2 * dt
        X += (vx + vx1) /2 * dt
        vy = vy1
        vx = vx1
        
        
        
        if t - 0.00000001 < sek and t + 0.0000001 > sek:
            sek += 1
            print (sek - 1 , m, g, H, vx, vy, aes)
        if H < 0:
            print( 'fall')
            print (sek - 1 , m, g, H, vx, vy, aes)
            break
  
  
M = 6.4185e23
G = 6.6742e-11
dm = 2
dv = 3600
R = 3389500
s = 2.0663 + 200
koef = 0.47

sput(1027.61)


def func(a, b):
    return (a**2 + b**2)**(1/2)