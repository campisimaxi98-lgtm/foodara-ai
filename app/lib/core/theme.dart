import 'package:flutter/material.dart';

/// Paleta de colores compartida para paneles que no dependen del tema.
class AppColors {
  AppColors._();
  static const Color primary = Color(0xFF2E7D32);
  static const Color accent = Color(0xFFF9A825);
  static const Color background = Color(0xFFF6F8F6);
}

/// Tema central de FOODARA AI.
class AppTheme {
  AppTheme._();

  static const Color primary = Color(0xFF2E7D32); // verde FOODARA
  static const Color primaryDark = Color(0xFF005005);
  static const Color accent = Color(0xFFF9A825); // ámbar (desperdicio/alertas)
  static const Color background = Color(0xFFF6F8F6);
  static const Color surface = Colors.white;

  static ThemeData light() {
    final base = ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primary,
        brightness: Brightness.light,
        primary: primary,
        secondary: accent,
        surface: surface,
      ),
    );

    return base.copyWith(
      scaffoldBackgroundColor: background,
      appBarTheme: const AppBarTheme(
        backgroundColor: primary,
        foregroundColor: Colors.white,
        elevation: 0,
        centerTitle: false,
      ),
      cardTheme: CardThemeData(
        color: surface,
        elevation: 1,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: surface,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFFD0D7D0)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFFD0D7D0)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: primary, width: 2),
        ),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: primary,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(vertical: 16),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
      ),
    );
  }
}
