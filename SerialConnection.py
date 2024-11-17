# AUTHOR: ASTRA CLUB
# DATE: 2024
# FILE: COMPUTADORA DE VUELO/SerialConnection.py
# Params: main.py
import serial
import serial.tools.list_ports
import time

class SerialConnection:
    def __init__(self, log_file="datos_recibidos.txt"):
        self.serial = None
        self.connected = False
        self.log_file = log_file
        self.file = open(self.log_file, "a")

    def list_ports(self):
        """Listar los puertos COM disponibles."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect(self, port, baudrate=9600):
        """Conectar al puerto COM seleccionado."""
        try:
            self.serial = serial.Serial(port, baudrate, timeout=1)
            self.connected = True
            print(f"Conectado a {port}")
        except serial.SerialException as e:
            print(f"Error de conexión: {e}")
            self.connected = False

    def disconnect(self):
        """Cerrar la conexión serial y el archivo de log."""
        if self.serial and self.connected:
            self.serial.close()
            self.connected = False
            print("Conexión cerrada.")
        self.file.close()

    def read_data(self):
        """Leer datos del puerto serial y guardarlos en un archivo."""
        if self.connected and self.serial.in_waiting > 0:
            try:
                data = self.serial.readline().decode('utf-8').strip()
                self.file.write(data + "\n")
                self.file.flush() 
                return data
            except UnicodeDecodeError:
                return None
        return None


if __name__ == "__main__":
    connection = SerialConnection()
    

    available_ports = connection.list_ports()
    print("Puertos disponibles:", available_ports)
    
    
    if available_ports:
        connection.connect(available_ports[0], baudrate=9600)
        
       
        try:
            while connection.connected:
                data = connection.read_data()
                if data:
                    print("Datos recibidos:", data)
        except KeyboardInterrupt:
            print("\nFinalizando lectura.")
        finally:
            connection.disconnect()
    else:
        print("No se encontraron puertos COM disponibles.")
