import 'package:flutter/material.dart';

import '../core/theme.dart';
import 'pantry_screen.dart';
import 'summary_screen.dart';
import 'households_screen.dart';
import 'profile_screen.dart';
import 'pantry_form_screen.dart';

/// Pantalla principal con navegación inferior.
class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _index = 0;

  static const _titles = ['Despensa', 'Resumen', 'Hogares', 'Perfil'];

  @override
  Widget build(BuildContext context) {
    final body = switch (_index) {
      0 => const PantryScreen(),
      1 => const SummaryScreen(),
      2 => const HouseholdsScreen(),
      _ => const ProfileScreen(),
    };

    return Scaffold(
      appBar: AppBar(title: Text(_titles[_index])),
      body: body,
      floatingActionButton: _index == 0
          ? FloatingActionButton(
              backgroundColor: AppColors.primary,
              foregroundColor: Colors.white,
              onPressed: () {
                Navigator.of(context).push(
                  MaterialPageRoute(builder: (_) => const PantryFormScreen()),
                );
              },
              tooltip: 'Agregar alimento',
              child: const Icon(Icons.add),
            )
          : null,
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (i) => setState(() => _index = i),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.kitchen_outlined),
            selectedIcon: Icon(Icons.kitchen),
            label: 'Despensa',
          ),
          NavigationDestination(
            icon: Icon(Icons.donut_large_outlined),
            selectedIcon: Icon(Icons.donut_large),
            label: 'Resumen',
          ),
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home),
            label: 'Hogares',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outline),
            selectedIcon: Icon(Icons.person),
            label: 'Perfil',
          ),
        ],
      ),
    );
  }
}
