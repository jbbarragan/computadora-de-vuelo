#by astra
import serial

puerto = 'COM13'  # Cambia esto al puerto que corresponda
baudrate = 9600

# Crear objeto serial
ser = serial.Serial(puerto, baudrate)

# Leer datos del puerto
try:
    while True:
        if ser.in_waiting > 0:  # Verificar si hay datos disponibles para leer
            mensaje = ser.readline().decode('utf-8').strip()
            print(f"Mensaje recibido: {mensaje}")
except KeyboardInterrupt:
    print("Interrupción del programa.")
finally:
    ser.close()  # Cerrar el puerto cuando se termina