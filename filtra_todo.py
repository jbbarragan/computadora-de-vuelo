#by joshua barragán Guardado 
import GUI
import matplotlib.pyplot as plt
import numpy as np
from math import atan2, degrees, sqrt

#from google.colab import files
#uploaded = files.upload()

# Filtro de media
def media_movil(data, ventana=3):
    return np.convolve(data, np.ones(ventana)/ventana, mode='valid')

# Filtro de Kalman
class FiltroKalman:
    def __init__(self, q=1e-5, r=1e-2):
        self.q = q  # Varianza del ruido del proceso
        self.r = r  # Varianza del ruido de la medida
        self.x = 0  # Valor estimado inicial
        self.p = 1  # Error de estimación inicial

    def filtrar(self, z):
        # Predicción
        self.p = self.p + self.q

        # Actualización
        k = self.p / (self.p + self.r)  # Ganancia de Kalman
        self.x = self.x + k * (z - self.x)  # Actualización del valor estimado
        self.p = (1 - k) * self.p  # Actualización del error de estimación

        return self.x

# Cargar el archivo
def leer_datos(archivo):
    # Arreglos para los datos
    temperatura = []
    presion = []
    humedad = []
    aceleracion_x = []
    aceleracion_y = []
    aceleracion_z = []
    vel_angular_x = []
    vel_angular_y = []
    vel_angular_z = []

    # Leer línea por línea
    with open(archivo, 'r') as f:
        lineas = f.readlines()

    # Evaluar líneas de lectura y discriminar
    for linea in lineas:
        if 'Temperatura' in linea:
            temperatura.append(float(linea.split(': ')[1]))
        elif 'Presion' in linea:
            presion.append(float(linea.split(': ')[1]))
        elif 'Humedad' in linea:
            humedad.append(float(linea.split(': ')[1]))
        elif 'Aceleracion en X' in linea:
            aceleracion_x.append(float(linea.split(': ')[1]))
        elif 'Aceleracion en Y' in linea:
            aceleracion_y.append(float(linea.split(': ')[1]))
        elif 'Aceleracion en Z' in linea:
            aceleracion_z.append(float(linea.split(': ')[1]))
        elif 'Velociad angular en X' in linea:
            vel_angular_x.append(float(linea.split(': ')[1]))
        elif 'Velociad angular en Y' in linea:
            vel_angular_y.append(float(linea.split(': ')[1]))
        elif 'Velociad angular en Z' in linea:
            vel_angular_z.append(float(linea.split(': ')[1]))

    return (temperatura, presion, humedad, aceleracion_x, aceleracion_y,
            aceleracion_z, vel_angular_x, vel_angular_y, vel_angular_z)

# Función para obtener la inclinación
def calcular_inclinacion(acel_x, acel_y, acel_z):
    inclinacion_x = atan2(acel_y, sqrt(acel_x**2 + acel_z**2))
    inclinacion_y = atan2(-acel_x, sqrt(acel_y**2 + acel_z**2))

    inclinacion_x = degrees(inclinacion_x)
    inclinacion_y = degrees(inclinacion_y)

    return inclinacion_x, inclinacion_y

