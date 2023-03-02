import numpy as np
import matplotlib.pyplot as plt

f_sig = 421 # Hz

f_ugc = 2e6 # Unity Gain Crossover (Hz)

Input_current = 1e-12 #Amps - Min Signal current

# Constants

Temp = 293.15 # Room Temp

k = 1.380649e-23 # Boltzmann

I_n = 0.07e-15 # Current Noise Density of the Op-amp

V_n = 80e-9 # Voltage Noise Density @ 10 Hz of Op-amp


# TIA Capacitance & Resistance
R_f = 200e6 # Feedback Resistor of TIA
R_s = 5e9 # Shunt Resistor of the Photodiode

C_f = 1e-12 # Farads - Feedback Capacitor of the TIA
C_s = 140e-12 + 8e-12 # F - Photodiode Capacitance and Op-amp Capacitance

## Theoretical Stable Feedback Cap
C_f_theory = np.sqrt(C_s/(np.pi*2*R_f*2e6))

print("\nTheoretical Stable Feedback Capacitor: ", C_f_theory*1e-12, " pF\n")
print("\nSignal Frequency: ", f_sig, " Hz\n")
print("\nModulation Frequency: ", f_sig/2, " Hz\n")
print("\nFeedback Resistor: ", R_f, " Ohm\n")
print("\nFeedback Capacitor: ", C_f*1e12, " pF\n")
print("\nCorner Frequency of TIA: ", 1/(2*np.pi*R_f*C_f), " Hz\n")

Output_Voltage = Input_current*R_f

print("\nInput Current: ", Input_current*1e12, " pA\n")
print("\nOutput Voltage: ", Output_Voltage*1e3, " mV\n")

# DC Error Analysis
# The inverting input bias current, I B− , sums directly with the
# photodiode current for a referred to input (RTI) error equal to
# I B− . This current flows through the feedback resistor, creating a
# referred to output (RTO) error.

V_os = 8e-6 # V
I_bias = 20e-15 # Amp

#Refered to output Error (V_rtoErr)
V_rtoErr = I_bias * R_f

#Error introduced due to Op-amp Voltage offset (V_rtoOs)

V_rtoOs = V_os * (1+(R_f/R_s))

DC_Error = V_rtoErr + V_rtoOs

print("\nDC Error: ", DC_Error, " V\n")
# AC Error Analysis

def Noise_gain(f, R_f, R_s,C_f, C_s):
    
    Noise_gain_1 = 1 + R_f/R_s
    Noise_gain_2 = 1 + C_s/C_f

    f1 = 1/( ( (R_f*R_s)/(R_f+R_s) ) * (C_s + C_f) )

    f2 = 1/(R_f*C_f)

    f3 = f_ugc/(Noise_gain_2)

    Noise_Gain_f = Noise_gain_1*(((2*np.pi*f)/f1 + 1)/((2*np.pi*f)/f2 + 1))
    
    return Noise_Gain_f, f1, f2, f3

AC_Error = Noise_gain(f_sig, R_f, R_s, C_f, C_s)

print("\nNoise Gain Pole Freq 1: ", AC_Error[1], " Hz\n")
print("\nNoise Gain Pole Freq 2: ", AC_Error[2], " Hz\n")
print("\nNoise Gain Pole Freq 3: ", AC_Error[3], " Hz\n")

# Noise Sources for Photodiode Interface

Noise_Rf = np.sqrt(4*k*Temp*R_f) # Noise due to Feedback Resistor

Noise_PD = (R_f/R_s)*np.sqrt(4*k*Temp*R_s) # Noise due to Photodiode

Noise_I_n = R_f * I_n # Noise due to Current Noise Density

Noise_V_n = V_n * AC_Error[0] # Noise due to Voltage Noise Density

Total_Noise = (Noise_V_n + Noise_I_n + Noise_PD + Noise_Rf)

print("\nVoltage Noise at Signal Frequency: ", (Noise_V_n), " V\n" )
print("\nCurrent Noise of Op-amp: ", (Noise_I_n), "A\n" )
print("\nPhotodiode Noise at Room Temperature: ", (Noise_PD), " V\n" )
print("\nFeedback Resistor Noise at Room Temperature: ", (Noise_Rf), " V\n" )
print("\nTotal TIA Noise at Signal Frequency: ", Total_Noise, " V\n" )
print("\nSignal to Noise of Minimum Input Signal: ", 20*np.log10(Output_Voltage/(Total_Noise + DC_Error)), " dB\n")

