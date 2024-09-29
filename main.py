#by astra
import tkinter as tk
from SerialConnection import SerialConnection
from GUI import DataDisplayGUI

if __name__ == "__main__":
    root = tk.Tk()
    serial_conn = SerialConnection()
    app = DataDisplayGUI(root, serial_conn)
    root.mainloop()


