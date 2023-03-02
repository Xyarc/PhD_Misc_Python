import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

#
freq_1 = 476.5 # Half of Frequency 2
freq_2 = 953 # Frequency we wish to measure

Period = 50/freq_2 # How many cycles to compute

def Power(V_0, V_1, R, freq):
    V = V_0 + V_1*np.sin(2*np.pi*freq*t)
    return (V*V)/R

t = np.linspace(0, Period, 5000)

No_offset = Power(0, .3, 10, freq_1)
#Large_offset =  Power(5, .5, 10, freq_2)
Similar_offset = Power(0.2, .1, 10, freq_2)

# Estimating the Phase Shift of the off-set vs No-Offset

def Phase_sift_estimate(Sig1, Sig2, freq):
    #Correlates both signals then produces plots of both + the Correllation vs Phase Delay. Prints & returns the Phase delay
    import scipy.signal as signal

    corr = signal.correlate(Sig1, Sig2)

    lags = signal.correlation_lags(len(Sig2), len(Sig1))

    lags_deg = lags*(Period/len(t))*360*freq
    
    corr /= np.max(corr)

    Phase_delay = lags_deg[np.argmax(corr)]  # Find the x value corresponding to the maximum y value
    print(Phase_delay)

    fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, figsize=(4.8, 4.8))

    ax_orig.plot(Sig1)
    ax_orig.set_xlim((0, 1000))
    ax_orig.set_title('No-offset with 300mV Modulation')

    

    ax_noise.plot(Sig2)
    ax_noise.set_xlim((0, 1000))
    ax_noise.set_title('200mV Off-set with 100mV Modulation')

    ax_noise.set_xlabel('Sample Number')

    ax_orig.set_xlabel('Sample Number')

    ax_corr.plot(lags_deg, corr)
    ax_corr.vlines(Phase_delay, 0, 1.1, color = "red", label="Phase Delay = %f Degrees" %(Phase_delay))
    ax_corr.legend()
    ax_corr.set_xlim((-1500, 1500))
    ax_corr.set_ylim((0, 1))

    ax_corr.set_title('Cross-correlated signals')

    ax_corr.set_xlabel('Phase Delay (Deg)')

    ax_orig.margins(0, 0.1)

    ax_noise.margins(0, 0.1)

    ax_corr.margins(0, 0.1)
    ax_corr.grid()

    fig.tight_layout()

    plt.show()

    return Phase_delay

Phase_sift_estimate(No_offset, Similar_offset)


#fig, ax = plt.subplots()
#fig.set_figheight(4)
#fig.set_figwidth(7)

#ax.plot(t, No_offset , label = "No Off-set", color='orange', marker='', linestyle='-')
#ax.plot(t, Large_offset , label = "Large Off-set", color='red', marker='.', linestyle='-')
#ax.plot(t, Similar_offset , label = "Similar Off-set", color='cyan', marker='', linestyle='-')

#ax.set_title("Heating Modulation")
#ax.set_xlabel("Time (Seconds)")
#ax.set_ylabel("Heating Power(W)")
    

#fig.tight_layout()
#plt.show()
