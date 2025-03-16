import pywt
import numpy as np
import cv2
import matplotlib.pyplot as plt
import scipy.signal as signal

def bandpass_signal(data, fs, wcl, wch):
    wn_l = wcl / (0.5*fs)
    wn_h = wch / (0.5*fs)
    [b,a] = signal.butter(10,Wn=[wn_l,wn_h], btype='band')
    filtered = signal.filtfilt(b,a,data)
    return filtered

def wavelet_denoise(signal, wavelet = 'sym6', level=4, method='soft'):
    coeffs = pywt.wavedec(signal, wavelet, level)
    sigma = np.median(np.abs(coeffs[-1])) / 0.6745

    thresholds = [sigma * np.sqrt(2* np.log(len(signal)))] * len(coeffs)

    new_coeffs = [coeffs[0]]
    for i in range(1,len(coeffs)):
        new_coeffs.append(pywt.threshold(coeffs[i], thresholds[i], mode=method))
    
    reconstructed_signal = pywt.waverec(new_coeffs, wavelet)
    return reconstructed_signal

def generate_scalogram(data, fs):
    # Apply wavelet transform
    wavelet = pywt.ContinuousWavelet("morl")
    scales = pywt.central_frequency(wavelet) * fs / np.arange(10,300,0.2)
    [coefficients, frequencies] = pywt.cwt(data, 
                                        scales, 
                                        wavelet, 
                                        sampling_period= 1/fs)
    return coefficients, frequencies

def scalogram_to_image(data, write_img = True):
    vmin = data.min()
    vmax = np.percentile(data, 99.95)
    data_normalized = np.clip((data - vmin) / (vmax - vmin) * 255, 0, 255).astype(np.uint8)
    data_normalized = data_normalized.astype(np.uint8)
    data_normalized = cv2.flip(data_normalized, 0)

    if write_img == True:
        # Grayscale
        cv2.imwrite('scalogram_image3.png', data_normalized)
        
        #Color image
        colored_data = cv2.applyColorMap(data_normalized, cv2.COLORMAP_JET)
        cv2.imwrite('scalogram_colored_image3.png', colored_data)
    else:
        pass