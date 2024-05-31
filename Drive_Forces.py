# Imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Drive paramaters
V0 = 15 # V
Vdrive = 1.5 # V
l_drive = 200 # micrometer
d_drive = 2 # micrometer
w = 3 # micrometer
N_drive = 100 # amount
m_drive = 10.6 # microgram
k_drive = 941.56 # N/m
b_drive = 2.8544e-03 # kg/s

# Sense paramaters
m_sense = 7.42 # microgram

# Constants
epsilon_0 = 8.8541878e-12

omega_0 = 9416 # rad/s

m_total = m_drive + m_sense


def Calculate_capacitor_force(e_y, V): # distance, magnitude 1 or -1
    F = e_y * N_drive * V**2 * epsilon_0 * w / d_drive
    return(F)

def model_omega(X, t, omega, b, F_t):
    x, v = X
    dxdt = v
    dvdt = (F_t - b_drive * v - k_drive * x) / m_total
    return [dxdt, dvdt]


t = np.linspace(0, 0.005, 10000)

V_t = V0 + Vdrive * np.sin(omega_0 * t)

F_capacitor_t = Calculate_capacitor_force(1, V_t)

X0 = [0, 0]
x_drive = odeint(model_omega, X0, t, omega_0, b_drive, F_capacitor_t)

#plt.plot(t, V_t)
plt.plot(t, x_drive)