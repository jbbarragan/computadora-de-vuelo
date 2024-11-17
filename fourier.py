import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la señal
Fs = 1000  # Frecuencia de muestreo (Hz)
T = 1 / Fs  # Intervalo de muestreo
t = np.arange(0, 1, T)  # Vector de tiempo de 1 segundo

# Generamos una señal con dos componentes de frecuencia
f1 = 50  # Frecuencia de la primera componente (Hz)
f2 = 120  # Frecuencia de la segunda componente (Hz)
signal = np.sin(2 * np.pi * 15 * t) + np.sin(2 * np.pi * 20 * t)

# Aplicamos la Transformada de Fourier
fft_signal = np.fft.fft(signal)
N = len(signal)
frequencies = np.fft.fftfreq(N, T)

# Tomamos el módulo del resultado para obtener la magnitud de la frecuencia
magnitude = np.abs(fft_signal) / N

# Visualizamos la señal original y su espectro de frecuencia
plt.figure(figsize=(12, 6))

# Señal en el dominio del tiempo
plt.subplot(2, 1, 1)
plt.plot(t, signal)
plt.title("Señal en el tiempo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")

# Espectro de frecuencia
plt.subplot(2, 1, 2)
plt.stem(frequencies[:N // 2], magnitude[:N // 2], 'b', markerfmt=" ", basefmt="-b")
plt.title("Espectro de frecuencia")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")
plt.tight_layout()
plt.show()
