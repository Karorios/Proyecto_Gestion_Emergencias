import tkinter as tk
from tkinter import messagebox
import zmq
import json

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 6000   # ← ← ESTE ES EL PUERTO CORRECTO


class UserEmergencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚨 Registro de Emergencia - Usuario")

        # Configurar ZeroMQ (envío PUSH)
        context = zmq.Context()
        self.sender = context.socket(zmq.PUSH)
        self.sender.connect(f"tcp://{BROKER_HOST}:{BROKER_PORT}")

        # ---- UI en Español ----
        tk.Label(root, text="Nombre Completo:").grid(row=0, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        tk.Label(root, text="Dirección:").grid(row=1, column=0)
        self.address_entry = tk.Entry(root)
        self.address_entry.grid(row=1, column=1)

        tk.Label(root, text="Número de Teléfono:").grid(row=2, column=0)
        self.phone_entry = tk.Entry(root)
        self.phone_entry.grid(row=2, column=1)

        tk.Label(root, text="Descripción de la Emergencia:").grid(row=3, column=0)
        self.emergency_entry = tk.Entry(root)
        self.emergency_entry.grid(row=3, column=1)

        tk.Button(root, text="🚨 Enviar Emergencia", command=self.send_emergency).grid(
            row=4, column=0, columnspan=2
        )

    def send_emergency(self):
        data = {
            "nombre": self.name_entry.get(),
            "direccion": self.address_entry.get(),
            "telefono": self.phone_entry.get(),
            "emergencia": self.emergency_entry.get(),
        }

        # Validación
        if not all(data.values()):
            messagebox.showwarning("Campos incompletos", "Por favor llene todos los campos.")
            return

        # Serializar y enviar
        self.sender.send_json(data)

        messagebox.showinfo("Enviado", "La emergencia ha sido enviada exitosamente.")

        # Limpiar campos
        self.name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.emergency_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = UserEmergencyApp(root)
    root.mainloop()
