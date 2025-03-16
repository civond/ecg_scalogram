# ECG Preprocessing
This repository preprocesses ECG signals (lead II) and generates the corresponding scalogram for use in machine learning applications. 
I used two steps: 
<ol>
  <li>Bandpass filtering to remove artifacts and baseline drift (Wc: [40,150]).</li>
  <li>Wavelet denoising using adaptive wavelet thresholding (pywt).</li>
</ol>

<img src="figures/Figure_1.png" align=center width=500px></img>

<h3> Scalogram of Bandpassed ECG Signal: </h3>
<img src="figures/scalogram_colored_image.png"></img>
<h3> Scalogram of ECG Signal After Wavelet Denoising: </h3>
<img src="figures/scalogram_colored_image2.png"></img>
