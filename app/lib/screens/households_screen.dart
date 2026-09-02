import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/theme.dart';
import '../models/household.dart';
import '../state/auth_state.dart';
import 'household_form_screen.dart';

/// Pantalla de hogares del usuario (FOODARA HOME).
class HouseholdsScreen extends StatefulWidget {
  const HouseholdsScreen({super.key});

  @override
  State<HouseholdsScreen> createState() => _HouseholdsScreenState();
}

class _HouseholdsScreenState extends State<HouseholdsScreen> {
  List<Household>? _households;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _error = null;
      _households = null;
    });
    final svc = context.read<AuthState>().householdService;
    try {
      final households = await svc.listMine();
      if (!mounted) return;
      setState(() => _households = households);
    } catch (e) {
      if (!mounted) return;
      setState(() => _error = e.toString());
    }
  }

  Future<void> _create() async {
    await Navigator.of(context).push(
      MaterialPageRoute(builder: (_) => const HouseholdFormScreen()),
    );
    if (!mounted) return;
    _load();
  }

  Future<void> _delete(Household h) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Eliminar hogar'),
        content: Text('¿Eliminar "${h.name}"? Esta acción no se puede deshacer.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('Cancelar'),
          ),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: const Color(0xFFC62828)),
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Eliminar'),
          ),
        ],
      ),
    );
    if (confirmed != true) return;

    final svc = context.read<AuthState>().householdService;
    try {
      await svc.delete(h.id);
      if (!mounted) return;
      _load();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text(e.toString())));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Expanded(
          child: _households == null
              ? const Center(child: CircularProgressIndicator())
              : _error != null
                  ? _ErrorRetry(message: _error!, onRetry: _load)
                  : _households!.isEmpty
                      ? const _EmptyState()
                      : RefreshIndicator(
                          onRefresh: _load,
                          child: ListView.builder(
                            padding: const EdgeInsets.all(12),
                            itemCount: _households!.length,
                            itemBuilder: (context, i) =>
                                _buildHouseholdCard(_households![i]),
                          ),
                        ),
        ),
        Padding(
          padding: const EdgeInsets.all(16),
          child: SizedBox(
            width: double.infinity,
            child: FilledButton.icon(
              icon: const Icon(Icons.add_home_outlined),
              label: const Text('Crear hogar'),
              onPressed: _create,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildHouseholdCard(Household h) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.home, color: AppColors.primary),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(h.name,
                      style: const TextStyle(
                          fontSize: 16, fontWeight: FontWeight.w600)),
                ),
                PopupMenuButton<String>(
                  onSelected: (value) {
                    if (value == 'delete') _delete(h);
                  },
                  itemBuilder: (_) => const [
                    PopupMenuItem(
                      value: 'delete',
                      child: Text('Eliminar'),
                    ),
                  ],
                ),
              ],
            ),
            if (h.description != null && h.description!.isNotEmpty) ...[
              const SizedBox(height: 4),
              Text(h.description!, style: const TextStyle(color: Colors.black54)),
            ],
            const SizedBox(height: 8),
            Row(
              children: [
                Icon(Icons.group_outlined,
                    size: 18, color: Colors.grey.shade600),
                const SizedBox(width: 6),
                Text('${h.peopleCount} persona${h.peopleCount == 1 ? '' : 's'}'),
                if (h.budgetArs != null) ...[
                  const SizedBox(width: 16),
                  Icon(Icons.attach_money,
                      size: 18, color: Colors.grey.shade600),
                  Text('Presupuesto: \$${h.budgetArs!.toStringAsFixed(0)}'),
                ],
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _EmptyState extends StatelessWidget {
  const _EmptyState();

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.home_outlined, size: 64, color: Colors.black26),
          SizedBox(height: 12),
          Text('Todavía no tenés hogares'),
          SizedBox(height: 4),
          Text('Creá un hogar para compartir la despensa y el presupuesto',
              textAlign: TextAlign.center),
        ],
      ),
    );
  }
}

class _ErrorRetry extends StatelessWidget {
  const _ErrorRetry({required this.message, required this.onRetry});

  final String message;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.cloud_off, size: 48, color: Colors.black38),
            const SizedBox(height: 12),
            Text(message, textAlign: TextAlign.center),
            const SizedBox(height: 16),
            FilledButton(onPressed: onRetry, child: const Text('Reintentar')),
          ],
        ),
      ),
    );
  }
}
