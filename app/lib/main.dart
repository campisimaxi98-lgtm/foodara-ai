import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'core/api_config.dart';
import 'core/theme.dart';
import 'screens/splash_screen.dart';
import 'state/auth_state.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await ApiConfig.loadOverride();
  final authState = await AuthState.create();
  runApp(FoodaraApp(authState: authState));
}

class FoodaraApp extends StatelessWidget {
  const FoodaraApp({super.key, required this.authState});

  final AuthState authState;

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider.value(
      value: authState,
      child: MaterialApp(
        title: 'FOODARA AI',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.light(),
        home: const SplashScreen(),
      ),
    );
  }
}
