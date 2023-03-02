import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
#from scipy.interpolate import InterpolatedUnivariateSpline
import scipy.integrate as integrate


########## Reading Data to Dataframes ###############
files = os.listdir('C:/Users/Conor/Documents/LTspiceXVII/PEAR_2')

R_f = np.linspace(100, 600, 21)
print(R_f)

First_Trans = True
First_Noise = True

i=0
j=0
for file in files:
    if file.endswith("_Trans.txt"):

      
        
        if First_Trans:
            Gain_df = pd.read_csv('C:/Users/Conor/Documents/LTspiceXVII/PEAR_2/' + file, sep="\t")
            Gain_df.columns = ['time', str(int(R_f[i]))+" MOhm"]
            #print(Gain_df)



            First_Trans = False
            i += 1
        
        else:
            temp = pd.read_csv('C:/Users/Conor/Documents/LTspiceXVII/PEAR_2/' + file, sep="\t")
            temp.columns = ['time', str(int(R_f[i]))+" MOhm"]
            Gain_df = pd.merge(Gain_df, temp, on='time', how='outer')


            i += 1

    
    elif file.endswith("_Noise.txt"):
        if First_Noise:
            Noise_df = pd.read_csv('C:/Users/Conor/Documents/LTspiceXVII/PEAR_2/' + file, sep="\t")
            
            Noise_df.columns = ['frequency', str(int(R_f[i]))+" MOhm"]
            


            First_Noise = False
            j += 1

        else:
            temp = pd.read_csv('C:/Users/Conor/Documents/LTspiceXVII/PEAR_2/' + file, sep="\t")
            temp.columns = ['frequency', str(int(R_f[i]))+" MOhm"]

            Noise_df = pd.merge(Noise_df, temp, on='frequency', how='outer')



            j += 1

##################### Computations #########################
#Total_Noise_LT = np.array([4.5891e-6, 5.2039e-6, 5.7522e-6, 6.2412e-6, 6.6759e-6, 7.061e-6, 7.4008e-6, 7.6996e-6, 7.9615e-6, 8.1904e-6, 8.3901e-6, 8.564e-6, 8.7152e-6, 8.8466e-6, 8.9605e-6]) # Total V(out_Noise) RMS @ 10 Hz Bandwidth around 421 Hz starting at R_f = 100MOhm to 450 MOhms in steps of 25MOhms.

labels = ["100 MOhm", "125 MOhm", "150 MOhm", "175 MOhm", "200 MOhm", "225 MOhm", "250 MOhm", "275 MOhm", "300 MOhm", "325 MOhm", "350 MOhm", "375 MOhm", "400 MOhm", "425 MOhm", "450 MOhm", "475 MOhm", "500 MOhm", "525 MOhm", "550 MOhm", "575 MOhm", "600 MOhm"]

f_sig = 421 #Hz
Bandwidth = 9.2 #Hz
Total_Noise = np.zeros(len(R_f))
Diffrence_Noise = np.zeros(len(R_f))
Sig_to_Noise = np.zeros(len(R_f))
Sig_Out = np.zeros(len(R_f))
Band_start = f_sig - Bandwidth/2
Band_end = f_sig + Bandwidth/2

Noise_Bandwidth = Noise_df.query("%f < frequency < %f" %(Band_start, Band_end))
#print(Noise_Bandwidth)
for i in range(0, len(Total_Noise)):
        
        Total_Noise[i] = integrate.trapezoid(Noise_Bandwidth[labels[i]], Noise_Bandwidth["frequency"])*0.707
        #Diffrence_Noise[i] = Total_Noise[i] - Total_Noise_LT[i]
        Sig_Out[i] = max(Gain_df[labels[i]])
        Sig_to_Noise[i] = 20*np.log10(Sig_Out[i]/Total_Noise[i])
         

#print(Diffrence_Noise)



############### Plot Settings #######################
fig, axs = plt.subplots(2, 2, figsize = (5, 10))

ax_gain = axs[0,0]
ax_noise = axs[0,1]
ax_comparison = axs[1,0]
ax_SNR = axs[1,1]

############ Plots of Output Signal ############

