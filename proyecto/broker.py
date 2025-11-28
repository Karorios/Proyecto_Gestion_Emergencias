# broker.py
import zmq
import json

def main():
    ctx = zmq.Context()

    # Recibir emergencias del usuario
    receiver = ctx.socket(zmq.PULL)
    receiver.bind("tcp://127.0.0.1:6000")
    print("🟢 BROKER escuchando emergencias del usuario en 6000...")

    # Enviar emergencias al dispatcher
    sender = ctx.socket(zmq.PUSH)
    sender.connect("tcp://127.0.0.1:6001")
    print("🟢 BROKER enviando emergencias a DISPATCHER en 6001...")

    while True:
        emergencia = receiver.recv_json()
        print(f"📥 Emergencia recibida en BROKER: {emergencia}")

        print("📤 Broker reenviando emergencia a DISPATCHER...")
        sender.send_json(emergencia)


if __name__ == "__main__":
    main()
