// Modelos de autenticación y usuario devueltos por la API FOODARA.

class AuthSession {
  AuthSession({required this.accessToken, required this.refreshToken});

  final String accessToken;
  final String refreshToken;

  factory AuthSession.fromJson(Map<String, dynamic> json) {
    return AuthSession(
      accessToken: json['access_token'] as String,
      refreshToken: (json['refresh_token'] ?? '') as String,
    );
  }
}

class User {
  User({
    required this.id,
    required this.email,
    required this.username,
    this.firstName,
    this.lastName,
  });

  final int id;
  final String email;
  final String username;
  final String? firstName;
  final String? lastName;

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as int,
      email: json['email'] as String,
      username: json['username'] as String,
      firstName: json['first_name'] as String?,
      lastName: json['last_name'] as String?,
    );
  }

  String get displayName =>
      (firstName != null && firstName!.isNotEmpty) ? '$firstName $lastName' : username;
}
