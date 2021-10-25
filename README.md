# Desarrollo de Sistemas - ONIET 2021
## BARRIOS POPULARES
!["Dashboard"](assets/images/auth/lockscreen-bg.jpg)
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
  
!["Dashboard"](assets/images/auth/lockscreen-bg.jpg)

### Barrios
Listado de todos los barrios. Se puede filtrar tanto por **Localidad** como por **Provincia**:
!["Dashboard"](assets/images/auth/lockscreen-bg.jpg)

### Barrio Seleccionado

En este apartado, se muestran los distintos accesos que tiene cada el barrio selecionado y además se pueden agregar paquetes de ayuda:
!["Dashboard"](assets/images/auth/lockscreen-bg.jpg)

### Localidades
Listado de todas las Localidades con la estadística de **`Paquetes por Persona`**:
!["Dashboard"](assets/images/auth/lockscreen-bg.jpg)

### Barrios Graves
Por último, se observan los **Barrios** que requieren una mayor **Cantidad de Paquetes**. Se puede elegir la cantidad que se desea mostrar:
!["Dashboard"](assets/images/auth/lockscreen-bg.jpg)