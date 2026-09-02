// Test de humo básico para FOODARA AI.
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:foodara_app/core/theme.dart';

void main() {
  testWidgets('El tema FOODARA se construye sin errores', (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        theme: AppTheme.light(),
        home: const Scaffold(body: Center(child: Text('FOODARA'))),
      ),
    );

    expect(find.text('FOODARA'), findsOneWidget);
    expect(AppColors.primary, isNotNull);
  });
}
