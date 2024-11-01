import argparse
import random
import time
import paho.mqtt.client as mqtt
import threading
import zmq  # ZeroMQ para obtener nuevos brokers

class Sensor_Humedad:
    def __init__(self, id,humedad_inicial):
        
        self.id = id
        self.humedad_actual = humedad_inicial
        self.humedad_inicial = humedad_inicial
        
        # Lista de brokers
        self.brokers = [
            ("10.43.101.203", 1883)
        ]
        self.current_broker_index = 0  # Índice para el broker actual

        # Inicializa el cliente MQTT
        self.client = mqtt.Client()
        # Asignar funciones de evento
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        #self.client.on_message = self.on_message

        # Conectar al broker actual
        self.conectar_broker()
        self.registrar()
        
        self.hilo_movimiento = threading.Thread(target=self.inicio)
        self.hilo_movimiento.start()

    def conectar_broker(self):
        # Intentar conectar con cada broker en la lista
        while self.current_broker_index < len(self.brokers):
            broker, port = self.brokers[self.current_broker_index]
            try:
                print(f"Sensor_Humedad {self.id}: Intentando conectar al broker {broker}:{port}...")
                self.client.connect(broker, port, 60)
                
                break  # Si la conexión es exitosa, salir del bucle
            except Exception as e:
                print(f"Error conectando al broker {broker}:{port}: {e}")
                self.current_broker_index += 1  # Intentar con el siguiente broker

        if self.current_broker_index >= len(self.brokers):
            self.current_broker_index = 0  # Reiniciar índice para intentar nuevamente con la lista


    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Sensor_Humedad {self.id}: Conectado exitosamente al broker MQTT")
        else:
            print(f"Sensor_Humedad {self.id}: Error al conectarse, código {rc}")

    def on_disconnect(self, client, userdata, rc):
        print(f"Sensor_Humedad {self.id}: Desconectado del broker MQTT")
        if rc != 0:
            print("Intentando reconectar al broker MQTT...")
            self.current_broker_index += 1  # Avanzar al siguiente broker
            self.conectar_broker()  # Intentar la conexión al siguiente broker

    def registrar(self):
        mensaje = f"Sensor_Humedad: {self.id}, Humedad Inicial: {self.humedad_inicial}"
        topic = "sensor/registro/humedad"
        print("Sensor humedad registrado:", mensaje)
        self.client.publish(topic, mensaje)
        time.sleep(5)

    def cambio_hum(self):
        nueva_humedad = random.randint(0, 100)
        self.humedad_actual =  str(nueva_humedad) + "%"
        
       

    def inicio(self):
        while True:
            self.cambio_hum()
            self.enviar_hum()
            self.mostrar_nueva_hum()
            time.sleep(5)  # Esperar 30 segundos antes de mover nuevamente

    def enviar_hum(self):
        posicion = f"Sensor_Humedad: {self.id}, Humedad {self.humedad_actual}"
        topic = "sensor/actualizacion/humedad"
        self.client.publish(topic, posicion) # Publica su nueva posicion por el tópico correspondiente
    
    def mostrar_nueva_hum(self):
        print(f"Sensor Humedad {self.id}: Nueva Humedad {self.humedad_actual}")

    

def main():
    parser = argparse.ArgumentParser(description='Inicializar un sensor')
    parser.add_argument('id', type=int, help='Número entero positivo que identifica al sensor')
    parser.add_argument('humedad_inicial', type=int, help='Número que representa la humedad inicial')
    

    args = parser.parse_args()
    sensor = validar_argumentos(args) # Se validan los argumentos de ejecución del taxi
    
def validar_argumentos(args):
    try:
        return Sensor_Humedad(args.id, args.humedad_inicial)
    except ValueError:
        print("Error: Algunos de los argumentos proporcionados no son válidos.")
        exit()

if __name__ == "__main__":
    main()
