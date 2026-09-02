import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/theme.dart';
import '../models/pantry_item.dart';
import '../models/pantry_summary.dart';
import '../state/auth_state.dart';

/// Pantalla de resumen: métricas determinísticas de la despensa.
class SummaryScreen extends StatefulWidget {
  const SummaryScreen({super.key});

  @override
  State<SummaryScreen> createState() => _SummaryScreenState();
}

class _SummaryScreenState extends State<SummaryScreen> {
  PantrySummary? _summary;
  List<PantryItem>? _expiring;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _error = null;
      _summary = null;
    });
    final svc = context.read<AuthState>().pantryService;
    try {
      final summary = await svc.summary();
      final expiring = await svc.expiring(days: 7, includeExpired: true);
      if (!mounted) return;
      setState(() {
        _summary = summary;
        _expiring = expiring;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _error = e.toString());
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_error != null) {
      return _ErrorRetry(message: _error!, onRetry: _load);
    }
    if (_summary == null) {
      return const Center(child: CircularProgressIndicator());
    }

    final s = _summary!;
    return RefreshIndicator(
      onRefresh: _load,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _MetricCard(
            label: 'Valor estimado',
            value: s.valueLabel,
            icon: Icons.attach_money,
            color: AppColors.primary,
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: _MetricCard(
                  label: 'En casa',
                  value: '${s.itemsAvailable}',
                  icon: Icons.kitchen,
                  color: Colors.blue,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _MetricCard(
                  label: 'Vencen pronto',
                  value: '${s.expirySoonCount}',
                  icon: Icons.timer,
                  color: AppColors.accent,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: _MetricCard(
                  label: 'Vencidos',
                  value: '${s.expiredCount}',
                  icon: Icons.warning_amber,
                  color: const Color(0xFFC62828),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _MetricCard(
                  label: 'Desperdiciados',
                  value: '${s.itemsWasted}',
                  icon: Icons.delete_outline,
                  color: const Color(0xFF6D4C41),
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),
          Text(
            'Próximos a vencer',
            style: Theme.of(context)
                .textTheme
                .titleMedium
                ?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          if (_expiring == null)
            const Padding(
              padding: EdgeInsets.all(16),
              child: Center(child: CircularProgressIndicator()),
            )
          else if (_expiring!.isEmpty)
            const Card(
              child: Padding(
                padding: EdgeInsets.all(20),
                child: Text('Sin productos próximos a vencer. ¡Bien!'),
              ),
            )
          else
            ..._expiring!.map((item) => _ExpiringTile(item: item)),
        ],
      ),
    );
  }
}

class _MetricCard extends StatelessWidget {
  const _MetricCard({
    required this.label,
    required this.value,
    required this.icon,
    required this.color,
  });

  final String label;
  final String value;
  final IconData icon;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: color, size: 28),
            const SizedBox(height: 8),
            Text(value,
                style:
                    const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            Text(label, style: const TextStyle(color: Colors.black54)),
          ],
        ),
      ),
    );
  }
}

class _ExpiringTile extends StatelessWidget {
  const _ExpiringTile({required this.item});

  final PantryItem item;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: const Icon(Icons.fastfood_outlined),
        title: Text(item.foodName ?? 'Ítem'),
        subtitle: Text(item.expiryMessage ?? ''),
        trailing: Text(
          item.quantityLabel,
          style: const TextStyle(fontWeight: FontWeight.w600),
        ),
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
