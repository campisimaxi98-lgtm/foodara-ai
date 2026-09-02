# 🚀 FOODARA AI - Despliegue en Render.com

El proyecto ya está **preparado y pusheado** para desplegarse en Render.com.
Estos son los pasos que tenés que completar desde tu cuenta (requieren
autenticación que no puedo hacer por vos).

---

## ✅ Lo que ya está listo en el repo

- `render.yaml` → Blueprint que Render detecta y usa automáticamente
  - Crea un **PostgreSQL free**
  - Crea el **servicio web** FastAPI (Docker)
  - Genera `SECRET_KEY` automáticamente
  - Conecta la DB vía `DATABASE_URL`
- `Dockerfile` + `docker-start.sh` → arranque productivo que crea las tablas
- `app/core/config.py` → soporta `DATABASE_URL` directo (compatible Render)
- Health check en `/api/v1/health`

---

## 🧭 Pasos manuales (5 min, una sola vez)

### 1. Crear cuenta en Render
- Andá a **https://render.com** → "Get Started" → registrate gratis
  (puede ser con cuenta de GitHub o email)

### 2. Conectar tu GitHub
- En el dashboard: **Account Settings → Connect a GitHub account**
- Autorizá y elegí el repositorio **campisimaxi98/foodara-ai**
- Asegurate de que Render pueda ver tu repo (el repo es público, así que no
  hace falta más).

### 3. Desplegar con Blueprint
- En el dashboard, clic en **New → Blueprint**
- Elegí el repositorio `foodara-ai`
- Render detecta el `render.yaml` y te muestra: `foodara-db` + `foodara-api`
- Clic en **Apply**
- Esperá a que depliegue (primer build tarda ~5-10 min)

### 4. Obtener tu URL pública
- Cuando termine, entrá al servicio `foodara-api` → pestaña **Events/Logs**
- La URL quedará como: `https://foodara-api.onrender.com`
- Probá: `https://foodara-api.onrender.com/api/v1/health`
  → debería responder `{"status": "healthy", ...}`

---

## 📱 Configurar la app (APK) con la URL del backend

La app Flutter ya permite cambiar el servidor desde la **pantalla de login**
(modo avanzado). En el celular, al iniciar sesión, configurá la URL:

```
https://foodara-api.onrender.com
```

> La app guarda la URL y la reutiliza entre sesiones.

Alternativamente, podés reconstruir el APK apuntando a la URL definitiva:

```bash
cd app
flutter build apk --release --dart-define=FOODARA_API_URL=https://foodara-api.onrender.com
```

---

## 🔒 Seguridad en producción

- `APP_ENV=production` (no expone `/api/docs` ni `/api/redoc`)
- `SECRET_KEY` auto-generada y guardada como secreto en Render (no en Git)
- `ANTHROPIC_ENABLED=false` y `OPENAI_ENABLED=false` (IA off hasta tener keys)
- Rate limiting activo (100 req/60s)
- CORS configurado

### Para habilitar la IA (cuando tengas API keys)
En el servicio `foodara-api` → **Environment** → agregar:
```
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_ENABLED=true
```
o
```
OPENAI_API_KEY=sk-...
OPENAI_ENABLED=true
DEFAULT_AI_PROVIDER=openai
```

---

## 🗄️ Base de datos

- PostgreSQL free en Render (90 días en el plan free, luego pasa a pago)
- Las tablas se crean automáticamente al arrancar (`docker-start.sh`)
- Para acceder a la DB: servicio `foodara-db` → pestaña **Connect**

---

## 🆓 Nota sobre el plan free

Render free tiene límites:
- El servicio web **se apaga tras 15 min de inactividad** (tarda unos segundos
  en volver a arrancar al recibir una petición).
- El PostgreSQL free expira a los 90 días.
Para un servicio 24/7 es necesario un plan de pago ($7/mes aprox).

---

## 🔄 Para redeployar tras cambios

- Hacé push a `main` → Render redeploya automáticamente
- O en Render: Manual Deploy → Deploy latest commit

---

**FOODARA AI** - Comprá mejor. Comé mejor. Desperdiciá menos. 🌱
