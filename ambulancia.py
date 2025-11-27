import tkinter as tk
from tkinter import messagebox
import zmq
import json
import threading
import time

DISPATCHER_HOST = "127.0.0.1"
DISPATCHER_PORT = 6002

DASHBOARD_HOST = "127.0.0.1"
DASHBOARD_PORT = 6003


class AmbulanceSystem:
    def __init__(self):
        context = zmq.Context()

        # Recibir del Dispatcher
        self.receiver = context.socket(zmq.PULL)
        self.receiver.bind(f"tcp://{DISPATCHER_HOST}:{DISPATCHER_PORT}")

        # Enviar al Dashboard
        self.sender = context.socket(zmq.PUSH)
        self.sender.connect(f"tcp://{DASHBOARD_HOST}:{DASHBOARD_PORT}")

        self.ambulances = ["A1", "A2", "A3", "A4"]
        self.current_index = 0

    def start(self):
        print("🚑 Ambulancias en espera de emergencias (6002)...")
        while True:
            data = self.receiver.recv_json()
            print("📥 Emergencia recibida del Dispatcher:")
            print(data)

            self.current_index = 0
            self.try_assign_ambulance(data)

    def try_assign_ambulance(self, emergency_data):
        if self.current_index >= len(self.ambulances):
            print("❌ Ninguna ambulancia aceptó. Reiniciando ciclo...")
            self.current_index = 0

        ambulance_name = self.ambulances[self.current_index]
        print(f"🚑 Intentando con ambulancia {ambulance_name}")

        self.show_popup(ambulance_name, emergency_data)

    def show_popup(self, ambulance_name, emergency_data):
        def response(result):
            popup.destroy()

            if result == "yes":
                print(f"✅ {ambulance_name} aceptó la emergencia")

                # Enviar al dashboard → CLAVE CORREGIDA
                data = {
                    "ambulancia": ambulance_name,
                    "emergency": emergency_data
                }
                self.sender.send_json(data)
                print("📤 Enviado al Dashboard")

            else:
                print(f"❌ {ambulance_name} rechazó la emergencia")
                self.current_index += 1
                self.try_assign_ambulance(emergency_data)

        popup = tk.Tk()
        popup.title(f"Ambulancia {ambulance_name}")

        tk.Label(
            popup,
            text=f"🚨 Emergencia recibida\n¿Ambulancia {ambulance_name} acepta?",
            font=("Arial", 12)
        ).pack(pady=10)

        tk.Button(popup, text="SI", width=10,
                  command=lambda: response("yes")).pack(pady=5)

        tk.Button(popup, text="NO", width=10,
                  command=lambda: response("no")).pack(pady=5)

        popup.mainloop()


def start_ambulance_system():
    system = AmbulanceSystem()
    system.start()


if __name__ == "__main__":
    start_ambulance_system()