# Graficar todo
def graficar_datos(temperatura, presion, humedad,
                   aceleracion_x, aceleracion_y, aceleracion_z,
                   vel_angular_x, vel_angular_y, vel_angular_z, ventana_filtro=5):

    # Aplicar filtro de media
    temperatura_suave = media_movil(temperatura, ventana=ventana_filtro)
    presion_suave = media_movil(presion, ventana=ventana_filtro)
    humedad_suave = media_movil(humedad, ventana=ventana_filtro)
    aceleracion_x_suave = media_movil(aceleracion_x, ventana=ventana_filtro)
    aceleracion_y_suave = media_movil(aceleracion_y, ventana=ventana_filtro)
    aceleracion_z_suave = media_movil(aceleracion_z, ventana=ventana_filtro)
    vel_angular_x_suave = media_movil(vel_angular_x, ventana=ventana_filtro)
    vel_angular_y_suave = media_movil(vel_angular_y, ventana=ventana_filtro)
    vel_angular_z_suave = media_movil(vel_angular_z, ventana=ventana_filtro)

    # Calcular inclinación después del filtro
    inclinacion_x = []
    inclinacion_y = []

    kalman_x = FiltroKalman()
    kalman_y = FiltroKalman()

    for i in range(len(aceleracion_x_suave)):
        ix, iy = calcular_inclinacion(aceleracion_x_suave[i], aceleracion_y_suave[i], aceleracion_z_suave[i])
        inclinacion_x.append(kalman_x.filtrar(ix))
        inclinacion_y.append(kalman_y.filtrar(iy))

    plt.figure(figsize=(12, 18))

    # Graficar temperatura
    plt.subplot(6, 3, 1)
    plt.plot(temperatura, color='r', label='Temperatura (Original)', alpha=0.5)
    plt.plot(range(len(temperatura_suave)), temperatura_suave, color='r', label='Temperatura (Suavizada)', linestyle='--')
    plt.title('Temperatura')
    plt.xlabel('Tiempo')
    plt.ylabel('Temperatura (°C)')
    plt.legend()

    # Graficar presión
    plt.subplot(6, 3, 2)
    plt.plot(presion, color='b', label='Presión (Original)', alpha=0.5)
    plt.plot(range(len(presion_suave)), presion_suave, color='b', label='Presión (Suavizada)', linestyle='--')
    plt.title('Presión')
    plt.xlabel('Tiempo')
    plt.ylabel('Presión (Pa)')
    plt.legend()

    # Graficar humedad
    plt.subplot(6, 3, 3)
    plt.plot(humedad, color='g', label='Humedad (Original)', alpha=0.5)
    plt.plot(range(len(humedad_suave)), humedad_suave, color='g', label='Humedad (Suavizada)', linestyle='--')
    plt.title('Humedad')
    plt.xlabel('Tiempo')
    plt.ylabel('Humedad (%)')
    plt.legend()

    # Graficar aceleraciones
    plt.subplot(6, 3, 4)
    plt.plot(aceleracion_x, color='purple', label='Aceleración X (Original)', alpha=0.5)
    plt.plot(range(len(aceleracion_x_suave)), aceleracion_x_suave, color='purple', label='Aceleración X (Suavizada)', linestyle='--')
    plt.title('Aceleración en X')
    plt.xlabel('Tiempo')
    plt.ylabel('Aceleración (m/s²)')
    plt.legend()

    plt.subplot(6, 3, 5)
    plt.plot(aceleracion_y, color='orange', label='Aceleración Y (Original)', alpha=0.5)
    plt.plot(range(len(aceleracion_y_suave)), aceleracion_y_suave, color='orange', label='Aceleración Y (Suavizada)', linestyle='--')
    plt.title('Aceleración en Y')
    plt.xlabel('Tiempo')
    plt.ylabel('Aceleración (m/s²)')
    plt.legend()

    plt.subplot(6, 3, 6)
    plt.plot(aceleracion_z, color='brown', label='Aceleración Z (Original)', alpha=0.5)
    plt.plot(range(len(aceleracion_z_suave)), aceleracion_z_suave, color='brown', label='Aceleración Z (Suavizada)', linestyle='--')
    plt.title('Aceleración en Z')
    plt.xlabel('Tiempo')
    plt.ylabel('Aceleración (m/s²)')
    plt.legend()

    # Graficar velocidades angulares
    plt.subplot(6, 3, 7)
    plt.plot(vel_angular_x, color='cyan', label='Vel. Angular X (Original)', alpha=0.5)
    plt.plot(range(len(vel_angular_x_suave)), vel_angular_x_suave, color='cyan', label='Vel. Angular X (Suavizada)', linestyle='--')
    plt.title('Velocidad Angular en X')
    plt.xlabel('Tiempo')
    plt.ylabel('Vel. Angular (rad/s)')
    plt.legend()

    plt.subplot(6, 3, 8)
    plt.plot(vel_angular_y, color='magenta', label='Vel. Angular Y (Original)', alpha=0.5)
    plt.plot(range(len(vel_angular_y_suave)), vel_angular_y_suave, color='magenta', label='Vel. Angular Y (Suavizada)', linestyle='--')
    plt.title('Velocidad Angular en Y')
    plt.xlabel('Tiempo')
    plt.ylabel('Vel. Angular (rad/s)')
    plt.legend()

    plt.subplot(6, 3, 9)
    plt.plot(vel_angular_z, color='lime', label='Vel. Angular Z (Original)', alpha=0.5)
    plt.plot(range(len(vel_angular_z_suave)), vel_angular_z_suave, color='lime', label='Vel. Angular Z (Suavizada)', linestyle='--')
    plt.title('Velocidad Angular en Z')
    plt.xlabel('Tiempo')
    plt.ylabel('Vel. Angular (rad/s)')
    plt.legend()

    # Graficar inclinaciones
    plt.subplot(6, 3, 10)
    plt.plot(inclinacion_x, color='cyan', label='Inclinación X (Kalman)', linestyle='--')
    plt.title('Inclinación en X (Grados)')
    plt.xlabel('Tiempo')
    plt.ylabel('Inclinación (°)')
    plt.legend()

    plt.subplot(6, 3, 11)
    plt.plot(inclinacion_y, color='magenta', label='Inclinación Y (Kalman)', linestyle='--')
    plt.title('Inclinación en Y (Grados)')
    plt.xlabel('Tiempo')
    plt.ylabel('Inclinación (°)')
    plt.legend()

    # Mostrar la gráfica
    plt.tight_layout()
    plt.show()

# Archivo
archivo = 'Telemetria_muestra.txt'
#archivo = str(GUI.DataDisplayGUI.get_file_name)
# Leer archivo
(temperatura, presion, humedad, aceleracion_x, aceleracion_y,
 aceleracion_z, vel_angular_x, vel_angular_y, vel_angular_z) = leer_datos(archivo)

# Graficar todos los datos con filtro
graficar_datos(temperatura, presion, humedad, aceleracion_x, aceleracion_y,
               aceleracion_z, vel_angular_x, vel_angular_y, vel_angular_z)