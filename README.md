# Control de Lector Keyence SR-X (Python)

Este proyecto proporciona una interfaz sencilla en Python para controlar lectores de códigos de barras Keyence de la serie SR-X a través de una conexión TCP/IP.

## Requisitos de Red
Para que el programa funcione, tu computadora y el lector deben estar en la misma subred:
*   **IP del Lector:** `192.168.100.2` (asignada)
*   **Submáscara:** `255.255.255.0`
*   **Puerto de Comando:** `9004`
*   **IP de la PC Sugerida:** `192.168.100.10`

## Funcionamiento Técnico
El script utiliza el protocolo de comunicación por comandos de Keyence. Cada comando debe terminar con un carácter de retorno de carro (`\r` o CR).

### Comandos Implementados:
- **LON:** Enciende el láser y comienza la lectura.
- **LOFF:** Detiene la lectura y apaga el láser.

## Estructura del Código
1. **Conexión:** Se abre un socket TCP en cada comando para asegurar que no haya bloqueos de red.
2. **Envío:** El comando se codifica en formato ASCII y se le añade el terminador `\r`.
3. **Recepción:** El programa espera una respuesta del sensor. Si se lee un código, el sensor devuelve el texto del código seguido de un `\r`.
4. **Cierre Automático:** Por seguridad, después de cada lectura exitosa o intento fallido, el programa envía un `LOFF` para evitar que el láser se quede encendido innecesariamente.

## Cómo Usar
1. Ejecuta `python keyence_controller.py`.
2. Escribe `ON` para leer un código.
3. Escribe `OFF` para forzar el apagado.
4. Escribe `EXIT` para cerrar el programa.
