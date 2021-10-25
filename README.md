# Desarrollo de Sistemas - ONIET 2021
## BARRIOS POPULARES
## Prueba del Sistema
1. Para empezar, descargue el repositorio o directamente clonarlo con git usando:
    ```text
    $ git clone https://github.com/lautipaletta/oniet2021.git
    ```
2. Luego, dentro del respositorio, ejecute el siguiente comando para instalar las librerías necesarias:
    ```text
    $ pip install -r requirements.txt
    ```
3. Y por último, para inicar el servidor en `http://localhost:8000`, use:
     ```text
     $ python manage.py runserver
     ```   
## Partes del Sistema

### Incio de Sesión
Se inicia sesión con las credenciales:
   - Usuario: **`admin`**
   - Contraseña: **`admin`**
  

### Barrios
Listado de todos los barrios. Se puede filtrar tanto por **Localidad** como por **Provincia**:

### Barrio Seleccionado

En este apartado, se muestran los distintos accesos que tiene cada el barrio selecionado y además se pueden agregar paquetes de ayuda:

### Localidades
Listado de todas las Localidades con la estadística de **`Paquetes por Persona`**:

### Barrios Graves
Por último, se observan los **Barrios** que requieren una mayor **Cantidad de Paquetes**. Se puede elegir la cantidad que se desea mostrar: