# 📲 News Bot API

API REST para la gestión de usuarios y suscripciones a categorías de noticias. Desarrollada con **Flask**, protegida con **JWT** y documentada con **Swagger (OpenAPI 3.0.3)**.

---

## 🚀 Tecnologías utilizadas

- **Flask**
- **Flask-JWT-Extended**
- **Marshmallow** para validaciones
- **Flasgger** para documentación Swagger
- **Blueprints** para modularidad
- **Servicios** y manejo de errores custom

---

## 🔐 Autenticación

Todas las rutas (excepto `register`, `login` y `categories`) requieren un JWT válido. El token debe enviarse en el header `Authorization` como:

```
Bearer <token>
```

---

## 📚 Endpoints disponibles

### 🟦 Auth

#### `POST /register`

Registrar nuevo usuario.

- Body:

```json
{
  "phone_number": "+549123456789",
  "password": "SecurePass123"
}
```

- Respuesta: `201 Created`\
  Devuelve `access_token` y datos del usuario.

---

#### `POST /login`

Iniciar sesión.

- Body:

```json
{
  "phone_number": "+549123456789",
  "password": "SecurePass123"
}
```

- Respuesta: `200 OK`\
  Devuelve `access_token` y datos del usuario.

---

### 🟧 Suscripciones

Todas las rutas siguientes requieren autenticación con JWT.

#### `GET /subscriptions/categories`

Obtener las categorías válidas para suscribirse.

- Respuesta:

```json
{
  "categories": ["cultura", "deportes", "economía", "tecnología"]
}
```

---

#### `POST /subscriptions`

Crear nuevas suscripciones.

- Body:

```json
{
  "categories": ["deportes", "tecnología"]
}
```

- Respuesta: `201 Created`\
  Devuelve la lista de suscripciones creadas.

---

#### `GET /subscriptions`

Obtener suscripciones del usuario actual.

- Respuesta:

```json
[
  {"category": "deportes"},
  {"category": "tecnología"}
]
```

---

#### `PUT /subscriptions`

Reemplazar todas las suscripciones del usuario actual.

- Body:

```json
{
  "categories": ["economía"]
}
```

- Respuesta: `200 OK`\
  Devuelve la nueva lista de suscripciones.

---

#### `DELETE /subscriptions/<category>`

Eliminar una suscripción por categoría.

- Ejemplo: `DELETE /subscriptions/deportes`
- Respuesta:

```json
{
  "message": "Suscripción eliminada exitosamente",
  "category": "deportes"
}
```

---

## 📄 Documentación Swagger

La documentación interactiva está disponible en:

```
/swagger/
```

---

## ✅ Validaciones

Las categorías válidas para suscripción son:

- `deportes`
- `tecnología`
- `economía`
- `cultura`

Si se envían categorías inválidas, se devuelve un error con estado `400`.

---

## 📁 Estructura recomendada

```
app/
├── auth/
│   ├── routes.py
│   ├── services.py
│   └── schemas.py
├── services/
│   └── subscription.py
├── schemas/
│   ├── subscription_schema.py
│   └── swagger_definitions.py
├── errors/
│   └── exceptions.py
├── routes/
│   ├── auth_routes.py
│   └── subscription_routes.py
main.py
README.md
```

---

## 🛠️ Setup rápido

1. Crear entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar el servidor:

```bash
flask run
```

---

## ✨ Ejemplo de uso con curl

```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+549123456789", "password": "test12345"}'
```

---

## 🔪 Tests

✅ Tests implementados con `pytest`.

Para correr los tests:

```bash
pytest
```

---

## 📬 Contacto

Este proyecto es parte de una práctica de backend con Flask y JWT.\
Hecho con 💻 y ☕ por fom78.

