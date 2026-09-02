# 🍽️ FOODARA AI

**Comprá mejor. Comé mejor. Desperdiciá menos.**

Una plataforma tecnológica de inteligencia artificial diseñada para optimizar las decisiones alimentarias de los usuarios argentinos.

## 📋 Descripción

FOODARA AI es un **ecosistema inteligente de alimentación** que conecta mediante IA:

- 🛒 **Compras inteligentes**: Análisis y recomendación de productos
- 🍽️ **Planificación de comidas**: Generación de menús optimizados
- 🏠 **Despensa digital**: Registro inteligente de inventario
- ♻️ **Reducción de desperdicio**: Detección y prevención
- 💰 **Optimización presupuestaria**: Máximo valor por dinero
- 🧾 **Lectura inteligente de tickets**: OCR y análisis automático
- 📷 **Reconocimiento visual**: Identificación de productos
- 🤖 **Asistente conversacional**: Interacción natural
- 📊 **Estadísticas**: Seguimiento del comportamiento
- 🎮 **Gamificación**: Motivación y logros
- 🧠 **Aprendizaje personalizado**: Mejora continua

## 🎯 Problema

Los usuarios argentinos enfrentan:

- ❌ Incertidumbre al comprar
- ❌ Desperdicio de alimentos
- ❌ Presupuestos limitados
- ❌ Falta de planificación

## ✅ Solución

FOODARA proporciona:

- ✨ Recomendaciones inteligentes
- 🧠 Aprendizaje del usuario
- 💡 Decisiones informadas
- 📈 Progreso medible

## 🚀 Comienza Rápido

### Requisitos Previos

- Python 3.12+
- Docker & Docker Compose
- PostgreSQL (incluido en Docker Compose)

### Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/foodara/foodara-ai.git
cd foodara-ai

# Crear archivo .env
cp .env.example .env

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

Acceder a: `http://localhost:8000`

### Instalación con Docker

```bash
# Construir e iniciar
docker compose up --build

# Aplicar migraciones (en otra terminal)
docker compose exec api alembic upgrade head
```

Acceder a: `http://localhost:8000`

## 📡 API

### Documentación

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

### Endpoints Principales (FASE 1)

```
# Health
GET    /api/v1/health
GET    /api/v1/info
GET    /api/v1/ai/providers

# Authentication
POST   /api/v1/auth/register
POST   /api/v1/auth/login

# Users
GET    /api/v1/users/me
PATCH  /api/v1/users/me
GET    /api/v1/users/{user_id}
```

## 🗄️ Base de Datos

### Modelos Principales

```
User
├── UserPreference
├── PantryItem
├── ShoppingList
├── Purchase
├── Receipt
├── MealPlan
├── AIConversation
├── WasteRecord
└── Achievement
```

### Migraciones

```bash
# Crear migración
alembic revision --autogenerate -m "Descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir migraciones
alembic downgrade -1
```

## 🤖 Sistema de IA

### Arquitectura Multi-Provider

FOODARA soporta múltiples proveedores de IA:

- 🟣 **Anthropic Claude**: Provider predeterminado
- 🔵 **OpenAI**: Alternativa principal
- ⚪ **Mock**: Para testing y desarrollo

### Configuración

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_ENABLED=True

OPENAI_API_KEY=sk-...
OPENAI_ENABLED=False

DEFAULT_AI_PROVIDER=anthropic
```

### Características

- ✅ Fallback automático entre providers
- ✅ Circuit breaker
- ✅ Logging y monitoreo
- ✅ Health checks

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=app

# Específicos
pytest tests/test_health.py -v

# De un módulo
pytest tests/ -k "security"
```

### Estructura de Tests

```
tests/
├── test_health.py
├── test_security.py
└── conftest.py (fixtures)
```

## 📁 Estructura del Proyecto

