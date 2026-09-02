import '../core/api_client.dart';
import '../models/auth_models.dart';

/// Servicio de autenticación contra la API FOODARA.
class AuthService {
  AuthService(this._api);

  final ApiClient _api;

  Future<AuthSession> login(String email, String password) async {
    final data = await _api.request('POST', '/auth/login', body: {
      'email': email,
      'password': password,
    });
    final session = AuthSession.fromJson(data as Map<String, dynamic>);
    _api.accessToken = session.accessToken;
    if (session.refreshToken.isNotEmpty) {
      _api.refreshToken = session.refreshToken;
    }
    return session;
  }

  Future<AuthSession> register({
    required String email,
    required String username,
    required String password,
    String? firstName,
    String? lastName,
  }) async {
    final data = await _api.request('POST', '/auth/register', body: {
      'email': email,
      'username': username,
      'password': password,
      if (firstName != null && firstName.isNotEmpty) 'first_name': firstName,
      if (lastName != null && lastName.isNotEmpty) 'last_name': lastName,
    });
    final session = AuthSession.fromJson(data as Map<String, dynamic>);
    _api.accessToken = session.accessToken;
    if (session.refreshToken.isNotEmpty) {
      _api.refreshToken = session.refreshToken;
    }
    return session;
  }

  Future<User> getCurrentUser() async {
    final data = await _api.request('GET', '/users/me');
    return User.fromJson(data as Map<String, dynamic>);
  }
}
