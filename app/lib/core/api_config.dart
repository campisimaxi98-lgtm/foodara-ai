import 'dart:io' show Platform;

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Configuración de la URL base de la API FOODARA.
///
/// La URL por defecto se puede inyectar en tiempo de compilación para
/// apuntar a un servidor de producción:
///
///   flutter build apk --dart-define=FOODARA_API_URL=https://api.tudominio.com
///
/// También se puede sobreescribir en tiempo de ejecución desde la pantalla
/// de login (modo avanzado), útil durante el desarrollo.
class ApiConfig {
  ApiConfig._();

  static const String _fromEnv = String.fromEnvironment('FOODARA_API_URL');
  static const String _prefsKey = 'foodara_api_url';

  /// Override de runtime. Si se define, tiene prioridad sobre todo.
  static String? overrideBaseUrl;

  static Future<void> loadOverride() async {
    final prefs = await SharedPreferences.getInstance();
    final saved = prefs.getString(_prefsKey);
    if (saved != null && saved.isNotEmpty) {
      overrideBaseUrl = saved;
    }
  }

  static Future<void> saveOverride(String url) async {
    overrideBaseUrl = url;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_prefsKey, url);
  }

  static Future<void> clearOverride() async {
    overrideBaseUrl = null;
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_prefsKey);
  }

  static String get baseUrl {
    if (overrideBaseUrl != null && overrideBaseUrl!.isNotEmpty) {
      return overrideBaseUrl!;
    }
    if (_fromEnv.isNotEmpty) {
      return _fromEnv;
    }

    if (kIsWeb) {
      return 'http://localhost:8000';
    }

    switch (Platform.operatingSystem) {
      case 'android':
        // Emulador de Android: 10.0.2.2 apunta al localhost del host.
        return 'http://10.0.2.2:8000';
      default:
        return 'http://localhost:8000';
    }
  }

  /// Prefijo de la API tal como se sirve en el backend.
  static const String apiPrefix = '/api/v1';
}
