#by astra & joshua barragán
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import time

class DataDisplayGUI:
    def __init__(self, root, serial_conn):
        """Inicializa la ventana principal con los botones de control y etiquetas de estado."""
        self.root = root
        self.serial_conn = serial_conn
        self.is_recording = False
        self.recording_file = None
       

        # Frame principal
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Frame para el estado de conexión y selección de puerto (Parte superior izquierda)
        self.connection_frame = tk.Frame(self.frame)
        self.connection_frame.grid(row=0, column=0, sticky="nw")

        # Estado de conexión
        self.connection_status = tk.Label(self.connection_frame, text="Estado: Desconectado", width=30, fg="red")
        self.connection_status.pack(pady=10)

        # Lista de puertos COM disponibles
        self.combobox = ttk.Combobox(self.connection_frame, values=self.serial_conn.list_ports())
        self.combobox.pack(padx=5, pady=5)
        self.combobox.set("Selecciona un puerto COM")
        self.combobox.bind("<<ComboboxSelected>>", self.enable_connect_button)

        # Botones de conectar y desconectar
        self.connect_button = tk.Button(self.connection_frame, text="Conectar", command=self.connect_serial, state=tk.DISABLED)
        self.connect_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.disconnect_button = tk.Button(self.connection_frame, text="Desconectar", command=self.disconnect_serial, state=tk.DISABLED)
        self.disconnect_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame para la entrada del nombre de archivo y los botones de grabación (Parte superior derecha)
        self.recording_frame = tk.Frame(self.frame)
        self.recording_frame.grid(row=0, column=1, sticky="ne")

        # Entrada para el nombre del archivo
        self.file_label = tk.Label(self.recording_frame, text="Guardado en Telemetria_muestra.txt")
        self.file_label.pack(padx=5, pady=5)
        #self.file_entry = tk.Entry(self.recording_frame)
        #self.file_entry.insert(0, "prueba.txt")  # Valor predeterminado
        #self.file_entry.pack(padx=5, pady=5)

        # Botones de grabación
        self.start_button = tk.Button(self.recording_frame, text="Start Recording", command=self.start_recording, state=tk.DISABLED)
        self.start_button.pack(padx=5, pady=5)

        self.stop_button = tk.Button(self.recording_frame, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(padx=5, pady=5)

        # Crear cuadros para cada tipo de dato
        self.create_data_labels()

        # Crear etiquetas de máximos y mínimos
        self.create_min_max_labels()

        # Botón para graficar (parte inferior central)
        self.create_graficar_button()  # Llama a la función para crear el botón de graficar

    def enable_connect_button(self, event):
        """Habilitar el botón de conectar cuando se seleccione un puerto."""
        self.connect_button.config(state=tk.NORMAL)

    def connect_serial(self):
        """Establecer la conexión serial con el puerto seleccionado."""
        port = self.combobox.get()
        self.serial_conn.connect(port)
        if self.serial_conn.connected:
            self.connection_status.config(text=f"Estado: Conectado a {port}", fg="green")
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
            self.start_button.config(state=tk.NORMAL)

            # Iniciar la recepción de datos en un hilo separado
            threading.Thread(target=self.receive_data).start()

    def disconnect_serial(self):
        """Cerrar la conexión serial."""
        self.serial_conn.disconnect()
        if not self.serial_conn.connected:
            self.connection_status.config(text="Estado: Desconectado", fg="red")
            self.disconnect_button.config(state=tk.DISABLED)
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)

    def start_recording(self):
        """Comenzar a grabar datos en un archivo de texto."""
        #file_name = self.file_entry.get()
        file_name = "Telemetria_muestra.txt"
        
        # Verificar si el archivo existe, si es así, eliminarlo y crear uno nuevo
        if os.path.exists(file_name):
            os.remove(file_name)

        self.recording_file = open(file_name, "w")
        self.is_recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        return file_name

    def stop_recording(self):
        """Detener la grabación de datos."""
        if self.recording_file:
            self.recording_file.close()
            self.recording_file = None
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def create_data_labels(self):
        """Crea las etiquetas para mostrar los datos en la GUI en cuadros separados."""

        # Crear un marco principal para contener todos los cuadros
        self.data_frames = tk.Frame(self.root)
        self.data_frames.pack(padx=10, pady=10)

        # Cuadro para Velocidad
        self.velocidad_frame = tk.LabelFrame(self.data_frames, text="Velocidad", padx=10, pady=10)
        self.velocidad_frame.grid(row=0, column=0, padx=5, pady=5)
        self.velocidad_labels = {}
        for axis in ['X', 'Y', 'Z']:
            label = tk.Label(self.velocidad_frame, text=f"Bno_aceleracion lineal {axis}: ---")
            label.pack(anchor="w")
            self.velocidad_labels[f"Bno_aceleracion lineal {axis}"] = label

        # Cuadro para Aceleraciones
        self.aceleracion_frame = tk.LabelFrame(self.data_frames, text="Aceleraciones", padx=10, pady=10)
        self.aceleracion_frame.grid(row=0, column=1, padx=5, pady=5)
        self.aceleracion_labels = {}
        for axis in ['X', 'Y', 'Z']:
            label = tk.Label(self.aceleracion_frame, text=f"Bno_acelerometro {axis}: ---")
            label.pack(anchor="w")
            self.aceleracion_labels[f"Bno_acelerometro {axis}"] = label

        # Cuadro para Gravedades
        self.gravedad_frame = tk.LabelFrame(self.data_frames, text="Gravedades", padx=10, pady=10)
        self.gravedad_frame.grid(row=0, column=2, padx=5, pady=5)
        self.gravedad_labels = {}
        for axis in ['X', 'Y', 'Z']:
            label = tk.Label(self.gravedad_frame, text=f"Bno_gravedad {axis}: ---")
            label.pack(anchor="w")
            self.gravedad_labels[f"Bno_gravedad {axis}"] = label

        # Cuadro para Giroscopio
        self.giroscopio_frame = tk.LabelFrame(self.data_frames, text="Giroscopio", padx=10, pady=10)
        self.giroscopio_frame.grid(row=0, column=3, padx=5, pady=5)
        self.giroscopio_labels = {}
        for axis in ['X', 'Y', 'Z']:
            label = tk.Label(self.giroscopio_frame, text=f"Bno_giroscopio {axis}: ---")
            label.pack(anchor="w")
            self.giroscopio_labels[f"Bno_giroscopio {axis}"] = label

        # Cuadro para Magnetómetro
        self.magnetometro_frame = tk.LabelFrame(self.data_frames, text="Magnetómetro", padx=10, pady=10)
        self.magnetometro_frame.grid(row=0, column=4, padx=5, pady=5)
        self.magnetometro_labels = {}
        for axis in ['X', 'Y', 'Z']:
            label = tk.Label(self.magnetometro_frame, text=f"Bno_magnetrometro {axis}: ---")
            label.pack(anchor="w")
            self.magnetometro_labels[f"Bno_magnetrometro {axis}"] = label

        # Cuadro para Condiciones Ambientales (Temperatura, Presión, Humedad)
        self.ambiental_frame = tk.LabelFrame(self.data_frames, text="Condiciones Ambientales", padx=10, pady=10)
        self.ambiental_frame.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="ew")
        self.ambiental_labels = {}
        for field in ["Bmp_temperatura", "Bmp_presion", "Aht_temperatura", "Aht_humedad"]:
            label = tk.Label(self.ambiental_frame, text=f"{field}: ---")
            label.pack(anchor="w")
            self.ambiental_labels[field] = label

        # Cuadro para Orientación
        self.orientacion_frame = tk.LabelFrame(self.data_frames, text="Orientación", padx=10, pady=10)
        self.orientacion_frame.grid(row=1, column=3, padx=5, pady=5, columnspan=2, sticky="ew")
        self.orientacion_labels = {}
        for field in ["Bno_yaw", "Bno_pitch", "Bno_heading", "Bno_roll"]:
            label = tk.Label(self.orientacion_frame, text=f"{field}: ---")
            label.pack(anchor="w")
            self.orientacion_labels[field] = label

        # Unificar todos los cuadros de etiquetas en un diccionario
        self.labels = {**self.velocidad_labels, **self.aceleracion_labels, **self.gravedad_labels,
                       **self.giroscopio_labels, **self.magnetometro_labels, **self.ambiental_labels,
                       **self.orientacion_labels}

    def create_min_max_labels(self):
        """Crea las etiquetas para mostrar las temperaturas y presiones máximas y mínimas."""
        self.max_labels = {}
        self.min_labels = {}

        # Cuadro para máximos y mínimos de temperatura y presión
        self.temp_press_max_min_frame = tk.LabelFrame(self.root, text="Temperaturas y Presiones Máximas y Mínimas", padx=10, pady=10)
        self.temp_press_max_min_frame.pack(padx=10, pady=10, side=tk.TOP, fill=tk.X)

        self.max_labels['Aht_temperatura'] = tk.Label(self.temp_press_max_min_frame, text="Temperatura AHT Máxima: ---")
        self.max_labels['Aht_temperatura'].pack(anchor="w")
        self.min_labels['Aht_temperatura'] = tk.Label(self.temp_press_max_min_frame, text="Temperatura AHT Mínima: ---")
        self.min_labels['Aht_temperatura'].pack(anchor="w")

        self.max_labels['Bmp_presion'] = tk.Label(self.temp_press_max_min_frame, text="Presión Máxima: ---")
        self.max_labels['Bmp_presion'].pack(anchor="w")
        self.min_labels['Bmp_presion'] = tk.Label(self.temp_press_max_min_frame, text="Presión Mínima: ---")
        self.min_labels['Bmp_presion'].pack(anchor="w")

    def update_labels(self, data_list):
        """Actualizar las etiquetas de datos con la información recibida."""
        keys = list(self.labels.keys())

        # Convertir los valores recibidos en float
        data_list = [float(value) for value in data_list]

        for i, value in enumerate(data_list):
            if i < len(keys):
                self.labels[keys[i]].config(text=f"{keys[i]}: {value}")

                # Actualizar máximos y mínimos
                if keys[i] in self.max_labels:
                    current_max = float(self.max_labels[keys[i]].cget("text").split(": ")[1])
                    if value > current_max or current_max == "---":
                        self.max_labels[keys[i]].config(text=f"{keys[i]} Máxima: {value}")

                if keys[i] in self.min_labels:
                    current_min = float(self.min_labels[keys[i]].cget("text").split(": ")[1])
                    if value < current_min or current_min == "---":
                        self.min_labels[keys[i]].config(text=f"{keys[i]} Mínima: {value}")

    def receive_data(self):
        """Hilo que recibe y actualiza los datos en la GUI."""
        while self.serial_conn.connected:
            data = self.serial_conn.read_data()

            if data:
                print(f"Datos recibidos: {data}")  # Mostrar los datos recibidos para depuración

                try:
                    data_list = data.split(',')

                    if len(data_list) == 23:  # Solo procesar si hay 23 valores
                        data_list = [float(value) for value in data_list]
                        print(f"Datos procesados: {data_list}")  # Mostrar los datos procesados para depuración

                        self.update_labels(data_list)

                        if self.is_recording:
                            self.recording_file.write(','.join(map(str, data_list)) + '\n')
                    else:
                        print(f"Error: Se esperaban 23 valores, pero se recibieron {len(data_list)}")
                except ValueError as e:
                    print(f"Error al procesar los datos: {e}, Datos recibidos: {data}")

            time.sleep(0.05)

    def create_graficar_button(self):
        """Crea un botón en la parte inferior central que ejecuta el script filtra_todo.py."""
        self.graficar_button = tk.Button(self.root, text="Graficar", command=self.run_filtra_todo)
        self.graficar_button.pack(pady=20, side=tk.BOTTOM)

    def run_filtra_todo(self):
        """Ejecuta el script filtra_todo.py."""
        try:
            os.system('python filtra_todo.py')
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar filtra_todo.py: {e}")
    
    def get_file_name(start_recording):
        """Método para obtener el nombre del archivo."""
        arch= start_recording
        return arch




