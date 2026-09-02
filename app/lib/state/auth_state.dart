import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../core/api_client.dart';
import '../models/auth_models.dart';
import '../services/auth_service.dart';
import '../services/household_service.dart';
import '../services/pantry_service.dart';

/// Estado global de la sesión FOODARA.
///
/// Maneja el login/registro/logout, la persistencia de tokens en el
/// dispositivo y expone los servicios de la API.
class AuthState extends ChangeNotifier {
  AuthState._();

  static const _kAccess = 'foodara_access_token';
  static const _kRefresh = 'foodara_refresh_token';

  static Future<AuthState> create() async {
    final state = AuthState._();
    final prefs = await SharedPreferences.getInstance();
    final access = prefs.getString(_kAccess) ?? '';
    final refresh = prefs.getString(_kRefresh) ?? '';
    state._api = ApiClient(accessToken: access.isEmpty ? null : access,
        refreshToken: refresh.isEmpty ? null : refresh);
    state._api.onTokensChanged = state._persistTokens;
    state._services();
    return state;
  }

  late ApiClient _api;
  late AuthService _authService;
  late HouseholdService _householdService;
  late PantryService _pantryService;

  User? _user;
  bool _isLoading = false;
  String? _error;

  void _services() {
    _authService = AuthService(_api);
    _householdService = HouseholdService(_api);
    _pantryService = PantryService(_api);
  }

  // Getters
  ApiClient get api => _api;
  AuthService get authService => _authService;
  HouseholdService get householdService => _householdService;
  PantryService get pantryService => _pantryService;
  User? get user => _user;
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get isLoggedIn => _user != null;
  bool get hasStoredToken =>
      (_api.accessToken?.isNotEmpty ?? false) && (_api.refreshToken?.isNotEmpty ?? false);

  Future<void> _persistTokens(String access, String refresh) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kAccess, access);
    if (refresh.isNotEmpty) await prefs.setString(_kRefresh, refresh);
  }

  /// Restaura la sesión si hay un token guardado; de lo contrario devuelve false.
  Future<bool> bootstrap() async {
    if (!hasStoredToken) return false;
    _setLoading(true);
    try {
      _user = await _authService.getCurrentUser();
      _setLoading(false);
      return true;
    } catch (_) {
      // Token inválido/expirado: limpiar sesión.
      await logout();
      _setLoading(false);
      return false;
    }
  }

  Future<bool> login(String email, String password) async {
    _setLoading(true);
    try {
      final session = await _authService.login(email, password);
      await _persistTokens(session.accessToken, session.refreshToken);
      _user = await _authService.getCurrentUser();
      _setError(null);
      _setLoading(false);
      return true;
    } catch (e) {
      _setError(e.toString());
      _setLoading(false);
      return false;
    }
  }

  Future<bool> register({
    required String email,
    required String username,
    required String password,
    String? firstName,
    String? lastName,
  }) async {
    _setLoading(true);
    try {
      final session = await _authService.register(
        email: email,
        username: username,
        password: password,
        firstName: firstName,
        lastName: lastName,
      );
      await _persistTokens(session.accessToken, session.refreshToken);
      _user = await _authService.getCurrentUser();
      _setError(null);
      _setLoading(false);
      return true;
    } catch (e) {
      _setError(e.toString());
      _setLoading(false);
      return false;
    }
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_kAccess);
    await prefs.remove(_kRefresh);
    _api.accessToken = null;
    _api.refreshToken = null;
    _user = null;
    _setError(null);
    notifyListeners();
  }

  void refreshUser() {
    _authService.getCurrentUser().then((u) {
      _user = u;
      notifyListeners();
    }).catchError((_) {});
  }

  void _setLoading(bool value) {
    _isLoading = value;
    notifyListeners();
  }

  void _setError(String? value) {
    _error = value;
    notifyListeners();
  }
}
