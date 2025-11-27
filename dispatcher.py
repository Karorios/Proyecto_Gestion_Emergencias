import zmq
import json
import time

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 6001    # Broker envía emergencias aquí

AMBULANCE_HOST = "127.0.0.1"
AMBULANCE_PORT = 6002  # Ambulancia escucha aquí

class Dispatcher:
    def __init__(self):
        ctx = zmq.Context()

        # Recibir del broker
        self.receiver = ctx.socket(zmq.PULL)
        self.receiver.bind(f"tcp://{BROKER_HOST}:{BROKER_PORT}")

        # Enviar a ambulancias
        self.sender = ctx.socket(zmq.PUSH)
        self.sender.connect(f"tcp://{AMBULANCE_HOST}:{AMBULANCE_PORT}")

    def start(self):
        print("🚨 Dispatcher esperando emergencias en 6001...")

        while True:
            emergency = self.receiver.recv_json()
            print(f"📥 Dispatcher recibió emergencia: {emergency}")

            # Enviar la emergencia a la primera ambulancia A1
            data = {
                "ambulancia": "A1",
                "emergencia": emergency
            }

            print("📤 Enviando emergencia a ambulancia A1...")
            self.sender.send_json(data)
            time.sleep(0.5)


if __name__ == "__main__":
    dispatcher = Dispatcher()
    dispatcher.start()
