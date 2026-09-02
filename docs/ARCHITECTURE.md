# 🏗️ FOODARA AI - Arquitectura

## Visión de Arquitectura

FOODARA AI es un sistema modular, escalable y orientado a IA para optimizar decisiones alimentarias.

## Capas de Arquitectura

```
┌─────────────────────────────────────────────────┐
│           Frontend (Futuro)                      │
│   (Flutter, Web, Desktop, Mobile)               │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│         API Gateway (FastAPI)                   │
│    Autenticación, CORS, Rate Limiting           │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│      Service Layer (Módulos FOODARA)            │
│  Shop | Menu | Pantry | Waste | Receipts       │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│    Core Services (Transversales)                │
│  AI Service | Database Service | Security      │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│    Data Access Layer (SQLAlchemy/ORM)           │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│    PostgreSQL Database                          │
└─────────────────────────────────────────────────┘

```

## Componentes Principales

### 1. **API Gateway** (`app/api`)
- Punto de entrada único
- Autenticación JWT
- CORS y seguridad
- Rate limiting (preparado)

### 2. **Core Layer** (`app/core`)
- Configuración centralizada
- Seguridad (JWT, hashing)
- Logging estructurado

### 3. **AI Layer** (`app/ai`)
```
AIService (Orquestador)
    ├── Claude Provider
    ├── OpenAI Provider
    ├── Mock Provider
    └── Fallback automático
```

### 4. **Data Layer** (`app/database`)
- SQLAlchemy ORM
- Alembic Migrations
- Connection pooling

### 5. **Models** (`app/models`)
- Usuarios
- Despensa
- Compras
- Recetas
- Conversaciones IA
- Gamificación

### 6. **Módulos de Negocio** (`app/modules`)
```
modules/
├── shopping/    (FOODARA SHOP)
├── menu/        (FOODARA MENU)
├── pantry/      (FOODARA HOME)
├── waste/       (FOODARA ZERO)
├── receipts/    (Lectura OCR)
├── vision/      (Reconocimiento)
├── nutrition/   (Información nutricional)
├── economy/     (Optimización económica)
└── gamification/ (Logros y puntos)
```

## FOODARA BRAIN

El cerebro central del sistema:

```
                   FOODARA BRAIN
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
    SHOP AI          MENU AI         WASTE AI
        │               │               │
        └───────────────┼───────────────┘
                        ▼
                   PANTRY ENGINE
                        ▼
                   USER PROFILE
                        ▼
                 DECISION ENGINE
                        ▼
                  FOODARA AI (Chat)
```

### Flujo de Datos

```
Usuario
   │
   ▼
FOODARA AI (NLP)
   │
   ├─► Detección de intención
   │
   ├─► Consulta de módulos
   │   ├── Despensa
   │   ├── Presupuesto
   │   ├── Historial
   │   ├── Preferencias
   │   └── Compras previas
   │
   ├─► Decisión Engine
   │   ├── Análisis
   │   ├── Recomendaciones
   │   └── Alternativas
   │
   └─► Respuesta personalizada
```

## Patrones de Diseño

### 1. **Dependency Injection**
```python
@app.get("/endpoint")
async def handler(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    ...
```

### 2. **Provider Pattern**
```python
class BaseAIProvider(ABC):
    async def chat(...) -> AIResponse:
        ...

class ClaudeProvider(BaseAIProvider):
    async def chat(...):
        # Implementación específica

class MockProvider(BaseAIProvider):
    async def chat(...):
        # Mock para testing
```

### 3. **Service Layer**
```python
class AIService:
    async def chat(...):
        # Orquesta providers
        # Maneja fallback
        # Logging y monitoreo
```

### 4. **Repository Pattern** (para futuras fases)
```python
class UserRepository:
    async def get_by_id(...)
    async def create(...)
    async def update(...)
```

## Flujo de Autenticación

```
1. Usuario registra/login
        ↓
2. Contraseña hasheada con Argon2
        ↓
3. JWT generado (access_token + refresh_token)
        ↓
4. Token incluido en Authorization header
        ↓
5. Middleware verifica token
        ↓
6. Usuario autenticado accede a endpoints protegidos
```

## Seguridad

### En Tránsito
- HTTPS en producción
- CORS configurado
- Rate limiting preparado

### En Reposo
- Contraseñas: Argon2
- API Keys: Variables de entorno
- Base de datos: Conexión segura

### Validación
- Pydantic schemas
- Type hints
- Input sanitization

## Escalabilidad

### Horizontal
```
Load Balancer
     │
  ┌──┴──┬──┐
  ▼     ▼  ▼
API1  API2 API3
  └──┬──┴──┘
     │
PostgreSQL (Connection Pool)
```

### Vertical
- Connection pooling
- Async/await
- Caching preparado (Redis)

## Tecnología Stack

| Capa | Tecnología |
|------|-----------|
| API | FastAPI |
| ORM | SQLAlchemy |
| BD | PostgreSQL |
| Auth | JWT + Argon2 |
| IA | Multi-provider (Claude, OpenAI) |
| Testing | Pytest |
| Container | Docker |
| Migrations | Alembic |

## Flujo de Desarrollo

```
Feature Branch
     ↓
Tests (pytest)
     ↓
Code Review
     ↓
Merge a Main
     ↓
Docker Build
     ↓
Staging
     ↓
Production
```

## Monitoreo

### Health Checks
```
GET /api/v1/health
GET /api/v1/ai/providers
```

### Logging
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "logger": "app.ai.ai_service",
  "message": "Usando provider: claude",
  "module": "ai_service",
  "function": "chat",
  "line": 45
}
```

## Próximas Fases

- **FASE 2**: Servicios de usuarios
- **FASE 3**: Módulo de despensa
- **FASE 4**: Módulo de compras
- **FASE 5**: Módulo de menús
- **FASE 6**: Módulo de desperdicio
- **FASE 7**: Chat de IA avanzado
- **FASE 8**: Visión artificial
- **FASE 9**: Dashboard
- **FASE 10**: Gamificación

---

**FOODARA AI** - Arquitectura modular, escalable, segura. 🏗️
