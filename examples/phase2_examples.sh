#!/bin/bash

# FOODARA AI - PHASE 2 Examples
# Ejemplos de uso de endpoints de FASE 2

BASE_URL="http://localhost:8000/api/v1"

echo "🍽️ FOODARA AI - PHASE 2 Examples"
echo "=================================="
echo ""

# ============================================
# 1. REGISTRO SIMPLE
# ============================================

echo "1️⃣ REGISTRO SIMPLE"
echo "==================="

REGISTER_RESPONSE=$(curl -s -X POST $BASE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@foodara.ar",
    "username": "juanperez",
    "password": "SecurePass123!",
    "first_name": "Juan",
    "last_name": "Pérez"
  }')

echo "Response:"
echo $REGISTER_RESPONSE | jq .
echo ""

# Extraer access token
ACCESS_TOKEN=$(echo $REGISTER_RESPONSE | jq -r '.access_token')
echo "Access Token: $ACCESS_TOKEN"
echo ""

# ============================================
# 2. OBTENER PERFIL ACTUAL
# ============================================

echo "2️⃣ OBTENER PERFIL ACTUAL"
echo "========================"

curl -s -X GET $BASE_URL/users/me \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .

echo ""

# ============================================
# 3. OBTENER PREFERENCIAS
# ============================================

echo "3️⃣ OBTENER PREFERENCIAS"
echo "======================="

curl -s -X GET $BASE_URL/users/me/preferences \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .

echo ""

# ============================================
# 4. ACTUALIZAR PREFERENCIAS
# ============================================

echo "4️⃣ ACTUALIZAR PREFERENCIAS"
echo "============================"

curl -s -X PATCH $BASE_URL/users/me/preferences \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "preferred_budget_ars": 100000,
    "people_at_home": 4,
    "cooking_time_available_minutes": 60,
    "vegetarian": true,
    "email_notifications": true,
    "waste_alerts": true,
    "budget_alerts": true
  }' | jq .

echo ""

# ============================================
# 5. OBTENER PERFIL COMPLETO
# ============================================

echo "5️⃣ OBTENER PERFIL COMPLETO (Usuario + Preferencias)"
echo "===================================================="

curl -s -X GET $BASE_URL/users/me/profile \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .

echo ""

# ============================================
# 6. ACTUALIZAR PERFIL
# ============================================

echo "6️⃣ ACTUALIZAR PERFIL DEL USUARIO"
echo "===================================="

curl -s -X PATCH $BASE_URL/users/me \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Juan Carlos",
    "last_name": "Pérez García"
  }' | jq .

echo ""

# ============================================
# 7. LOGIN CON CREDENCIALES
# ============================================

echo "7️⃣ LOGIN CON CREDENCIALES"
echo "=========================="

LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@foodara.ar",
    "password": "SecurePass123!"
  }')

echo "Response:"
echo $LOGIN_RESPONSE | jq .
echo ""

# ============================================
# 8. REGISTRO CON PREFERENCIAS COMPLETAS
# ============================================

echo "8️⃣ REGISTRO CON PREFERENCIAS COMPLETAS"
echo "========================================"

curl -s -X POST $BASE_URL/auth/register-full \
  -H "Content-Type: application/json" \
  -d '{
    "email": "maria@foodara.ar",
    "username": "mariag",
    "password": "StrongPass456!",
    "first_name": "María",
    "last_name": "García",
    "preferences": {
      "currency": "ARS",
      "language": "es",
      "timezone": "America/Argentina/Buenos_Aires",
      "preferred_budget_ars": 50000,
      "people_at_home": 2,
      "cooking_time_available_minutes": 30,
      "vegetarian": true,
      "vegan": false,
      "gluten_free": false,
      "dairy_free": false
    }
  }' | jq .

echo ""

# ============================================
# 9. DESACTIVAR CUENTA
# ============================================

echo "9️⃣ DESACTIVAR CUENTA"
echo "===================="

curl -s -X POST $BASE_URL/users/me/deactivate \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .

echo ""

# ============================================
# 10. ACTIVAR CUENTA
# ============================================

echo "🔟 ACTIVAR CUENTA"
echo "================"

curl -s -X POST $BASE_URL/users/me/activate \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .

echo ""

echo "✅ Ejemplos completados"
echo ""
echo "Documentación completa en: docs/PHASE2_API.md"
