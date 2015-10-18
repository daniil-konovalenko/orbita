from numpy import roots
from sympy.solvers import solve
from sympy import Symbol
from math import pi, cos, asin, sin, degrees

G = 6.6742e-11
Me = 5.9726e24
R = 6371032
k = 1.38064852e-23
horb = 650000
gamma = pi/2
GMP = 216


coeff = [1, - 2 * (R + horb) * cos(gamma/2), (R + horb) ** 2 - R**2]
x = Symbol('x')


NK1 = min(roots(coeff)[0])

alpha1 = asin(NK1 / R * sin(gamma/2))


print('{: .2f}'.format(NK1))
print('Alpha1 = {:.4f}'.format(degrees(alpha1) + GMP))