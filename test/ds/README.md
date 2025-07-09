# 📊 DSP LAB-29 - Signal Processing with Python

This repository contains code and visualizations for various fundamental concepts in **Digital Signal Processing (DSP)**, as outlined in DSP Lab-29. Each section demonstrates key DSP operations like signal generation, sampling, filtering, convolution, and spectral analysis using Python libraries.

---

## 📁 Contents

### 🔹 1. Elementary Signal Generation

Generate and plot:
- **Unit Step:** `u(n)`
- **Ramp:** `n * u(n)`
- **Exponential:** `a^n * u(n)`
- **Sine & Cosine:** `sin(ωn)`, `cos(ωn)`

**Filename:** `01_elementary_signals.ipynb`

---

### 🔹 2. Sampling & Aliasing

Demonstrates the **aliasing effect** using the signal:

`x_a(t) = 3cos(100πt)`

Sampled at:
- **200 Hz** (Nyquist rate)
- **75 Hz** (Aliasing visible)

Compare the discrete-time plots.

**Filename:** `02_sampling_aliasing.ipynb`

---

### 🔹 3. Maximum Oscillation at ω = π

Show that `ω = π` results in the **highest oscillation rate** in a discrete-time sinusoid:

`x[n] = cos(ωn)`

**Filename:** `03_max_oscillation.ipynb`

---

### 🔹 4. Complex Analog Signal Sampling

Signal:

`x_a(t) = 3cos(2000πt) + 5sin(6000πt) + 10cos(12000πt)`

Sampled at:
- Below Nyquist
- At Nyquist
- Above Nyquist

Observe and visualize **aliasing and frequency folding**.

**Filename:** `04_complex_sampling.`

---

### 🔹 5. LTI System Convolution

Impulse response:

`h[n] = u(n) - u(n-5)`

Input:

`x[n] = u(n)`

Compute output:

`y[n] = x[n] * h[n]`

Using **convolution sum**.

**Filename:** `05_convolution_lti.ipynb`

---

### 🔹 6. Correlation

Given:
- `x(n) = [1, 3, -2, 4]`
- `y(n) = [2, 3, -1, 3]`
- `z(n) = [2, -1, 4, -2]`

Compute:
- Cross-correlation between `x(n)` and `y(n)`
- Cross-correlation between `y(n)` and `z(n)`

**Filename:** `06_correlation.ipynb`

---

### 🔹 7. Filter Realization

Implement:
- **6-point Averaging Filter:**
  `y[n] = (1/6) * (x[n] + x[n-1] + ... + x[n-5])`
- **6-point Differencing Filter:**
  `y[n] = x[n] - x[n-6]`

**Filename:** `07_filter_realization.ipynb`

---

### 🔹 8. DFT and Windowing

Signal:

`x[n] = sin(2π·1000t) + 0.5sin(2π·2000t + 3π/4)`

Tasks:
- DFT without window
- DFT with Hamming and Hanning windows

Observe:
- **Spectral leakage**
- **Window smoothing effect**

**Filename:** `08_dft_windowing.ipynb`

---

### 🔹 9. Low-Pass FIR Filter Design

- Add high-frequency noise to a signal
- Design **Low-Pass FIR Filter** using Hamming window
- Apply the filter using **convolution**
- Visualize results in time and frequency domain

**Filename:** `09_fir_filter.ipynb`

---

## 🛠 Requirements

Install required libraries with:

```bash
pip install numpy matplotlib scipy
