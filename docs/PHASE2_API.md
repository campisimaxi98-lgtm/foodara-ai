# 📡 FOODARA AI - PHASE 2 API

## Autenticación

### Register - Usuario Simple

**Endpoint:** `POST /api/v1/auth/register`

Registra un nuevo usuario con preferencias por defecto.

**Request:**
```json
{
  "email": "usuario@foodara.ar",
  "username": "username123",
  "password": "SecurePass123!",
  "first_name": "Juan",
  "last_name": "Pérez"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Validaciones:**
- Email válido
- Username único
- Password fuerte (≥8 chars, mayúscula, número, símbolo)

---

### Register - Con Preferencias

**Endpoint:** `POST /api/v1/auth/register-full`

Registra usuario configurando preferencias desde el inicio.

**Request:**
```json
{
  "email": "usuario@foodara.ar",
  "username": "username123",
  "password": "SecurePass123!",
  "first_name": "Juan",
  "last_name": "Pérez",
  "preferences": {
    "currency": "ARS",
    "language": "es",
    "timezone": "America/Argentina/Buenos_Aires",
    "preferred_budget_ars": 75000,
    "people_at_home": 4,
    "cooking_time_available_minutes": 45,
    "vegetarian": false,
    "vegan": false,
    "gluten_free": false,
    "dairy_free": false
  }
}
```

**Response (200):**
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

---

### Login

**Endpoint:** `POST /api/v1/auth/login`

Autentica usuario y devuelve tokens.

**Request:**
```json
{
  "email": "usuario@foodara.ar",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Errores:**
- `401`: Credenciales inválidas
- `403`: Usuario desactivado

---

## Gestión de Usuarios

### Obtener Perfil Actual

**Endpoint:** `GET /api/v1/users/me`

Obtiene datos del usuario autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "email": "usuario@foodara.ar",
  "username": "username123",
  "first_name": "Juan",
  "last_name": "Pérez",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

---

### Obtener Perfil Completo

**Endpoint:** `GET /api/v1/users/me/profile`

Obtiene usuario + preferencias en una sola consulta.

**Response (200):**
```json
{
  "id": 1,
  "email": "usuario@foodara.ar",
  "username": "username123",
  "first_name": "Juan",
  "last_name": "Pérez",
  "is_active": true,
  "preferences": {
    "id": 1,
    "user_id": 1,
    "currency": "ARS",
    "language": "es",
    "timezone": "America/Argentina/Buenos_Aires",
    "preferred_budget_ars": 75000,
    "people_at_home": 4,
    "cooking_time_available_minutes": 45,
    "vegetarian": false,
    "vegan": false,
    "gluten_free": false,
    "dairy_free": false,
    "email_notifications": true,
    "waste_alerts": true,
    "budget_alerts": true
  }
}
```

---

### Actualizar Perfil

**Endpoint:** `PATCH /api/v1/users/me`

Actualiza información del usuario.

**Request (campos opcionales):**
```json
{
  "first_name": "Juan Carlos",
  "last_name": "Pérez García",
  "email": "nuevo@foodara.ar"
}
```

**Response (200):**
```json
{
  "id": 1,
  "email": "nuevo@foodara.ar",
  "username": "username123",
  "first_name": "Juan Carlos",
  "last_name": "Pérez García",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:35:00"
}
```

---

### Desactivar Cuenta

**Endpoint:** `POST /api/v1/users/me/deactivate`

Desactiva la cuenta de forma reversible.

**Response (200):**
```json
{
  "message": "Cuenta desactivada"
}
```

---

### Activar Cuenta

**Endpoint:** `POST /api/v1/users/me/activate`

Activa una cuenta desactivada.

**Response (200):**
```json
{
  "message": "Cuenta activada"
}
```

---

### Eliminar Cuenta

**Endpoint:** `DELETE /api/v1/users/me`

⚠️ **ACCIÓN IRREVERSIBLE** - Elimina permanentemente la cuenta y todos sus datos.

**Response (200):**
```json
{
  "message": "Cuenta eliminada"
}
```

---

## Preferencias

### Obtener Preferencias

**Endpoint:** `GET /api/v1/users/me/preferences`

Obtiene preferencias del usuario autenticado.

**Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "currency": "ARS",
  "language": "es",
  "timezone": "America/Argentina/Buenos_Aires",
  "preferred_budget_ars": 75000,
  "people_at_home": 4,
  "cooking_time_available_minutes": 45,
  "vegetarian": false,
  "vegan": false,
  "gluten_free": false,
  "dairy_free": false,
  "email_notifications": true,
  "waste_alerts": true,
  "budget_alerts": true
}
```

---

### Actualizar Preferencias

**Endpoint:** `PATCH /api/v1/users/me/preferences`

Actualiza preferencias del usuario (todos los campos son opcionales).

**Request:**
```json
{
  "preferred_budget_ars": 100000,
  "people_at_home": 5,
  "cooking_time_available_minutes": 60,
  "vegetarian": true,
  "email_notifications": false,
  "waste_alerts": true,
  "budget_alerts": true
}
```

**Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "currency": "ARS",
  "language": "es",
  "timezone": "America/Argentina/Buenos_Aires",
  "preferred_budget_ars": 100000,
  "people_at_home": 5,
  "cooking_time_available_minutes": 60,
  "vegetarian": true,
  "vegan": false,
  "gluten_free": false,
  "dairy_free": false,
  "email_notifications": false,
  "waste_alerts": true,
  "budget_alerts": true
}
```

---

## Validaciones

### Presupuesto
- Mínimo: 0
- Máximo: Ilimitado (recomendado ≤ 500.000 ARS)

### Cantidad de Personas
- Mínimo: 1
- Máximo: 20

### Tiempo de Cocina
- Mínimo: 5 minutos
- Máximo: 480 minutos (8 horas)

### Contraseña
- Mínimo: 8 caracteres
- Debe tener: Mayúscula, número, símbolo especial

### Monedas Soportadas
- ARS (Peso Argentino)
- USD (Futuro)
- EUR (Futuro)

### Lenguajes
- es (Español - por defecto)
- en (Inglés - futuro)

---

## Códigos de Error

| Código | Significado |
|--------|-------------|
| `200` | Éxito |
| `201` | Creado |
| `400` | Solicitud inválida |
| `401` | No autenticado |
| `403` | Prohibido / Usuario desactivado |
| `404` | No encontrado |
| `422` | Error de validación |
| `500` | Error interno del servidor |

---

## Ejemplos de Uso

### Flujo de Registro Completo

```bash
# 1. Registrarse
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@foodara.ar",
    "username": "juanperez",
    "password": "SecurePass123!",
    "first_name": "Juan",
    "last_name": "Pérez"
  }'

# Respuesta:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIs...",
#   "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
#   "token_type": "bearer"
# }

# 2. Obtener perfil
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."

# 3. Actualizar preferencias
curl -X PATCH http://localhost:8000/api/v1/users/me/preferences \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -d '{
    "preferred_budget_ars": 100000,
    "people_at_home": 4,
    "vegetarian": true
  }'
```

---

## Security

### JWT Tokens
- **Access Token**: Válido por 30 minutos
- **Refresh Token**: Válido por 7 días
- Incluir en header: `Authorization: Bearer <token>`

### Password Hashing
- Algoritmo: Argon2
- Las contraseñas NUNCA se transmiten en respuestas

### CORS
- Habilitado en: `localhost:3000`, `localhost:8000`

---

## Próximas Fases

- **FASE 3**: Despensa Digital (FOODARA HOME)
- **FASE 4**: Compras Inteligentes (FOODARA SHOP)

