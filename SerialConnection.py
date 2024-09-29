#by astra
import serial
import serial.tools.list_ports

class SerialConnection:
    def __init__(self):
        self.serial = None
        self.connected = False

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
        """Cerrar la conexión serial."""
        if self.serial and self.connected:
            self.serial.close()
            self.connected = False
            print("Conexión cerrada.")

    def read_data(self):
        """Leer datos del puerto serial."""
        if self.connected and self.serial.in_waiting > 0:
            try:
                return self.serial.readline().decode('utf-8').strip()
            except UnicodeDecodeError:
                return None
        return None
