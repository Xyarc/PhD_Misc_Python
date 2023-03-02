import matplotlib.pyplot as plt
import numpy as np

c = 3e8

w = np.linspace(2*np.pi/1.2e-6, 0,  10000)
wave_vector = w/c

w_p = np.sqrt((5.4e28*(1.6e-19)**2)/(9.1e-31*8.85e-12))

print(w_p)

#Optical params of silver @ 532nm
e1 = np.linspace(-75.663,-0.324, 10000)
e2 = np.linspace(1.4571, 2.593,  10000)
n = np.linspace(2.38, 2.593, 10000)

w_sp = w_p/np.sqrt(1+n**2)

theta = np.deg2rad(47)

def dispersion(w, e1, n):
    return (w/c)*np.sqrt((e1*n**2)/(e1+n**2))


fig, ax = plt.subplots()
fig.set_figheight(4)
fig.set_figwidth(7)

#ax.plot(wave_vector, w/w_p, label = "Light Line", color='blue', marker='', linestyle='-')
ax.plot(wave_vector/w_p, dispersion(w, e1, e2)/w_p , label = "Dispersion relation of Silver", color='red', marker='', linestyle='-')
#ax.plot(wave_vector/w_p,  n*w*np.sin(theta)/w_p, label = "Altered Light Line", color='cyan', marker='', linestyle='-')


ax.set_title("Dispersion Relation")
ax.set_xlabel("Wave_vector")
ax.set_ylabel("Frequency")
    
fig.tight_layout()
plt.show()