# FOODARA AI — App (Flutter)

Aplicación cliente de FOODARA AI construida con **Flutter**. Un solo código base para:

- 📱 **Android**
- 🍎 **iOS / iPhone**
- 🖥️ **Windows desktop**
- 🌐 **Web**

Consume la API del backend FOODARA (ver `../README.md`).

## ✨ Funcionalidades

- 🔐 **Autenticación**: login, registro y renovación automática de token (refresh).
- 🏠 **Hogares (FOODARA HOME)**: crear y listar hogares compartidos.
- 🛒 **Despensa digital**: agregar alimentos, cantidades, precios, vencimientos; marcar consumido o desperdiciado; alertas de vencimiento ("El yogur vence en 2 días").
- 📊 **Resumen determinístico**: valor estimado, próximos a vencer, vencidos y desperdiciados.
- ⚙️ **URL de servidor configurable** desde la pantalla de login (para desarrollo).

## 🚀 Requisitos

- Flutter 3.x (probado en 3.47)
- Android: Android Studio / SDK 36
- iOS: macOS con Xcode y CocoaPods
- Windows: Visual Studio con la carga de trabajo "Desktop development with C++"

## 🧑‍💻 Run en desarrollo

La URL de la API por defecto según plataforma:

| Plataforma | URL por defecto |
|------------|-----------------|
| Android emulador | `http://10.0.2.2:8000` |
| iOS / Windows / Web | `http://localhost:8000` |
| Device físico | configurá la IP de tu PC desde el login |

```bash
cd app
flutter pub get
flutter run
```

## 📦 Builds

**Android (APK):**
```bash
flutter build apk --release
# con URL de producción
flutter build apk --release --dart-define=FOODARA_API_URL=https://api.tudominio.com
```

**iOS (requiere Mac + Xcode):**
```bash
flutter build ios --release
```

**Windows (requiere Visual Studio C++):**
```bash
flutter build windows --release
```

**Web:**
```bash
flutter build web --release
```

## 🧪 Tests

```bash
flutter test
```

## 🗂️ Estructura

```
lib/
  main.dart              # entrada y raíz de Provider
  core/                  # api_config, api_client, theme
  models/                # user, household, pantry_item, pantry_summary
  services/              # auth, household, pantry
  state/                 # auth_state (Provider)
  screens/               # splash, login, register, home, pantry, summary, households, profile
```
