import json
from math import pi, exp, sqrt, atan, sin, cos
import numpy as np
from matplotlib import pyplot as plt
from decimal import Decimal
from decimal import getcontext


params = json.load(open('mars.json'))

PLANET_MASS = Decimal(params['M'])
PLANET_RADIUS = Decimal(params['R'])
START_HEIGHT = Decimal(params['H'])
GRAV_CONSTANT = Decimal(params['G'])
START_MASS = Decimal(params['m0'])
THRUST = params['u'] * params['dm']
MASS_LOSS = Decimal(params['dm'])
START_VELOCITY_X = Decimal(params['vx'])
START_VELOCITY_Y = Decimal(params['vy'])
FUEL_MASS =Decimal(params["fuel_mass"])
SHIP_RADIUS = Decimal(params['r'])
DENSITY = Decimal(params['density'])


def density(height):
    return DENSITY * Decimal(exp(-height / Decimal(12500)))


class Ship():

    def __init__(self, mass, height, fuel_mass, eng_on, eng_off, shi_on, shi_off,
                 para_on, para_off):
        self.time = 0
        self.mass = mass
        self.fuel_mass = fuel_mass
        self.area = Decimal(pi) * SHIP_RADIUS ** 2
        self.eng_on = eng_on
        self.eng_off = eng_off
        self.shi_on = shi_on
        self.shi_off = shi_off
        self.para_on = para_on
        self.para_off = para_off
        self.thrust = THRUST
        self.is_eng_on = lambda: (self.eng_on <= self.time <= self.eng_off) and self.fuel_mass > 0
        self.is_shield_on = lambda: self.shi_on <= self.time <= self.shi_off
        self.is_parachute_on = lambda: self.para_on <= self.time <= self.para_off
        self.x = 0
        self.y = height
        self.vy = START_VELOCITY_Y
        self.vx = START_VELOCITY_X
        self.v = sqrt(self.vx**2 + self.vy**2)
        self.ax = 0
        self.ay = 0
        self.a = 0
        self.X = [self.x]
        self.Y = [self.y]
        self.VX = [self.vx]
        self.VY = [self.vy]
        self.AX = [0]
        self.AY = [0]
        self.A = [0]


    def next(self, dt):
        assert not (self.is_parachute_on() and self.is_shield_on())
        if self.is_eng_on():
            self.mass -= MASS_LOSS * dt
            self.fuel_mass -= MASS_LOSS * dt

        if abs(self.time - self.para_on) < 2 * dt:
            assert self.v < 600
            print('Parachute deployed')
            self.area += 200
        if abs(self.time - self.shi_on) < 2 * dt:
            assert self.v < 7000
            print('Shield deployed')
            self.area += 18
        if abs(self.time - self.shi_off) < dt:
            print('Shield dropped')
            self.mass -= 150
            self.area -= 18
        if abs(self.time - self.para_off) < dt:
            self.mass -= 10
            self.area -= 18
            print('Parachute dropped')


        self.v = sqrt(self.vx**2 + self.vy**2)
        v1 = self.v - (self.thrust * self.is_eng_on() + self.stokes()) / self.mass * dt

        vx1 = v1 / self.v * self.vx
        vy1 = v1 / self.v * self.vy - g(self.y) * dt

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.ax = (vx1 - self.vx) / dt
        self.ay = (vy1 - self.vy) / dt
        self.a = sqrt(self.ax**2 + self.ay**2)
        self.v = v1
        self.vx = vx1
        self.vy = vy1
        self.AX.append(self.ax)
        self.AY.append(self.ay)
        self.A.append(self.a)
        self.VX.append(self.vx)
        self.VY.append(self.vy)
        self.X.append(self.x)
        self.Y.append(self.y)

    def stokes(self):
        return Decimal(0.47) * density(self.y) * self.v ** 2 * self.area / 2


def g(height):
    return GRAV_CONSTANT * PLANET_MASS / (height + PLANET_RADIUS) ** 2

if __name__ == '__main__':
    ship = Ship(START_MASS, START_HEIGHT, FUEL_MASS, 8888888, 888880, 0, 8888, 888888, 88888888)
    dt = Decimal(1e-3)
    time = []
    while ship.Y[-1] >= 0:
        #print(ship.time)
        ship.time += dt
        ship.next(dt)
        T = round(ship.time, 4)
        time.append(T)

        if int(T) == T:
            pass
            print('T={:d<3} - X: {:.3f} Y: {:.3f} Vx: {:.3f} Vy: {:.3f} V: {:.3f} a: {:.3f} fuel: {:.2f} mass: {:.2f} As: {:.3f} S: {:.3f}'.format(T, ship.x, ship.y, ship.vx, ship.vy, ship.v, ship.a, ship.fuel_mass,
                                                                     ship.mass, ship.stokes() / ship.mass, ship.area))

    print('SURFACE! T+{} - Y: {:.3f} V: {:.3f} Vx: {:.3f} Vy: {:.3f} maxa: {:.3f} fuel: {:.2f} mass: {:.2f}'.format(T, ship.y, ship.v, ship.vx, ship.vy, max(ship.A), ship.fuel_mass,ship.mass))
