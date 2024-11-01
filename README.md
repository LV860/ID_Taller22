# ID_Taller22

### Integrantes del Equipo

1. Leonardo Velázquez Colin
2. María José Cárdenas Machaca
3. Oscar Rodríguez Gómez 
4. Pablo Escobar Gómez


# Guía de Instalación para el Entorno Virtual y MQTT

## Instalaciones para usar ambiente virtual

1. Actualiza los paquetes del sistema:
    ```bash
    sudo apt update
    ```
   
2. Instala el módulo para crear entornos virtuales de Python:
    ```bash
    sudo apt install python3-venv
    ```

## Crear el entorno virtual

1. Crea un nuevo entorno virtual llamado `mi_entorno`:
    ```bash
    python3 -m venv mi_entorno
    ```

## Activar el ambiente virtual

1. Activa el entorno virtual:
    ```bash
    source mi_entorno/bin/activate
    ```

## Instalar MQTT

1. Instala la biblioteca `paho-mqtt`:
    ```bash
    pip install paho-mqtt==1.5.1
    ```

## Instalar el broker de Mosquitto

1. Actualiza los paquetes del sistema nuevamente:
    ```bash
    sudo apt update
    ```

2. Instala Mosquitto y sus clientes:
    ```bash
    sudo apt-get install mosquitto mosquitto-clients
    ```

## Habilitar Mosquitto para acceso en línea

1. Edita el archivo de configuración de Mosquitto:
    ```bash
    sudo nano /etc/mosquitto/mosquitto.conf
    ```

2. Añade las siguientes líneas para habilitar el acceso remoto:
    ```
    listener 1883 0.0.0.0
    allow_anonymous true
    ```

## Habilitar Mosquitto

1. Habilita el servicio de Mosquitto para que se inicie automáticamente al arrancar:
    ```bash
    sudo systemctl enable mosquitto
    ```

2. Inicia el servicio de Mosquitto:
    ```bash
    sudo systemctl start mosquitto
    ```

3. Verifica el estado de Mosquitto:
    ```bash
    sudo systemctl status mosquitto
    ```

4. Visualiza los logs de Mosquitto:
    ```bash
    sudo tail -f /var/log/mosquitto/mosquitto.log
    ```

