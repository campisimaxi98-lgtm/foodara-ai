# 🚀 FOODARA AI - PHASE 2 - Quick Start

## Inicio Rápido - FASE 2

¡Bienvenido a FOODARA PHASE 2! Aquí puedes gestionar usuarios y preferencias.

### 📋 Requisitos

- Docker & Docker Compose
- O: Python 3.12+ + PostgreSQL local

---

## Opción 1: Docker (Recomendado)

### 1. Iniciar FOODARA

```bash
cd /home/claude/foodara-ai
docker compose up --build
```

Espera hasta ver:
```
✅ Base de datos inicializada
🚀 FOODARA AI v1.0.0 iniciando...
```

### 2. Verificar que está funcionando

```bash
# En otra terminal
curl http://localhost:8000/api/v1/health | jq
```

Deberías ver:
```json
{
  "status": "healthy",
  "service": "FOODARA AI",
  "version": "1.0.0"
}
```

---

## Opción 2: Local

### 1. Preparar ambiente

```bash
cd /home/claude/foodara-ai

# Crear .env
cp .env.example .env

# Crear virtual environment
python3.12 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Inicializar BD (requiere PostgreSQL corriendo)
alembic upgrade head

# Ejecutar servidor
uvicorn app.main:app --reload
```

---

## 🎯 Pruebas Rápidas

### 1. Registrarse

```bash
# Opción simple (con preferencias por defecto)
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@foodara.ar",
    "username": "juanperez",
    "password": "SecurePass123!",
    "first_name": "Juan",
    "last_name": "Pérez"
  }'
```

Respuesta esperada:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

**Copia el `access_token` para los próximos pasos.**

### 2. Ver tu perfil

```bash
TOKEN="eyJ..."  # Reemplaza con tu token

curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Ver tus preferencias

```bash
curl -X GET http://localhost:8000/api/v1/users/me/preferences \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Actualizar preferencias

```bash
curl -X PATCH http://localhost:8000/api/v1/users/me/preferences \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "preferred_budget_ars": 100000,
    "people_at_home": 4,
    "cooking_time_available_minutes": 60,
    "vegetarian": true,
    "email_notifications": true
  }'
```

---

## 🔐 Consideraciones de Seguridad

### Contraseña Fuerte

Tu contraseña debe tener:
- ✅ Mínimo 8 caracteres
- ✅ Al menos 1 mayúscula
- ✅ Al menos 1 número
- ✅ Al menos 1 símbolo especial (`!@#$%^&*`)

Ejemplos válidos:
- `SecurePass123!`
- `FoobaraBest@2024`
- `Argentina.2025#Rocks`

### Token JWT

El `access_token` es válido por **30 minutos**.
El `refresh_token` es válido por **7 días**.

Siempre incluye en requests protegidos:
```
Authorization: Bearer <access_token>
```

---

## 📱 Endpoints Principales

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/register` | Registrar usuario |
| POST | `/auth/register-full` | Registrar con preferencias |
| POST | `/auth/login` | Login |

### Perfil

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/users/me` | Tu perfil |
| GET | `/users/me/profile` | Tu perfil + preferencias |
| PATCH | `/users/me` | Actualizar perfil |
| DELETE | `/users/me` | Eliminar cuenta ⚠️ |

### Preferencias

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/users/me/preferences` | Tus preferencias |
| PATCH | `/users/me/preferences` | Actualizar preferencias |

### Control de Cuenta

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/users/me/deactivate` | Desactivar cuenta |
| POST | `/users/me/activate` | Activar cuenta |

---

## 🧪 Testing

### Ejecutar tests

```bash
# Todos los tests
pytest

# Solo tests de usuarios
pytest tests/test_users.py -v

# Con cobertura
pytest --cov=app

# Tests específicos
pytest tests/test_users.py::TestUserRegistration::test_register_valid_user -v
```

---

## 📊 Documentación Interactiva

Una vez que FOODARA esté corriendo, accede a:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

Aquí puedes probar todos los endpoints interactivamente.

---

## 🛠️ Troubleshooting

### "Port already in use"

```bash
# Cambiar puerto en docker-compose.yml
# O matar proceso en el puerto
lsof -i :8000  # Ver proceso
kill -9 <PID>  # Terminar proceso
```

### "Connection refused to database"

```bash
# Verificar que PostgreSQL está corriendo
docker ps

# Reiniciar servicios
docker compose down
docker compose up --build
```

### "Invalid token"

- El token puede haber expirado
- Registrate nuevamente para obtener un nuevo token
- Verifica que estés usando `Bearer <token>` correctamente

---

## 📚 Documentación Completa

Para información más detallada, ver:

- **API Docs**: `docs/PHASE2_API.md`
- **Arquitectura**: `docs/ARCHITECTURE.md`
- **Ejemplos**: `examples/phase2_examples.sh`
- **README**: `README.md`

---

## 🎯 Siguientes Pasos

Una vez domines FASE 2, puedes:

1. **FASE 3**: Crear tu despensa digital (inventario de alimentos)
2. **FASE 4**: Usar compras inteligentes para encontrar mejores productos
3. **FASE 5**: Generar menús optimizados

---

## 📞 Ayuda

Si tienes problemas:

1. Revisa `docs/PHASE2_API.md` para detalles de endpoints
2. Verifica logs en la consola de Docker
3. Abre un issue en GitHub si encuentras un bug

---

## ✨ Características FASE 2

✅ Autenticación con JWT
✅ Gestión de usuarios
✅ Preferencias personalizadas
✅ Validaciones robustas
✅ Seguridad mejorada
✅ Logging completo
✅ Testing
✅ Documentación

---

## 🚀 ¡Listo para empezar!

```bash
# 1. Ir al directorio
cd /home/claude/foodara-ai

# 2. Iniciar FOODARA
docker compose up --build

# 3. En otra terminal, registrarse
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"tu@email.ar","username":"tuuser","password":"TuPass123!"}'

# 4. ¡A explorar FOODARA! 🍽️
```

---

**FOODARA AI** - Comprá mejor. Comé mejor. Desperdiciá menos. 🌱
