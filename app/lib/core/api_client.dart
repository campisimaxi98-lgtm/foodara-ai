import 'dart:convert';

import 'package:http/http.dart' as http;

import 'api_config.dart';

/// Error tipado devuelto por la API FOODARA.
class ApiException implements Exception {
  ApiException(this.statusCode, this.message);

  final int statusCode;
  final String message;

  bool get isUnauthorized => statusCode == 401;
  bool get isForbidden => statusCode == 403;
  bool get isNotFound => statusCode == 404;

  @override
  String toString() => message;
}

/// Cliente HTTP centralizado para la API FOODARA.
///
/// - Adjunta el token de acceso a cada request.
/// - Maneja el refresh automático del access token cuando expira.
/// - Devuelve objetos [ApiException] con mensajes legibles.
class ApiClient {
  ApiClient({required this.accessToken, required this.refreshToken});

  String? accessToken;
  String? refreshToken;

  /// Invocado por el backend cuando cambian los tokens (login / refresh).
  Future<void> Function(String access, String refresh)? onTokensChanged;

  static const _timeout = Duration(seconds: 20);

  Uri _uri(String path, [Map<String, dynamic>? query]) {
    final fullPath = '${ApiConfig.baseUrl}${ApiConfig.apiPrefix}$path';
    final uri = Uri.parse(fullPath);
    if (query == null || query.isEmpty) {
      return uri;
    }
    return uri.replace(
      queryParameters: query.map((k, v) => MapEntry(k, v.toString())),
    );
  }

  Map<String, String> _headers({bool json = true}) {
    return {
      if (json) 'Content-Type': 'application/json',
      if (accessToken != null && accessToken!.isNotEmpty)
        'Authorization': 'Bearer $accessToken',
    };
  }

  /// Ejecuta un request e intenta refrescar el token una vez si da 401.
  Future<dynamic> request(
    String method,
    String path, {
    Map<String, dynamic>? query,
    Object? body,
  }) async {
    http.Response response = await _send(method, path, query: query, body: body);

    if (response.statusCode == 401 && refreshToken != null && refreshToken!.isNotEmpty) {
      final refreshed = await _tryRefresh();
      if (refreshed) {
        response = await _send(method, path, query: query, body: body);
      }
    }

    return _decode(response);
  }

  Future<http.Response> _send(
    String method,
    String path, {
    Map<String, dynamic>? query,
    Object? body,
  }) async {
    final uri = _uri(path, query);
    final headers = _headers();

    late http.Response response;

    switch (method.toUpperCase()) {
      case 'GET':
        response = await _get(uri, headers);
        break;
      case 'POST':
        response = await _post(uri, headers, body);
        break;
      case 'PATCH':
        response = await _patch(uri, headers, body);
        break;
      case 'PUT':
        response = await _put(uri, headers, body);
        break;
      case 'DELETE':
        response = await _delete(uri, headers);
        break;
      default:
        throw ApiException(400, 'Método no soportado: $method');
    }

    return response;
  }

  Future<http.Response> _get(Uri uri, Map<String, String> headers) {
    return http
        .get(uri, headers: headers)
        .timeout(_timeout);
  }

  Future<http.Response> _post(
      Uri uri, Map<String, String> headers, Object? body) {
    return http
        .post(uri, headers: headers, body: _encodeBody(body))
        .timeout(_timeout);
  }

  Future<http.Response> _patch(
      Uri uri, Map<String, String> headers, Object? body) {
    return http
        .patch(uri, headers: headers, body: _encodeBody(body))
        .timeout(_timeout);
  }

  Future<http.Response> _put(
      Uri uri, Map<String, String> headers, Object? body) {
    return http
        .put(uri, headers: headers, body: _encodeBody(body))
        .timeout(_timeout);
  }

  Future<http.Response> _delete(Uri uri, Map<String, String> headers) {
    return http
        .delete(uri, headers: headers)
        .timeout(_timeout);
  }

  String? _encodeBody(Object? body) {
    if (body == null) return null;
    return jsonEncode(body);
  }

  /// Decodifica la respuesta HTTP en un objeto Dart.
  dynamic _decode(http.Response response) {
    final body = response.body;
    if (response.statusCode >= 200 && response.statusCode < 300) {
      if (body.isEmpty) return null;
      return jsonDecode(body);
    }

    final detail = _extractDetail(body);
    throw ApiException(response.statusCode, detail);
  }

  String _extractDetail(String body) {
    if (body.isEmpty) return 'Error de conexión con el servidor';
    try {
      final decoded = jsonDecode(body);
      if (decoded is Map<String, dynamic>) {
        final detail = decoded['detail'];
        if (detail is String && detail.isNotEmpty) return detail;
        if (detail is Map && detail.isNotEmpty) {
          // Errores de validación de Pydantic (FastAPI)
          final first = detail.entries.first.value;
          if (first is List && first.isNotEmpty) {
            return first.first.toString();
          }
          return 'Datos inválidos enviados al servidor';
        }
        if (decoded['error'] is String) return decoded['error'] as String;
      }
    } catch (_) {
      // Ignorar parsing v fallar con mensaje por defecto.
    }
    return 'No se pudo completar la operación';
  }

  /// Intenta renovar el access token con el refresh token.
  Future<bool> _tryRefresh() async {
    if (refreshToken == null || refreshToken!.isEmpty) return false;

    try {
      final uri = _uri('/auth/refresh');
      final response = await http
          .post(uri, headers: {'Content-Type': 'application/json'}, body: jsonEncode({
            'refresh_token': refreshToken,
          }))
          .timeout(_timeout);

      if (response.statusCode != 200) return false;

      final data = jsonDecode(response.body) as Map<String, dynamic>;
      final newAccess = data['access_token'] as String;
      final newRefresh = data['refresh_token'] as String?;

      accessToken = newAccess;
      if (newRefresh != null) {
        refreshToken = newRefresh;
      }

      await onTokensChanged?.call(accessToken!, refreshToken ?? '');
      return true;
    } catch (_) {
      return false;
    }
  }
}
