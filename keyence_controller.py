import socket
import time

# --- Configuración del Sensor ---
IP_LECTOR = "192.168.100.2"
# Según el manual, el puerto por defecto para comandos es 9004
PUERTO_LECTOR = 9004
TERMINADOR_COMANDO = "\r"  # Retorno de Carro (CR)

def enviar_comando(comando):
    """
    Se conecta al sensor, envía un comando y retorna la respuesta.
    Retorna None si la conexión falla.
    """
    try:
        # Creamos un nuevo socket para cada comando para simplificar
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Tiempo de espera (timeout) para conexión y lectura
            s.settimeout(3.0)
            
            print(f"Conectando a {IP_LECTOR}:{PUERTO_LECTOR}...")
            s.connect((IP_LECTOR, PUERTO_LECTOR))
            
            # Preparamos el comando con su terminador \r y lo codificamos
            comando_completo = (comando + TERMINADOR_COMANDO).encode('ascii')
            print(f"Enviando comando: {comando!r}")
            s.sendall(comando_completo)

            # Recibimos la respuesta del sensor
            datos_respuesta = b""
            while True:
                try:
                    # Leemos en bloques de 1024 bytes
                    pedazo = s.recv(1024)
                    if not pedazo:
                        break
                    datos_respuesta += pedazo
                    # Si encontramos el \r, ya tenemos la respuesta completa
                    if b"\r" in datos_respuesta:
                        break
                except socket.timeout:
                    break
            
            # Decodificamos y limpiamos espacios o saltos de línea
            respuesta = datos_respuesta.decode('ascii').strip()
            print(f"Respuesta recibida: {respuesta!r}")
            return respuesta

    except socket.timeout:
        print("Error: Tiempo de espera agotado (Timeout).")
        return None
    except ConnectionRefusedError:
        print(f"Error: Conexión rechazada en {IP_LECTOR}. Verifica la IP y la Subred.")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None

def detener_lector():
    """
    Envía el comando LOFF para asegurar que el láser se apague.
    """
    print("--- Deteniendo Lector ---")
    enviar_comando("LOFF")
    print("---")

def main():
    """
    Bucle principal para recibir órdenes del usuario.
    """
    print("--- Controlador de Lector Keyence ---")
    print("Comandos: 'ON' (Escanear), 'OFF' (Detener), 'EXIT' (Salir)")
    
    while True:
        try:
            entrada_usuario = input("Ingrese comando: ").strip().upper()

            if entrada_usuario == "ON":
                datos_escaneados = enviar_comando("LON")
                if datos_escaneados:
                    print(f">>> Datos recibidos: {datos_escaneados}")
                    # Al recibir datos, apagamos el lector automáticamente
                    detener_lector()
                else:
                    print("No se recibieron datos o hubo timeout.")
                    detener_lector()
            
            elif entrada_usuario == "OFF":
                detener_lector()

            elif entrada_usuario == "EXIT":
                print("Saliendo de la aplicación.")
                break
                
            else:
                print("Comando inválido. Use ON, OFF o EXIT.")

        except KeyboardInterrupt:
            print("\nCerrando aplicación por interrupción del usuario.")
            break

if __name__ == "__main__":
    main()
