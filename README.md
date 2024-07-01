# BookManager

BookManager es una aplicación web para gestionar información de libros utilizando MongoDB como base de datos y Django REST Framework (DRF) para proporcionar una API REST. Esta aplicación está dockerizada para facilitar su despliegue y ejecución.

## Requisitos

- Docker
- Docker Compose

## Configuración del Proyecto

### Clonar el Repositorio

Primero, clona el repositorio del proyecto:

```sh
git clone https://github.com/tu_usuario/bookmanager.git
cd bookmanager
```

## Configurar Variables de Entorno
Crea un archivo .env en el directorio raíz del proyecto con las siguientes variables de entorno:
```sh
MONGO_URI=mongodb://db:27017/
MONGO_DB_NAME=bookmanager
DJANGO_SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,
DEBUG=True
```

## Construir y Ejecutar la Aplicación
Usa Docker Compose para construir y ejecutar la aplicación:
```sh
docker-compose up --build

```
Ejecutar las pruebas unitarias para el módulo books
```sh
docker-compose exec web python manage.py test books
```
Una vez que los contenedores estén en ejecución, la API estará disponible en http://localhost:8000.
Se genera los datos de pruebas al ejecutarse el script ubicado books/scripts/initial_data.py

## Endpoints Disponibles
Se puede revisar la documentación en base a swagger en http://ec2-54-235-27-107.compute-1.amazonaws.com/swagger/
```sh
- Registro de Usuarios: POST /api/register/
- Inicio de Sesión: POST /api/login/
- Listar Libros: GET /api/books/
- Detalle de Libro: GET /api/books/{id}/
- Crear Libro: POST /api/books/
- Actualizar Libro: PUT /api/books/{id}/
- Eliminar Libro: DELETE /api/books/{id}/
- Precio Promedio por Año: GET /api/books/average-price/{year}/
```

## Uso de la API
Registrar un Nuevo Usuario
```sh
curl -X POST http://ec2-54-235-27-107.compute-1.amazonaws.com/api/register/ \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpassword"}'
```

Obtener Token de Autenticación
```sh
curl -X POST http://ec2-54-235-27-107.compute-1.amazonaws.com/api/login/ \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "testpassword"}'
```

Usar el Token para Autenticar Solicitudes
```sh
curl -X GET http://localhost:8000/api/books/ \
-H "Authorization: Token your_token_here"
```

## Pruebas Unitarias
```sh
docker-compose exec web python manage.py test books
```
