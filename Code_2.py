import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

# Sense paramaers
mass_sense = 7.42e-6  # Massa van de detectiemassa in kg
stiffness_sense = 2636.4  # Veerconstante van de detectiemassa in N/m
damping_sense = 2.797e-03  # Dempingsfactor van de detectiemassa in kg/s
angular_velocity = 10 / 60 * 2 * np.pi  # Rotatiesnelheid in rad/s
num_capacitors_sense = 40  # Aantal detectie-elektroden
dc_voltage = 15  # Gelijkspanning op de detectie-elektroden in volt
distance_sense = 2e-6  # Afstand tussen de detectie-elektroden in meter

# Drive parameters
mass_drive = 10.6e-6  # Massa
stiffness_drive = 941.56  # Veerconstante
damping_drive = 2.8544e-03  # Demping
distance_drive = 2e-6  # Afstand tussen condensatorplaten
thickness_drive = 3e-6  # Dikte platen
num_capacitors_drive = 100  # Aantal condensatoren
voltage_drive = 15  # Standaard voltage
voltage_difference_drive = 1.5  # Amplitude van de oscillerende kracht in N


# Time parameters
total_time = 0.07  # Totale tijd
time_step = 1e-5  # Tijdstap
time_points = np.arange(0, total_time, time_step)

# Drive calculations
resonant_frequency_drive = np.sqrt(stiffness_drive / mass_drive)
voltage_top = voltage_drive + voltage_difference_drive * np.sin(resonant_frequency_drive * time_points)
voltage_bottom = voltage_drive + voltage_difference_drive * np.sin(resonant_frequency_drive * time_points + np.pi)
force_top = (num_capacitors_drive * 8.85e-12 * thickness_drive * voltage_top ** 2) / distance_drive
force_bottom = (num_capacitors_drive * 8.85e-12 * thickness_drive * voltage_bottom ** 2) / distance_drive
net_force = force_top - force_bottom
net_voltage = voltage_top - voltage_bottom






# Drive simulation
velocity_drive = 0
position_drive = 0
velocity_drive_list = []
position_drive_list = []

for i in range(len(time_points)):
    acceleration_drive = (net_force[i] - damping_drive * velocity_drive - stiffness_drive * position_drive) / mass_drive
    velocity_drive += acceleration_drive * time_step
    position_drive += velocity_drive * time_step
    position_drive_list.append(position_drive)
    velocity_drive_list.append(velocity_drive)
    


velocity_drive_list = np.array(velocity_drive_list)





# Coriolis force
coriolis_force = 2 * mass_sense * angular_velocity * velocity_drive_list

# Sense simulation
velocity_sense = 0
position_sense = 0
velocity_sense_list = []
position_sense_list = []

for i in range(len(time_points)):
    acceleration_sense = (coriolis_force[i] - damping_sense * velocity_sense - stiffness_sense * position_sense) / mass_sense
    velocity_sense += acceleration_sense * time_step
    position_sense += velocity_sense * time_step
    position_sense_list.append(position_sense)
    velocity_sense_list.append(velocity_sense)


position_sense_list = np.array(position_sense_list)
position_drive_list = np.array(position_drive_list)




# Output voltage calculation
voltage_sense = num_capacitors_sense * position_sense_list * dc_voltage / distance_sense
voltage_drive = num_capacitors_drive * position_drive_list * dc_voltage / distance_drive

velocity_drive_analytic = signal.hilbert(velocity_drive_list)
force_drive_analytic = signal.hilbert(net_force)
voltage_drive_analytic = signal.hilbert(net_voltage)
position_sense_analytic = signal.hilbert(position_sense_list)
voltage_sense_analytic = signal.hilbert(voltage_sense)

n1 = voltage_drive_analytic / force_drive_analytic
n2 = force_drive_analytic  / velocity_drive_analytic
n3 = velocity_drive_analytic / position_sense_analytic
n4 = voltage_sense_analytic / force_drive_analytic

print(np.mean(n1),np.mean(n2),np.mean(n3),np.mean(n4))
print(16.5 / max(voltage_sense))
# Plotting
plt.plot(time_points, voltage_sense)

# plt.plot(time_points, net_voltage)

plt.xlabel('Tijd (s)')
plt.ylabel('Spanning (V)')
plt.title('Spanning op de probe')
plt.savefig('Spannig_Tijd.png', dpi=600)
plt.show()