ax_gain.plot(Gain_df["time"]*1e3, Gain_df["100 MOhm"]*1e3, label = "100 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["125 MOhm"]*1e3, label = "125 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["150 MOhm"]*1e3, label = "150 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["175 MOhm"]*1e3, label = "175 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["200 MOhm"]*1e3, label = "200 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["225 MOhm"]*1e3, label = "225 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["250 MOhm"]*1e3, label = "250 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["275 MOhm"]*1e3, label = "275 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["300 MOhm"]*1e3, label = "300 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["325 MOhm"]*1e3, label = "325 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["350 MOhm"]*1e3, label = "350 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["375 MOhm"]*1e3, label = "375 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["400 MOhm"]*1e3, label = "400 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["425 MOhm"]*1e3, label = "425 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["450 MOhm"]*1e3, label = "450 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["475 MOhm"]*1e3, label = "475 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["500 MOhm"]*1e3, label = "500 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["525 MOhm"]*1e3, label = "525 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["550 MOhm"]*1e3, label = "550 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["575 MOhm"]*1e3, label = "575 MOhm")
ax_gain.plot(Gain_df["time"]*1e3, Gain_df["600 MOhm"]*1e3, label = "600 MOhm")


ax_gain.set_title('1 pA Signal Passed Through ADA4530-1 TIA With Varied Feedback Resistor')
ax_gain.set_ylabel('Output Signal (mV)')
ax_gain.set_xlabel('Time (ms)')
ax_gain.legend(loc = 'lower left')
ax_gain.grid(True)
    
############ Plots of Noise Response ############

ax_noise.plot(Noise_df["frequency"], Noise_df["100 MOhm"]*1e6,label = "100 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["125 MOhm"]*1e6,label = "125 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["150 MOhm"]*1e6,label = "150 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["175 MOhm"]*1e6,label = "175 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["200 MOhm"]*1e6,label = "200 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["225 MOhm"]*1e6,label = "225 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["250 MOhm"]*1e6,label = "250 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["275 MOhm"]*1e6,label = "275 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["300 MOhm"]*1e6,label = "300 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["325 MOhm"]*1e6,label = "325 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["350 MOhm"]*1e6,label = "350 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["375 MOhm"]*1e6,label = "375 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["400 MOhm"]*1e6,label = "400 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["425 MOhm"]*1e6,label = "425 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["450 MOhm"]*1e6,label = "450 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["475 MOhm"]*1e6,label = "475 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["500 MOhm"]*1e6,label = "500 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["525 MOhm"]*1e6,label = "525 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["550 MOhm"]*1e6,label = "550 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["575 MOhm"]*1e6,label = "575 MOhm")
ax_noise.plot(Noise_df["frequency"], Noise_df["600 MOhm"]*1e6,label = "600 MOhm")

#labels = ["100 MOhm", "125 MOhm", "150 MOhm", "175 MOhm", "200 MOhm", "225 MOhm", "250 MOhm", "275 MOhm", "300 MOhm", "325 MOhm", "350 MOhm", "375 MOhm", "400 MOhm", "425 MOhm", "450 MOhm"]

#for label in labels:
    #ax_noise.annotate(label, (Noise_df["frequency"][8000], Noise_df[label][8000]*1e6), textcoords="offset points", xytext=(0,0.1), ha='center')

ax_noise.set_xscale("log")

#ax_noise.vlines(x = [416,421], ymin = 0, ymax = 3, color = "red", label = "Operational Bandwidth", linestyles= "--")
ax_noise.axvspan(416, 426, alpha=.2, color='red', label = "Operational Bandwidth")
ax_noise.set_xlim((0.1, 10e3))
ax_noise.set_ylim((1, 4))

ax_noise.set_title('Noise Response of ADA4530-1 TIA With Varied Feedback Resistor')
ax_noise.set_ylabel(r"Noise ($\mu V/\sqrt{Hz}$)")
ax_noise.set_xlabel('Frequency (Hz)')
ax_noise.legend(loc = 'lower left')
ax_noise.grid(True)

############ Gain Vs Noise ############
ax_comparison_2 = ax_comparison.twinx()

ax_comparison.plot(R_f, Sig_Out*1e3, color = "green", linestyle = "--", marker = "o", label = "Signal")
ax_comparison_2.plot(R_f, Total_Noise*1e6, color = "red", linestyle = "--", marker = "o", label = "Noise")

ax_comparison.set_ylabel(r"Output Voltage ($mV$)")
ax_comparison_2.set_ylabel(r"Output RMS Noise ($\mu V$)")

ax_comparison.set_title('Signal Output and Noise output for a given Feedback Resistor')

ax_noise.set_ylim((0, 0.4))
ax_noise.set_ylim((0, 20))

ax_comparison.set_xlabel(r'Feedback Resistance ($M\Omega$)')
ax_comparison.legend()
ax_comparison.grid(True)

############ SNR ############
ax_SNR.plot(R_f, Sig_to_Noise)

ax_SNR.set_title('Signal to Noise with Increaseing Feedback Resistor')
ax_SNR.set_ylabel("Signal to Noise Ratio (dB)")
ax_SNR.set_xlabel(r'Feedback Resistance ($M\Omega$)')
#ax_SNR.legend(loc = 'lower left')
ax_SNR.grid(True)
plt.tight_layout()
plt.show()