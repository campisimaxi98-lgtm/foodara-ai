import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/theme.dart';
import '../models/pantry_item.dart';
import '../state/auth_state.dart';
import 'pantry_form_screen.dart';

/// Pantalla de la despensa (lista de alimentos del usuario).
class PantryScreen extends StatefulWidget {
  const PantryScreen({super.key});

  @override
  State<PantryScreen> createState() => _PantryScreenState();
}

class _PantryScreenState extends State<PantryScreen> {
  List<PantryItem>? _items;
  String? _error;
  String _filter = 'available';

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _error = null;
      _items = null;
    });
    final svc = context.read<AuthState>().pantryService;
    try {
      final items = await svc.list(status: _filter == 'all' ? null : _filter);
      if (!mounted) return;
      setState(() => _items = items);
    } catch (e) {
      if (!mounted) return;
      setState(() => _error = e.toString());
    }
  }

  Future<void> _mark(PantryItem item, String status) async {
    final svc = context.read<AuthState>().pantryService;
    try {
      await svc.markStatus(item.id, status);
      _load();
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(e.toString())));
    }
  }

  Future<void> _delete(PantryItem item) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Eliminar alimento'),
        content:
            Text('¿Eliminar ${item.foodName ?? 'este alimento'} de la despensa?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('Cancelar'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Eliminar'),
          ),
        ],
      ),
    );
    if (confirmed != true) return;

    final svc = context.read<AuthState>().pantryService;
    try {
      await svc.delete(item.id);
      if (!mounted) return;
      _load();
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(e.toString())));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
          child: _buildFilter(),
        ),
        Expanded(
          child: _items == null
              ? const Center(child: CircularProgressIndicator())
              : _error != null
                  ? _buildError()
                  : _items!.isEmpty
                      ? const _EmptyState()
                      : RefreshIndicator(
                          onRefresh: _load,
                          child: ListView.builder(
                            padding: const EdgeInsets.all(12),
                            itemCount: _items!.length,
                            itemBuilder: (context, i) =>
                                _buildItemCard(_items![i]),
                          ),
                        ),
        ),
      ],
    );
  }

  Widget _buildFilter() {
    return SegmentedButton<String>(
      segments: const [
        ButtonSegment(value: 'available', label: Text('En casa')),
        ButtonSegment(value: 'consumed', label: Text('Consumidos')),
        ButtonSegment(value: 'wasted', label: Text('Desperdicio')),
        ButtonSegment(value: 'all', label: Text('Todos')),
      ],
      selected: {_filter},
      onSelectionChanged: (sel) {
        setState(() => _filter = sel.first);
        _load();
      },
    );
  }

  Widget _buildError() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.cloud_off, size: 48, color: Colors.black38),
            const SizedBox(height: 12),
            Text(_error!, textAlign: TextAlign.center),
            const SizedBox(height: 16),
            FilledButton(onPressed: _load, child: const Text('Reintentar')),
          ],
        ),
      ),
    );
  }

  Widget _buildItemCard(PantryItem item) {
    final expired = item.expiryDate != null &&
        item.expiryDate!.isBefore(DateTime.now());

    final isWasted = item.status == 'wasted';
    final isConsumed = item.status == 'consumed';

    return Card(
      color: isWasted || isConsumed ? Colors.grey.shade100 : null,
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    item.foodName ?? 'Sin nombre',
                    style: const TextStyle(
                        fontSize: 16, fontWeight: FontWeight.w600),
                  ),
                ),
                if (isWasted)
                  const Chip(
                    label: Text('Desperdiciado'),
                    backgroundColor: Color(0xFFE57373),
                    labelStyle: TextStyle(color: Colors.white),
                  )
                else if (isConsumed)
                  const Chip(
                    label: Text('Consumido'),
                    backgroundColor: Colors.green,
                    labelStyle: TextStyle(color: Colors.white),
                  ),
              ],
            ),
            const SizedBox(height: 4),
            Row(
              children: [
                const Icon(Icons.category_outlined, size: 18),
                const SizedBox(width: 6),
                Text(item.quantityLabel),
                if (item.brand != null && item.brand!.isNotEmpty) ...[
                  const SizedBox(width: 12),
                  Text(item.brand!, style: const TextStyle(color: Colors.black54)),
                ],
              ],
            ),
            if (item.priceLabel != null) ...[
              const SizedBox(height: 4),
              Row(
                children: [
                  const Icon(Icons.attach_money, size: 18),
                  const SizedBox(width: 6),
                  Text(item.priceLabel!),
                ],
              ),
            ],
            if (item.expiryMessage != null)
              Padding(
                padding: const EdgeInsets.only(top: 6),
                child: Row(
                  children: [
                    Icon(
                      expired ? Icons.warning_amber : Icons.schedule,
                      size: 18,
                      color: expired ? AppColors.accent : Colors.black54,
                    ),
                    const SizedBox(width: 6),
                    Expanded(
                      child: Text(
                        item.expiryMessage!,
                        style: TextStyle(
                          color:
                              expired ? const Color(0xFF8A6200) : Colors.black54,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            if (!isWasted && !isConsumed) ...[
              const SizedBox(height: 8),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton.icon(
                      icon: const Icon(Icons.check_circle_outline),
                      label: const Text('Consumir'),
                      onPressed: () => _mark(item, 'consumed'),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: OutlinedButton.icon(
                      icon: const Icon(Icons.delete_outline),
                      label: const Text('Desperdiciar'),
                      style: OutlinedButton.styleFrom(
                        foregroundColor: const Color(0xFFC62828),
                      ),
                      onPressed: () => _mark(item, 'wasted'),
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.delete),
                    onPressed: () => _delete(item),
                  ),
                ],
              ),
            ],
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
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.kitchen_outlined, size: 64, color: Colors.black26),
          const SizedBox(height: 12),
          const Text('Tu despensa está vacía'),
          const SizedBox(height: 4),
          TextButton(
            onPressed: () async {
              await Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const PantryFormScreen()),
              );
            },
            child: const Text('Agregá tu primer alimento'),
          ),
        ],
      ),
    );
  }
}
