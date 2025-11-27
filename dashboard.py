
import tkinter as tk
from tkinter import ttk
import zmq
import threading
from database import guardar_reporte



class DashboardApp:
    def __init__(self):
        self.ctx = zmq.Context()

        # recibir reportes de ambulancias
        self.receiver = self.ctx.socket(zmq.PULL)
        self.receiver.bind("tcp://127.0.0.1:6003")

        self.root = tk.Tk()
        self.root.title("Dashboard - Emergencias")
        self.root.geometry("900x400")

        title = tk.Label(self.root, text="📊 Dashboard de Emergencias", font=("Arial", 18))
        title.pack(pady=10)

        columns = ("nombre", "direccion", "telefono", "emergencia", "ambulancia")

        self.table = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        self.table.pack(fill="both", expand=True)

        self.table.heading("nombre", text="Nombre")
        self.table.heading("direccion", text="Dirección")
        self.table.heading("telefono", text="Teléfono")
        self.table.heading("emergencia", text="Emergencia")
        self.table.heading("ambulancia", text="Ambulancia Asignada")

        for col in columns:
            self.table.column(col, width=150)

        threading.Thread(target=self.listen_updates, daemon=True).start()

    def listen_updates(self):
        print("📡 Dashboard escuchando reportes en 6003...")
        while True:
            reporte = self.receiver.recv_json()
            print("📥 Reporte recibido:", reporte)
            self.root.after(0, lambda r=reporte: self.add_report(r))

    def add_report(self, reporte):
        emergency = reporte["emergency"]["emergencia"]
        ambulancia = reporte["ambulancia"]

        # Insertar en la tabla visual
        self.table.insert("", "end", values=(
            emergency["nombre"],
            emergency["direccion"],
            emergency["telefono"],
            emergency["emergencia"],
            ambulancia
        ))

        guardar_reporte(emergency, ambulancia)

        print("📌 Reporte agregado y guardado en la base de datos.")


if __name__ == "__main__":
    DashboardApp().root.mainloop()
