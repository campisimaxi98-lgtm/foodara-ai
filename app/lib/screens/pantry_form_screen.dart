import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/pantry_item.dart';
import '../state/auth_state.dart';

/// Formulario para agregar un alimento a la despensa.
class PantryFormScreen extends StatefulWidget {
  const PantryFormScreen({super.key, this.item});

  /// Si se provee, el formulario edita el item existente.
  final PantryItem? item;

  @override
  State<PantryFormScreen> createState() => _PantryFormScreenState();
}

class _PantryFormScreenState extends State<PantryFormScreen> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _nameController;
  late final TextEditingController _qtyController;
  late final TextEditingController _unitController;
  late final TextEditingController _brandController;
  late final TextEditingController _priceController;
  late final TextEditingController _locationController;
  late final TextEditingController _notesController;

  DateTime? _expiryDate;
  bool _saving = false;

  @override
  void initState() {
    super.initState();
    final item = widget.item;
    _nameController = TextEditingController(text: item?.foodName ?? '');
    _qtyController = TextEditingController(
        text: item != null ? _qty(item.quantity) : '1');
    _unitController = TextEditingController(text: item?.unit ?? 'u');
    _brandController = TextEditingController(text: item?.brand ?? '');
    _priceController = TextEditingController(
        text: item?.priceArs != null ? item!.priceArs.toString() : '');
    _locationController = TextEditingController(text: item?.location ?? '');
    _notesController = TextEditingController(text: item?.notes ?? '');
    _expiryDate = item?.expiryDate;
  }

  static String _qty(double q) =>
      q == q.roundToDouble() ? q.toStringAsFixed(0) : q.toString();

  @override
  void dispose() {
    _nameController.dispose();
    _qtyController.dispose();
    _unitController.dispose();
    _brandController.dispose();
    _priceController.dispose();
    _locationController.dispose();
    _notesController.dispose();
    super.dispose();
  }

  Future<void> _pickExpiry() async {
    final now = DateTime.now();
    final picked = await showDatePicker(
      context: context,
      initialDate: _expiryDate ?? now.add(const Duration(days: 7)),
      firstDate: now.subtract(const Duration(days: 30)),
      lastDate: now.add(const Duration(days: 365 * 3)),
    );
    if (picked != null) {
      setState(() => _expiryDate = picked);
    }
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _saving = true);
    final svc = context.read<AuthState>().pantryService;
    final foodName = _nameController.text.trim();
    final quantity = double.parse(_qtyController.text.trim());
    final unit = _unitController.text.trim();
    final price = double.tryParse(_priceController.text.replaceAll(',', '.'));

    try {
      if (widget.item == null) {
        await svc.add(
          foodName: foodName,
          quantity: quantity,
          unit: unit,
          brand: _brandController.text.trim(),
          priceArs: price,
          expiryDate: _expiryDate,
          location: _locationController.text.trim(),
          notes: _notesController.text.trim(),
        );
      } else {
        await svc.update(
          widget.item!.id,
          quantity: quantity,
          unit: unit,
          brand: _brandController.text.trim(),
          priceArs: price,
          expiryDate: _expiryDate,
          location: _locationController.text.trim(),
          notes: _notesController.text.trim(),
        );
      }

      if (!mounted) return;
      Navigator.of(context).pop(true);
    } catch (e) {
      setState(() => _saving = false);
      if (mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text(e.toString())));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final isEdit = widget.item != null;

    return Scaffold(
      appBar: AppBar(title: Text(isEdit ? 'Editar alimento' : 'Agregar alimento')),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                TextFormField(
                  controller: _nameController,
                  decoration: const InputDecoration(
                    labelText: 'Alimento *',
                    hintText: 'Ej: Leche Entera',
                    prefixIcon: Icon(Icons.restaurant_outlined),
                  ),
                  validator: (v) =>
                      (v == null || v.trim().isEmpty) ? 'Requerido' : null,
                ),
                const SizedBox(height: 16),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(
                      flex: 2,
                      child: TextFormField(
                        controller: _qtyController,
                        keyboardType:
                            const TextInputType.numberWithOptions(decimal: true),
                        decoration: const InputDecoration(
                          labelText: 'Cantidad *',
                          prefixIcon: Icon(Icons.numbers),
                        ),
                        validator: (v) {
                          final d = double.tryParse((v ?? '').trim());
                          if (d == null || d <= 0) {
                            return 'Cantidad inválida';
                          }
                          return null;
                        },
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      flex: 2,
                      child: TextFormField(
                        controller: _unitController,
                        decoration: const InputDecoration(
                          labelText: 'Unidad *',
                          hintText: 'u, kg, g, L',
                        ),
                        validator: (v) => (v == null || v.trim().isEmpty)
                            ? 'Requerido'
                            : null,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(
                      child: TextFormField(
                        controller: _brandController,
                        decoration: const InputDecoration(
                          labelText: 'Marca',
                          prefixIcon: Icon(Icons.local_offer_outlined),
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: TextFormField(
                        controller: _priceController,
                        keyboardType:
                            const TextInputType.numberWithOptions(decimal: true),
                        decoration: const InputDecoration(
                          labelText: 'Precio (\$)',
                          prefixIcon: Icon(Icons.attach_money),
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _locationController,
                  decoration: const InputDecoration(
                    labelText: 'Ubicación',
                    hintText: 'Ej: heladera, alacena',
                    prefixIcon: Icon(Icons.location_on_outlined),
                  ),
                ),
                const SizedBox(height: 16),
                InkWell(
                  onTap: _pickExpiry,
                  child: InputDecorator(
                    decoration: const InputDecoration(
                      labelText: 'Fecha de vencimiento',
                      prefixIcon: Icon(Icons.event_outlined),
                      suffixIcon: Icon(Icons.calendar_today),
                    ),
                    child: Text(
                      _expiryDate == null
                          ? 'Seleccionar fecha'
                          : '${_expiryDate!.day}/${_expiryDate!.month}/${_expiryDate!.year}',
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _notesController,
                  maxLines: 2,
                  decoration: const InputDecoration(
                    labelText: 'Notas',
                    prefixIcon: Icon(Icons.notes),
                  ),
                ),
                const SizedBox(height: 24),
                FilledButton(
                  onPressed: _saving ? null : _save,
                  child: _saving
                      ? const SizedBox(
                          width: 22,
                          height: 22,
                          child: CircularProgressIndicator(
                              color: Colors.white, strokeWidth: 2),
                        )
                      : Text(isEdit ? 'Guardar cambios' : 'Agregar a la despensa'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
