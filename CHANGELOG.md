# 📋 FOODARA AI - Changelog

## [FASE 2] - 2024-01-15

### ✨ Agregado

#### Servicios
- **UserService**: Servicio centralizado para gestión de usuarios
  - `create_user()`: Crear usuarios con validaciones
  - `get_user_by_id()`: Obtener usuario por ID
  - `get_user_by_email()`: Obtener usuario por email
  - `get_user_by_username()`: Obtener usuario por username
  - `update_user()`: Actualizar información del usuario
  - `delete_user()`: Eliminar usuario
  - `deactivate_user()`: Desactivar usuario
  - `activate_user()`: Activar usuario

- **UserPreferenceService**: Servicio de preferencias
  - `get_preferences()`: Obtener preferencias del usuario
  - `update_preferences()`: Actualizar preferencias
  - `validate_preferences()`: Validar datos de preferencias

#### Schemas Pydantic
- **PreferenceBase**: Base para preferencias
- **PreferenceCreate**: Para crear preferencias
- **PreferenceUpdate**: Para actualizar preferencias
- **PreferenceResponse**: Respuesta de preferencias
- **FoodaryProfileCreate**: Crear perfil completo
- **FoodaryProfileResponse**: Respuesta de perfil completo

#### Endpoints - Autenticación
- `POST /auth/register`: Registro simple
- `POST /auth/register-full`: Registro con preferencias personalizadas
- `POST /auth/login`: Login con email/password

#### Endpoints - Perfil de Usuario
- `GET /users/me`: Obtener perfil actual
- `GET /users/me/profile`: Obtener perfil + preferencias
- `PATCH /users/me`: Actualizar perfil
- `DELETE /users/me`: Eliminar cuenta
- `POST /users/me/deactivate`: Desactivar cuenta
- `POST /users/me/activate`: Activar cuenta

#### Endpoints - Preferencias
- `GET /users/me/preferences`: Obtener preferencias
- `PATCH /users/me/preferences`: Actualizar preferencias

#### Testing
- `tests/test_users.py`: Tests para usuarios
- `tests/conftest.py`: Fixtures y configuración de testing
- Fixtures: `test_db`, `test_client`, `sample_user_data`, `sample_preferences_data`

#### Documentación
- `docs/PHASE2_API.md`: Documentación completa de API FASE 2
- `examples/phase2_examples.sh`: Ejemplos de uso con curl
- `CHANGELOG.md`: Este archivo

#### Validaciones
- Validación de presupuesto: 0 o más
- Validación de cantidad de personas: 1-20
- Validación de tiempo de cocina: 5-480 minutos
- Validación de contraseñas fuertes

### 🔧 Mejorado

#### Logging
- Agregado logging detallado en servicios
- Logs para operaciones de usuarios
- Logs de advertencia para intentos fallidos

#### Seguridad
- Validación mejorada de inputs
- Mejor manejo de errores
- Mensajes de error seguros (sin exponer información sensible)

#### Estructura
- Capa de servicios bien definida
- Separación de responsabilidades
- Código más mantenible

### 📦 Dependencias Agregadas
- `aiosqlite==0.19.0`: Para testing con SQLite async

### 🗂️ Estructura del Proyecto

```
foodara-ai/
├── app/
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py (NUEVO)
│   ├── schemas/
│   │   ├── user.py
│   │   └── preference.py (NUEVO)
│   └── api/routes/
│       ├── auth.py (MEJORADO)
│       ├── users.py (MEJORADO)
│       └── health.py
├── tests/
│   ├── test_health.py
│   ├── test_security.py
│   ├── test_users.py (NUEVO)
│   └── conftest.py (NUEVO)
├── examples/
│   └── phase2_examples.sh (NUEVO)
├── docs/
│   ├── PHASE2_API.md (NUEVO)
│   └── ARCHITECTURE.md
└── CHANGELOG.md (NUEVO)
```

### 🚀 Cómo Usar FASE 2

#### Instalar y Ejecutar
```bash
cd foodara-ai
docker compose up --build
```

#### Registrarse
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@foodara.ar",
    "username": "usuario123",
    "password": "SecurePass123!"
  }'
```

#### Obtener Perfil
```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer <access_token>"
```

#### Actualizar Preferencias
```bash
curl -X PATCH http://localhost:8000/api/v1/users/me/preferences \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "preferred_budget_ars": 100000,
    "people_at_home": 4,
    "vegetarian": true
  }'
```

### 🧪 Testing

```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_users.py -v

# Con cobertura
pytest --cov=app
```

### 📊 Base de Datos

#### Nuevas Tablas
- Tablas ya existentes, sin cambios necesarios

#### Nuevos Campos en `user_preferences`
- `email_notifications` (default: True)
- `waste_alerts` (default: True)
- `budget_alerts` (default: True)

### 🔄 Migraciones

```bash
# Crear migración (si hay cambios en models)
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones
alembic upgrade head
```

### 📝 Notas

- ✅ Todos los endpoints de FASE 2 están implementados
- ✅ Servicios de usuario centralizados
- ✅ Validaciones completas
- ✅ Logging y manejo de errores mejorados
- ✅ Documentación exhaustiva
- ✅ Tests unitarios básicos
- 🔄 Tests de integración en progreso
- 🔄 Cobertura de tests objetivo: 80%+

### 🔜 Próxima Fase

**FASE 3**: Despensa Digital (FOODARA HOME)
- Gestión de inventario
- Registro de alimentos
- Alertas de vencimiento
- Categorización de productos

---

## [FASE 1] - 2024-01-15

### ✨ Agregado

#### Core
- Configuración centralizada
- Seguridad (JWT, Argon2)
- Logging estructurado
- Base de datos con SQLAlchemy

#### API
- Sistema multi-proveedor de IA
- Autenticación básica
- Endpoints de salud

#### Models
- 16 modelos SQLAlchemy
- Relaciones completas
- Base de datos lista

#### Docker
- Docker Compose configurado
- Dockerfile ready
- PostgreSQL incluido

#### Testing
- Tests básicos
- Pytest configurado
- Fixtures preparadas

#### Documentación
- README profesional
- Documentación de arquitectura
- .env.example

---

**FOODARA AI** - Comprá mejor. Comé mejor. Desperdiciá menos. 🌱
