import matplotlib.pyplot as plt
import numpy as np
from math import atan2, degrees, sqrt
import os
import tkinter as tk
from tkinter import filedialog

# Crear la carpeta "graficas" si no existe
os.makedirs("graficas", exist_ok=True)

def media_movil(data, ventana=3):
    return np.convolve(data, np.ones(ventana) / ventana, mode='valid')

def calcular_y_graficar_altitud(aceleracion_y, delta_t=1):
    # Suavizar datos de aceleración en Y
    aceleracion_y_suave = media_movil(aceleracion_y)

    # Calcular velocidad y altitud
    velocidad = np.cumsum(aceleracion_y_suave * delta_t)  # Integral de aceleración para obtener velocidad
    altitud = np.cumsum(velocidad * delta_t)  # Integral de velocidad para obtener altitud
    altitud_maxima = np.max(altitud)

    # Graficar altitud
    plt.figure()
    plt.plot(altitud, label='Altitud')
    plt.title('Altitud Calculada')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Altitud (m)')
    plt.legend()
    plt.savefig(os.path.join("graficas", "altitud.png"))
    plt.close()

    print(f"Altitud máxima alcanzada: {altitud_maxima:.2f} m")
    return altitud_maxima

class FiltroKalman:
    def __init__(self, q=1e-5, r=1e-2):
        self.q = q
        self.r = r
        self.x = 0
        self.p = 1

    def filtrar(self, z):
        self.p = self.p + self.q
        k = self.p / (self.p + self.r)
        self.x = self.x + k * (z - self.x)
        self.p = (1 - k) * self.p
        return self.x

# Función para seleccionar el archivo
def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de datos", filetypes=[("Archivos de texto", "*.txt")])
    return archivo

# Cargar el archivo
def leer_datos(archivo):
    temperatura, presion, humedad = [], [], []
    aceleracion_x, aceleracion_y, aceleracion_z = [], [], []
    vel_angular_x, vel_angular_y, vel_angular_z = [], [], []

    with open(archivo, 'r') as f:
        for linea in f:
            datos = list(map(float, linea.strip().split(',')))
            temperatura.append(datos[0])  # Temp_BME
            presion.append(datos[1])      # Pres_BME
            humedad.append(datos[2])      # Hume_BME
            aceleracion_x.append(datos[10])  # Accel_X
            aceleracion_y.append(datos[11])  
            aceleracion_z.append(datos[12])  
            vel_angular_x.append(datos[7])   
            vel_angular_y.append(datos[8])   
            vel_angular_z.append(datos[9])   

    return (temperatura, presion, humedad, aceleracion_x, aceleracion_y,
            aceleracion_z, vel_angular_x, vel_angular_y, vel_angular_z)

def calcular_inclinacion(acel_x, acel_y, acel_z):
    inclinacion_x = atan2(acel_y, sqrt(acel_x**2 + acel_z**2))
    inclinacion_y = atan2(-acel_x, sqrt(acel_y**2 + acel_z**2))
    return degrees(inclinacion_x), degrees(inclinacion_y)

def graficar_y_guardar(dato, suavizado, titulo, eje_y, nombre_archivo):
    plt.figure()
    plt.plot(dato, label=f'{titulo} (Original)', alpha=0.5)
    plt.plot(range(len(suavizado)), suavizado, linestyle='--', label=f'{titulo} (Suavizado)')
    plt.title(titulo)
    plt.xlabel('Tiempo')
    plt.ylabel(eje_y)
    plt.legend()

    ruta = os.path.join("graficas", f"{nombre_archivo}.png")
    if os.path.exists(ruta):
        os.remove(ruta)
    plt.savefig(ruta)
    plt.close()

def graficar_datos(temperatura, presion, humedad,
                   aceleracion_x, aceleracion_y, aceleracion_z,
                   vel_angular_x, vel_angular_y, vel_angular_z, ventana_filtro=5):
 
    temperatura_suave = media_movil(temperatura, ventana=ventana_filtro)
    presion_suave = media_movil(presion, ventana=ventana_filtro)
    humedad_suave = media_movil(humedad, ventana=ventana_filtro)
    aceleracion_x_suave = media_movil(aceleracion_x, ventana=ventana_filtro)
    aceleracion_y_suave = media_movil(aceleracion_y, ventana=ventana_filtro)
    aceleracion_z_suave = media_movil(aceleracion_z, ventana=ventana_filtro)
    vel_angular_x_suave = media_movil(vel_angular_x, ventana=ventana_filtro)
    vel_angular_y_suave = media_movil(vel_angular_y, ventana=ventana_filtro)
    vel_angular_z_suave = media_movil(vel_angular_z, ventana=ventana_filtro)
    altitud_maxima = calcular_y_graficar_altitud(aceleracion_y, delta_t=0.1)

    inclinacion_x, inclinacion_y = [], []
    kalman_x, kalman_y = FiltroKalman(), FiltroKalman()
    for i in range(len(aceleracion_x_suave)):
        ix, iy = calcular_inclinacion(aceleracion_x_suave[i], aceleracion_y_suave[i], aceleracion_z_suave[i])
        inclinacion_x.append(kalman_x.filtrar(ix))
        inclinacion_y.append(kalman_y.filtrar(iy))

    graficar_y_guardar(temperatura, temperatura_suave, 'Temperatura', 'Temperatura (°C)', 'temperatura')
    graficar_y_guardar(presion, presion_suave, 'Presión', 'Presión (Pa)', 'presion')
    graficar_y_guardar(humedad, humedad_suave, 'Humedad', 'Humedad (%)', 'humedad')
    graficar_y_guardar(aceleracion_x, aceleracion_x_suave, 'Aceleración en X', 'Aceleración (m/s²)', 'aceleracion_x')
    graficar_y_guardar(aceleracion_y, aceleracion_y_suave, 'Aceleración en Y', 'Aceleración (m/s²)', 'aceleracion_y')
    graficar_y_guardar(aceleracion_z, aceleracion_z_suave, 'Aceleración en Z', 'Aceleración (m/s²)', 'aceleracion_z')
    graficar_y_guardar(vel_angular_x, vel_angular_x_suave, 'Velocidad Angular en X', 'Vel. Angular (rad/s)', 'vel_angular_x')
    graficar_y_guardar(vel_angular_y, vel_angular_y_suave, 'Velocidad Angular en Y', 'Vel. Angular (rad/s)', 'vel_angular_y')
    graficar_y_guardar(vel_angular_z, vel_angular_z_suave, 'Velocidad Angular en Z', 'Vel. Angular (rad/s)', 'vel_angular_z')
    graficar_y_guardar(inclinacion_x, inclinacion_x, 'Inclinación en X', 'Grados', 'inclinacion_x')
    graficar_y_guardar(inclinacion_y, inclinacion_y, 'Inclinación en Y', 'Grados', 'inclinacion_y')

# Seleccionar el archivo
archivo = seleccionar_archivo()

if archivo:
    (temperatura, presion, humedad, aceleracion_x, aceleracion_y,
    aceleracion_z, vel_angular_x, vel_angular_y, vel_angular_z) = leer_datos(archivo)
    
    graficar_datos(temperatura, presion, humedad, aceleracion_x, aceleracion_y,
                   aceleracion_z, vel_angular_x, vel_angular_y, vel_angular_z)
else:
    print("No se seleccionó ningún archivo.")
