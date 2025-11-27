# 🏥 Sistema Distribuido de Gestión y Despacho de Emergencias Médicas
### Proyecto académico – Infraestructura de TI  
### Python + ZeroMQ + Tkinter + SQLite

---

## 📘 Descripción General

Este proyecto implementa un **sistema distribuido completo** que simula el proceso real de atención de emergencias médicas.  
Desde que un usuario reporta una emergencia, hasta que una ambulancia la acepta y el dashboard central registra el evento, todo funciona mediante **comunicación distribuida**, interfaces gráficas e intercambio de mensajes asíncronos usando ZeroMQ.

El sistema se divide en varios módulos independientes que se comunican entre sí mediante sockets ZMQ en diferentes puertos.

---

## 🧩 Componentes del Sistema

### 🔹 1. Usuario de Emergencias (`usuario_emergencia.py`)
Interfaz gráfica donde un ciudadano ingresa:
- Nombre  
- Dirección  
- Teléfono  
- Tipo de emergencia  

La información se envía al **Broker** mediante ZeroMQ.

---

### 🔹 2. Broker (`broker.py`)
Componente intermediario entre el usuario y el despachador.  
Sus funciones:
- Recibir emergencias del usuario  
- Validar el formato  
- Enviar la emergencia al **Dispatcher**  

---

### 🔹 3. Dispatcher (`dispatcher.py`)
Recibe emergencias desde el Broker y se encarga de:
- Enviar la emergencia a la ambulancia A1  
- Si A1 rechaza → enviar a A2  
- Si A2 rechaza → enviar a A3  
- Si A3 rechaza → enviar a A4  
- Si A4 rechaza → reiniciar ciclo  
- Cuando una ambulancia acepta, envía confirmación al Dashboard  

---

### 🔹 4. Ambulancias (`ambulancia.py`)
Módulo que representa **cuatro ambulancias (A1, A2, A3, A4)**.

Cuando llega una emergencia:
1. Aparece una ventana emergente:  
   _“¿Ambulancia A1 acepta la emergencia?”_
2. Si A1 rechaza → el Dispatcher envía a A2  
3. Si A2 rechaza → A3  
4. Si A3 rechaza → A4  
5. Si una acepta → se notifica al Dashboard  

---

### 🔹 5. Dashboard (`dashboard.py`)
Panel central del sistema que muestra una tabla con:
- Nombre del paciente  
- Dirección  
- Teléfono  
- Tipo de emergencia  
- Ambulancia asignada  

Recibe reportes desde las ambulancias y registra todo en la base de datos.

---

### 🔹 6. Base de Datos (`init_db.py`, `database.py`)
Implementación con SQLite3 para registrar:
- Emergencias  
- Ambulancias que las atienden  
- Historial completo  

---

### 🔹 7. Ejecutor Global (`run_all.py`)
Inicia automáticamente todos los módulos:
- Dashboard  
- Ambulancia  
- Dispatcher  
- Broker  
- Usuario  

Permite pruebas rápidas del sistema completo.

---

## 🔄 Flujo Completo del Sistema

```text
usuario_emergencia.py
        ↓
        Broker (6000)
        ↓
        Dispatcher (6001)
        ↓
ambulancia.py (6002)
        ↓
dashboard.py (6003)
