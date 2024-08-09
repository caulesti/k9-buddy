# K9-Buddy
K9-Buddy es un robot cuadrúpedo de código abierto diseñado para fomentar la educación en STEAM y proporcionar una base sólida para competir en eventos de robótica. Destacándose por su bajo costo, K9-Buddy es accesible tanto para estudiantes como para entusiastas de la robótica. 
<p align="center">
  <img src="images/1.png" alt="K9-Buddy" width="500"/>
</p>

### Configuración del entorno
1. Actualizar el Sistema
Abre una terminal y ejecuta los siguientes comandos para actualizar la lista de paquetes y actualizar los paquetes instalados a sus versiones más recientes:
```
sudo apt-get update
sudo apt-get upgrade
```
2. Instalar Python y Pip: 
```
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
```
3. Instalar Paquetes Adicionales:
```
# Instalar python-smbus y i2c-tools
sudo apt-get install -y python3-smbus
sudo apt-get install -y i2c-tools

# Verificar la conexión I2C
sudo i2cdetect -y 1

# Instalar Adafruit CircuitPython ServoKit
sudo pip3 install adafruit-circuitpython-servokit
```

### Uso
1. Clonación del Repositorio
```
git clone https://github.com/caulesti/k9-buddy.git
```
2. Otorgar permisos al script
```
chmod +x k9-buddy/software/k9_buddy.py
```
3. Ejecución
```
python3 k9-buddy/software/k9_buddy.py
```





















