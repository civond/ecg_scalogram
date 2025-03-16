import numpy as np
import wfdb
import matplotlib.pyplot as plt

from utils import *

def main():
    data = [wfdb.rdsamp("data/00001_hr")]
    data = np.array([signal for signal, meta in data])[0]

    lead_1 = data[:, 0]
    lead_2 = data[:,1]
    lead_3 = data[:,2]
    fs=500

    # Bandpass to remove drift and basic denoising
    filtered = bandpass_signal(lead_2, fs, 25, 150)

    # Apply wavelet denoising thresholing
    reconstructed_signal = wavelet_denoise(filtered)

    # Generate scalogram
    [coefficients, frequencies] = generate_scalogram(reconstructed_signal, fs)
    
    # Apply log
    data = np.abs(coefficients)
    data = np.log(data+1)

    # Generate scalogram image for cv2
    scalogram_to_image(data, write_img=True)


    t = np.linspace(0, len(lead_2) / fs, len(lead_2))

    # Plot waveform
    plt.figure(1)
    plt.subplot(2,1,1)
    plt.grid(True)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.plot(t, lead_2, color='c')
    plt.plot(t,filtered, color='b')
    plt.title("Lead II")
    plt.legend(['Raw ECG (II)', "Filtered ECG (II)"])

    plt.xlim(0,t[-1])
    #plt.xlim(0,2)
    plt.tight_layout()

    plt.subplot(2,1,2)
    plt.grid(True)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Lead II After Wavelet Denoising")
    plt.plot(t,reconstructed_signal, color='r')
    plt.xlim(0,t[-1])
    #plt.xlim(0,2)
    plt.tight_layout()

    # Plot scalogram matplotlib    
    cmap = plt.get_cmap('jet', 256)
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111)
    t = np.arange(data.shape[1]) / fs 
    

    ax.pcolormesh(t, frequencies, data, cmap=cmap, 
                vmin=data.min(),
                vmax=np.percentile(data, 99.95), 
                shading='auto')
    ax.set_yscale('log')
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    plt.tight_layout()

    plt.show()
    
main()