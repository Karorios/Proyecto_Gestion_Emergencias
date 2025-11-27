# run_all.py
import subprocess
import time

def run(title, command):
    subprocess.Popen(
        ["start", "cmd", "/k", command],
        shell=True
    )
    print(f"✔ Lanzado: {title}")
    time.sleep(1)


print("🚀 INICIANDO SISTEMA DE EMERGENCIAS...\n")

# 1. Inicializar base de datos
run("Base de datos", "python init_db.py")

# 2. Broker
run("Broker", "python broker.py")

# 3. Dispatcher
run("Dispatcher", "python dispatcher.py")

# 4. Ambulancias
run("Ambulancias", "python ambulancia.py")

# 5. Dashboard
run("Dashboard", "python dashboard.py")

# 6. Usuario (opcional)
run("Usuario Emergencia", "python usuario_emergencia.py")

print("\n🟢 Todo el sistema está corriendo!")
