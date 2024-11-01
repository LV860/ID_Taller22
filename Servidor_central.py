import paho.mqtt.client as mqtt
import time
import threading

import signal
import sys
 

class ServidorCentral:
    def __init__(self):
        self.sensor_temp = {}
        self.sensor_hum = {}
       
        self.broker_list = ["10.43.101.203:1883"]
        self.broker_index = 0  # Indice del broker actual
        self.client = mqtt.Client("ServidorCentral")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        self.conectar_a_broker()  # Se conecta al primer broker

        # Captura de señal de interrupción (Ctrl+C)
        signal.signal(signal.SIGINT, self.handle_exit)

        threading.Thread(target=self.loop_mqtt, daemon=True).start()

    def conectar_a_broker(self):
        
        while self.broker_index < len(self.broker_list):
            broker_address = self.broker_list[self.broker_index]
            try:
                print(f"Intentando conectar al broker: {broker_address}")
                self.client.connect(broker_address.split(":")[0], int(broker_address.split(":")[1]))  # Se inetenta conectar con el broker actual en la lista
                return  # Conexión exitosa, sale del bucle
            except Exception as e:
                print(f"Error al conectar al broker {broker_address}: {e}")
                self.broker_index += 1  # Se cmabia al siguiente broker

        # Si todos los brokers fallan, intenta obtener uno nuevo del healthchecker
        print("Todos los brokers fallaron. Solicitando un nuevo broker al HealthChecker...")
        

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Servidor conectado al broker con éxito.")
            #client.subscribe("sensor/#")
            client.subscribe("sensor/registro/temperatura")
            client.subscribe("sensor/registro/humedad")
            client.subscribe("sensor/actualizacion/temperatura")
            client.subscribe("sensor/actualizacion/humedad")
        else:
            print(f"Error al conectar con el broker. Código de retorno: {rc}")
            self.reintentar_conexion()

    def on_disconnect(self, client, userdata, rc):
        print(f"Desconectado del broker. Código de retorno: {rc}")
        if rc != 0:  # Si no fue una desconexión intencionada
            self.broker_index += 1  # Cambia al siguiente broker en la lista
            self.reintentar_conexion()

    def reintentar_conexion(self):
        """ Intenta reconectar al siguiente broker en la lista """
        if self.broker_index < len(self.broker_list):
            print("Intentando reconectar al siguiente broker...")
            self.conectar_a_broker() # Se conecta
        else:
            print("No hay más brokers disponibles en la lista. Solicitando al HealthChecker.")
            self.obtener_nuevo_broker()

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode("utf-8")

        if topic == "sensor/registro/temperatura":
            self.registrar_sensorTemp(payload)
        elif topic == "sensor/registro/humedad":
            self.registrar_sensorHum(payload)
        elif topic == "sensor/actualizacion/temperatura":
            self.act_sensorTemp(payload)
        elif topic == "sensor/actualizacion/humedad":
            self.act_sensorHum(payload)
        

          

    def registrar_sensorTemp(self, mensaje):
        sensor_part, temp_inicial = mensaje.split(", Temperatura Inicial: ")
        sensor_id = sensor_part.split(":")[1].strip()
        
        print(f"Se ha registrado el sensor de temperatura con ID {sensor_id} con medida :{temp_inicial}")
        self.sensor_temp[sensor_id] = [temp_inicial]

        

    def act_sensorTemp(self, mensaje):
        try:
            sensor_id, temp= mensaje.split(", Temperatura ")
            sensor_id = sensor_id.split(":")[1].strip()
            
            if sensor_id in self.sensor_temp:
                self.sensor_temp[sensor_id] = temp
                
                print(f"Sensor ID {sensor_id} actualizado con la temperatura: {temp}")
                
            else:
                print(f"Sensor ID {sensor_id} no encontrado.")
        except ValueError as e:
            print(f"Ocurrió un error al procesar el mensaje: {e}")
    
    def registrar_sensorHum(self, mensaje):
        
        sensor_id, hum_inicial = mensaje.split(", Humedad Inicial: ")
        sensor_id = sensor_id.split(":")[1].strip()
        print(f"Se ha registrado el sensor de humedad con ID {sensor_id} con medida ({hum_inicial})")
        self.sensor_hum[sensor_id] = [hum_inicial]
        

    def act_sensorHum(self, mensaje):
        try:
            sensor_id, hum= mensaje.split(", Humedad ")
            sensor_id = sensor_id.split(":")[1].strip()
            
            if sensor_id in self.sensor_hum:
                self.sensor_hum[sensor_id] = hum
                
                print(f"Sensor ID {sensor_id} actualizado con la humedad: {hum}")
                
            else:
                print(f"Sensor ID {sensor_id} no encontrado.")
        except ValueError as e:
            print(f"Ocurrió un error al procesar el mensaje: {e}")

    
    

    
    def loop_mqtt(self):
        """Bucle principal del cliente MQTT"""
        try:
            self.client.loop_forever()
        except Exception as e:
            print(f"Error en el loop MQTT: {e}")
            self.reintentar_conexion()


    def handle_exit(self, sig, frame):
        """ Manejo de señal de salida como Ctrl+C """
        print("Interrupción detectada, desconectando del broker...")
        self.client.disconnect() 
        sys.exit(0)  
        

def main():
    servidor = ServidorCentral()
    while True:
        time.sleep(150)  

if __name__ == "__main__":
    main()
