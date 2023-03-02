import numpy as np
import matplotlib.pyplot as plt

f = np.linspace(0.1, 1e6, 50000)
I_input = 1e-14 

f_sig = 953 # Hz

R_feedback = 200e6 # Hz



# C_Photodiode + C_Op-Amp / 1) FD11A + ADA4530-1 2) BPW + ADA4530-1
C_Shunt = 140e-12 + 8e-12

R_Shunt = 5e9 # Ohm

V_out = I_input * R_feedback

C_feedback_theory = np.sqrt(C_Shunt/(np.pi*2*R_feedback*2e6))

print("Feedback Capacitance >=", C_feedback_theory)
print("\n Output voltages:", V_out, "\n")
C_feedback = 1e-12
######  DC analysis  ######
# he inverting input bias current, I B− , sums directly with the
# photodiode current for a referred to input (RTI) error equal to
# I B− . This current flows through the feedback resistor, creating a
# referred to output (RTO) error,

V_os = 8e-6 # V
I_bias = 20e-15 # Amp

#Refered to output Error (V_rtoErr)
V_rtoErr = I_bias * R_feedback

#Error introduced due to Op-amp Voltage offset (V_rtoOs)

V_rtoOs = V_os * (1+(R_feedback/R_Shunt))

#print("\n Voltage Errors:", V_rtoErr, V_rtoOs, "\n")


#AC Analysis

Noise_gain_1 = (1+(R_feedback/R_Shunt))

#Noise_gain_2 = (1+(C_Shunt/C_feedback))

f_ugc = 2e6

f1 = 1/( ( (R_feedback*R_Shunt)/(R_feedback+R_Shunt) ) * (C_Shunt + C_feedback) )

f2 = 1/(R_feedback*C_feedback)

f3 = f_ugc/(1+C_Shunt/C_feedback)

fp = 1/(2*np.pi*(R_feedback*C_feedback))

Noise_gain = Noise_gain_1*(((2*np.pi*f)/f1 + 1)/((2*np.pi*f)/f2 + 1))

Signal_gain = R_feedback*(1/(2*np.pi*f_sig)/f2 + 1)


V_out = I_input * R_feedback
print("\nCurrent Input:", I_input, "\n")

print("\n Output voltages:", V_out, "\n")

print("\nPole Frequency:", fp, "\n")

print("\nNoise Gain Frequencies:", "\n", f1, "\n",f2 , "\n",f3, "\n")

print("Signal Gain:", Signal_gain, "\n")

print("\n Voltage Errors Total:", V_rtoErr + V_rtoOs, "\n")

# fig, ax = plt.subplots()
# fig.set_figheight(4)
# fig.set_figwidth(7)

# ax.loglog(f, Noise_gain)
# ax.vlines(f1, 0 , max(Noise_gain), color = "green")
# ax.vlines(f2, 0 , max(Noise_gain), color = "red")
# ax.vlines(f3, 0 , max(Noise_gain), color = "purple")

# ax.set_title("Bode Plot")
# ax.set_xlabel("Frequency")
# ax.set_ylabel("Gain")
    
# fig.tight_layout()
# plt.show()
