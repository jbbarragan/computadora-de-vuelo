# AUTHOR: ASTRA CLUB
# DATE: 2024
# FILE: COMPUTADORA DE VUELO/GUI.py
# Params: main.py, SerialConnection
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
       

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        self.connection_frame = tk.Frame(self.frame)
        self.connection_frame.grid(row=0, column=0, sticky="nw")

        self.connection_status = tk.Label(self.connection_frame, text="Estado: Desconectado", width=30, fg="red")
        self.connection_status.pack(pady=10)

        self.combobox = ttk.Combobox(self.connection_frame, values=self.serial_conn.list_ports())
        self.combobox.pack(padx=5, pady=5)
        self.combobox.set("Selecciona un puerto COM")
        self.combobox.bind("<<ComboboxSelected>>", self.enable_connect_button)

      
        self.connect_button = tk.Button(self.connection_frame, text="Conectar", command=self.connect_serial, state=tk.DISABLED)
        self.connect_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.disconnect_button = tk.Button(self.connection_frame, text="Desconectar", command=self.disconnect_serial, state=tk.DISABLED)
        self.disconnect_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.recording_frame = tk.Frame(self.frame)
        self.recording_frame.grid(row=0, column=1, sticky="ne")


        self.file_label = tk.Label(self.recording_frame, text="Guardado en Telemetria_muestra.txt")
        self.file_label.pack(padx=5, pady=5)
      
        self.start_button = tk.Button(self.recording_frame, text="Start Recording", command=self.start_recording, state=tk.DISABLED)
        self.start_button.pack(padx=5, pady=5)

        self.stop_button = tk.Button(self.recording_frame, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(padx=5, pady=5)

        self.create_data_labels()


        self.create_min_max_labels()

    
        self.create_graficar_button()  

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
        file_name = "Telemetria_muestra.txt"
        

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


        self.data_frames = tk.Frame(self.root)
        self.data_frames.pack(padx=10, pady=10)


        self.velocidad_frame = tk.LabelFrame(self.data_frames, text="Velocidad", padx=10, pady=10)
        self.velocidad_frame.grid(row=0, column=0, padx=5, pady=5)
        self.velocidad_labels = {}
        for axis in ['X', 'Y', 'Z']:
            label = tk.Label(self.velocidad_frame, text=f"aceleracion lineal {axis}: ---")
            label.pack(anchor="w")
            self.velocidad_labels[f"aceleracion lineal {axis}"] = label


        self.aceleracion_frame = tk.LabelFrame(self.data_frames, text="Aceleraciones", padx=10, pady=10)
        self.aceleracion_frame.grid(row=0, column=1, padx=5, pady=5)
        self.aceleracion_labels = {}
        for axis in ['X', 'Y', 'Z']:
            label = tk.Label(self.aceleracion_frame, text=f"acelerometro {axis}: ---")
            label.pack(anchor="w")
            self.aceleracion_labels[f"acelerometro {axis}"] = label


        self.gravedad_frame = tk.LabelFrame(self.data_frames, text="Gravedades", padx=10, pady=10)
        self.gravedad_frame.grid(row=0, column=2, padx=5, pady=5)
        self.gravedad_labels = {}
        for axis in ['X', 'Y', 'Z']:
            label = tk.Label(self.gravedad_frame, text=f"gravedad {axis}: ---")
            label.pack(anchor="w")
            self.gravedad_labels[f"gravedad {axis}"] = label

   
        self.giroscopio_frame = tk.LabelFrame(self.data_frames, text="Giroscopio", padx=10, pady=10)
        self.giroscopio_frame.grid(row=0, column=3, padx=5, pady=5)
        self.giroscopio_labels = {}
        for axis in ['X', 'Y', 'Z']:
            label = tk.Label(self.giroscopio_frame, text=f"giroscopio {axis}: ---")
            label.pack(anchor="w")
            self.giroscopio_labels[f"giroscopio {axis}"] = label

 
        self.ambiental_frame = tk.LabelFrame(self.data_frames, text="Condiciones Ambientales", padx=10, pady=10)
        self.ambiental_frame.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky="ew")
        self.ambiental_labels = {}
        for field in ["temperatura", "presion", "temperatura", "humedad"]:
            label = tk.Label(self.ambiental_frame, text=f"{field}: ---")
            label.pack(anchor="w")
            self.ambiental_labels[field] = label

   
        self.orientacion_frame = tk.LabelFrame(self.data_frames, text="Orientación", padx=10, pady=10)
        self.orientacion_frame.grid(row=1, column=3, padx=5, pady=5, columnspan=2, sticky="ew")
        self.orientacion_labels = {}
        for field in ["yaw", "pitch", "heading", "roll"]:
            label = tk.Label(self.orientacion_frame, text=f"{field}: ---")
            label.pack(anchor="w")
            self.orientacion_labels[field] = label


        self.labels = {**self.velocidad_labels, **self.aceleracion_labels, **self.gravedad_labels,
                       **self.giroscopio_labels, **self.ambiental_labels,
                       **self.orientacion_labels}

    def create_min_max_labels(self):
        """Crea las etiquetas para mostrar las temperaturas y presiones máximas y mínimas."""
        self.max_labels = {}
        self.min_labels = {}

       
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


        data_list = [float(value) for value in data_list]

        for i, value in enumerate(data_list):
            if i < len(keys):
                self.labels[keys[i]].config(text=f"{keys[i]}: {value}")

       
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
                print(f"Datos recibidos: {data}")  

                try:
                    data_list = data.split(',')

                    if len(data_list) == 23:  
                        data_list = [float(value) for value in data_list]
                        print(f"Datos procesados: {data_list}")  

                        self.update_labels(data_list)

                        if self.is_recording:
                            self.recording_file.write(','.join(map(str, data_list)) + '\n')
                    
                except ValueError as e:
                    print(f"Datos recibidos: {data}")

            time.sleep(0.05)

    def create_graficar_button(self):
        """Crea botones en la parte inferior para Graficar y Procesar Archivo."""
        # Frame contenedor para los botones
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20, side=tk.BOTTOM)
    
        # Botón Graficar
        self.graficar_button = tk.Button(self.button_frame, text="Graficar", command=self.run_filtra_todo)
        self.graficar_button.pack(side=tk.LEFT, padx=10)
    
        # Botón Procesar Archivo
        self.procesar_button = tk.Button(self.button_frame, text="Procesar Archivo", command=self.run_filtra_sd)
        self.procesar_button.pack(side=tk.LEFT, padx=10)
    
    def run_filtra_sd(self):
     """Ejecuta el script filtra_sd.py."""
     try:
      os.system('python filtra_sd.py')
     except Exception as e:
      messagebox.showerror("Error", f"Error al ejecutar filtra_sd.py: {e}")

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




