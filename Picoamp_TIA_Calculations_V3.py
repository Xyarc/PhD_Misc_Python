import numpy as np
import matplotlib.pyplot as plt

####### Functions ########
def Noise_gain(Opamp, f, R_f, R_s,C_f, C_s):
    
    Noise_gain_1 = 1 + R_f/R_s
    Noise_gain_2 = 1 + C_s/C_f

    f1 = 1/( ( (R_f*R_s)/(R_f+R_s) ) * (C_s + C_f) )

    f2 = 1/(R_f*C_f)

    f3 = Opamp[2]/(Noise_gain_2)

    Noise_Gain_f = Noise_gain_1*(((2*np.pi*f)/f1 + 1)/((2*np.pi*f)/f2 + 1))
    
    return Noise_Gain_f, f1, f2, f3

def TIA_Comparison(Opamp, f_sig, I_in, R_f, R_s, C_f, read_out = False):
    
    # "Op-amp name": [Voltage Noise Density, Current Noise Density, Gain Bandwidth Product, Input Offset Voltage, Input Offset Current, Input Capacitance]
    # Theoretical Feedback Capacitor
    
    C_s = 140e-12 + Opamp[5] # F - Photodiode Capacitance and Op-amp Capacitance
    
    Output_Voltage = I_in*R_f

    C_f_theory = np.sqrt(C_s/(np.pi*2*R_f*Opamp[2]))
    
    # DC Error Analysis
    # The inverting input bias current, I B− , sums directly with the
    # photodiode current for a referred to input (RTI) error equal to
    # I B− . This current flows through the feedback resistor, creating a
    # referred to output (RTO) error.

    #Refered to output Error (V_rtoErr)
    V_rtoErr = Opamp[4] * R_f

    #Error introduced due to Op-amp Voltage offset (V_rtoOs)

    V_rtoOs = Opamp[3] * (1+(R_f/R_s))

    DC_Error = V_rtoErr + V_rtoOs

    if read_out:
        print("\n%s DC Error: %E V\n" % (Opamp_Current, DC_Error))
    
    # AC Error Analysis

    AC_Error = Noise_gain(Opamp,f_sig, R_f, R_s, C_f, C_s)

    Noise_Rf = np.sqrt(4*k_b*Temp*R_f) # Noise due to Feedback Resistor

    Noise_PD = (R_f/R_s)*np.sqrt(4*k_b*Temp*R_s) # Noise due to Photodiode

    Noise_I_n = R_f * Opamp[1] # Noise due to Current Noise Density

    Noise_V_n = Opamp[0] * AC_Error[0] # Noise due to Voltage Noise Density

    #print("\n", R_f, "\n", R_s, "\n", Temp, "\n", k)
    
    #print("\nPhotodiode Noise at Room Temperature: ", (Noise_PD), " V\n" )
    #print("\nFeedback Resistor Noise at Room Temperature: ", (Noise_Rf), " V\n" )

    Total_Noise = (Noise_V_n + Noise_I_n + Noise_PD + Noise_Rf)

    Sig_to_Noise = 20*np.log10(Output_Voltage/(Total_Noise ))#+ DC_Error))
    
    if read_out:
        print("\n ------- Op-Amp: %s -------\n" % Opamp_Current)
        print("\nTheoretical Stable Feedback Capacitor: ", C_f_theory*1e-12, " pF\n")
        print("\nDC Error: %E V\n" % DC_Error)
        print("\nVoltage Noise at Signal Frequency: %E V\n" % (Noise_V_n))
        print("\nCurrent Noise of Op-amp: %E V\n" %(Noise_I_n))
        print("\nPhotodiode Noise at Room Temperature: %E V\n" %(Noise_PD))
        print("\nFeedback Resistor Noise at Room Temperature: %E V\n" %(Noise_Rf))
        print("\nTotal TIA Noise at Signal Frequency: %E V\n" %Total_Noise )

    return Sig_to_Noise

######## Constants ########

Temp = 293.15 # Room Temp

k_b = 1.380649e-23 # Boltzmann

######## Op-Amp Properties ########

# "Op-amp name": [Voltage Noise Density, Current Noise Density, Gain Bandwidth Product, Input Offset Voltage, Input Offset Current, Input Capacitance]
Opamps = {
    "ADA4530-1": [20e-9, 6.41e-15, 2e6, 9e-6, 20e-15, 8e-12],
    #"ADA4177-1": [8e-9, 0.2e-12, 3.5e6, 3e-6, 0.1e-9, 8e-12],
    #"AD797B": [1.7e-9, 2e-12, 110e6, 30e-6, 120e-9, 5e-12],
    "ADA4817-1": [12e-9, 2.5e-15, 1e9, 0.4e3, 1e-12, 1.3e-12]

}

######## Parameters of Intrest ########

f_sig = np.array([421]) # Hz

# TIA Capacitance & Resistance

R_f =  250e6 # Feedback Resistor of TIA

R_s = 5e9 # Shunt Resistor of the Photodiode

C_f = 1e-12 # Farads - Feedback Capacitor of the TIA

Input_current = 1e-12 #Amps - Min Signal current

Output_Voltage = Input_current*R_f
print("\nSignal Frequency: ", f_sig, " Hz\n")
print("\nModulation Frequency: ", f_sig/2, " Hz\n")
print("\nFeedback Resistor: ", R_f, " Ohm\n")
print("\nFeedback Capacitor: ", C_f*1e12, " pF\n")
print("\nCorner Frequency of TIA: ", 1/(2*np.pi*R_f*C_f), " Hz\n")
print("\nInput Current: ", Input_current*1e12, " pA\n")
print("\nOutput Voltage: ", Output_Voltage*1e3, " mV\n")


######## Op-Amp Comparison ########
Opamps_SNR = np.zeros(len(Opamps.keys()))

k=0

for Opamp_Current in Opamps.keys():
    
    Opamps_SNR[k] = TIA_Comparison(Opamps[Opamp_Current], f_sig[0], Input_current, R_f, R_s, C_f, False)
    print("%s | Signal to Noise: %f \n" %(Opamp_Current, Opamps_SNR[k]))
    k+=1