```
foodara-ai/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── users.py
│   │       └── health.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   ├── models/
│   ├── schemas/
│   ├── database/
│   ├── ai/
│   │   ├── base.py
│   │   ├── ai_service.py
│   │   └── providers/
│   └── modules/
│
├── tests/
├── alembic/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## 🔐 Seguridad

### Implementado

- ✅ JWT para autenticación
- ✅ Hashing con Argon2
- ✅ Validación de inputs
- ✅ CORS configurado
- ✅ Variables de entorno
- ✅ Rate limiting preparado

### Mejores Prácticas

- 🔒 NUNCA guardar contraseñas en texto plano
- 🔒 NUNCA incluir API keys en código
- 🔒 Usar HTTPS en producción
- 🔒 Validar y sanitizar inputs
- 🔒 Implementar rate limiting

## 🌍 Configuración Argentina

FOODARA AI está optimizado para Argentina:

- 💵 Moneda: ARS (Peso Argentino)
- 🗣️ Idioma: Español
- 🕐 Zona horaria: America/Argentina/Buenos_Aires
- 🏪 Supermercados y almacenes locales
- 🍲 Comidas típicas argentinas

## 📈 Roadmap

### FASE 1 ✅ Arquitectura Base
- Estructura del proyecto
- Autenticación
- Base de datos
- Sistema multi-IA

### FASE 2 - Usuarios y Perfil
- Gestión de usuarios
- Preferencias
- Configuración

### FASE 3 - Despensa Digital
- FOODARA HOME
- Inventario
- Vencimientos

### FASE 4 - Compras Inteligentes
- FOODARA SHOP
- Análisis de productos
- Comparativas

### FASE 5 - Planificación
- FOODARA MENU
- Generación de menús
- Optimización presupuestaria

### FASE 6 - Reducción de Desperdicio
- FOODARA ZERO
- Detección de riesgos
- Recomendaciones

### FASE 7 - Asistente IA
- FOODARA AI
- Conversación natural
- Integración de módulos

### FASE 8 - Visión Artificial
- OCR para tickets
- Reconocimiento de productos
- Análisis de imágenes

### FASE 9 - Dashboard
- Estadísticas
- Visualización de datos
- Reportes

### FASE 10 - Gamificación
- FOODARA SCORE
- Logros y desafíos
- Leaderboards

### FASE 11 - Seguridad Avanzada
- Auditoría
- Encryption
- Compliance

### FASE 12 - Producción
- Testing completo
- Docker optimizado
- Documentación
- Deployment

## 📚 Documentación

- [API Documentation](/docs/api.md)
- [Database Schema](/docs/database.md)
- [AI System](/docs/ai.md)
- [Architecture](/docs/architecture.md)

## 🤝 Contribuir

FOODARA es un proyecto en desarrollo activo.

```bash
# Fork el repositorio
# Crea una rama: git checkout -b feature/feature-name
# Commit cambios: git commit -am 'Add feature'
# Push: git push origin feature/feature-name
# Abre Pull Request
```

## 📝 Licencia

MIT License - Abierto para uso y modificación

## 👥 Equipo

Desarrollado con 🍲 para Argentina

## 📞 Soporte

- 📧 Email: support@foodara.ar
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

**FOODARA AI** - Comprá mejor. Comé mejor. Desperdiciá menos. 🌱

---

## 📱 App Móvil y Desktop (Flutter)

La app cliente está en pp/ y usa **un solo código base** en Flutter para:

- **Android** (APK)
- **iOS / iPhone**
- **Windows desktop**
- **Web**

### Funcionalidades de la app

- Autenticación (login, registro, refresh de token automático)
- Hogares (FOODARA HOME): crear y listar
- Despensa digital: agregar alimentos, vencimientos, precios; marcar consumido/desperdiciado
- Resumen determinístico: valor estimado, próximos a vencer, vencidos
- URL del servidor configurable desde la pantalla de login

### Builds

`ash
cd app
flutter pub get

# Android
flutter build apk --release --dart-define=FOODARA_API_URL=https://api.tudominio.com

# iOS (requiere Mac + Xcode)
flutter build ios --release

# Windows (requiere Visual Studio con C++ workload)
flutter build windows --release

# Web
flutter build web --release

# Tests
flutter test
`

Más detalles en [app/README.md](app/README.md).
