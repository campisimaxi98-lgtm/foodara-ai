import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state/auth_state.dart';

/// Formulario para crear un hogar (FOODARA HOME).
class HouseholdFormScreen extends StatefulWidget {
  const HouseholdFormScreen({super.key});

  @override
  State<HouseholdFormScreen> createState() => _HouseholdFormScreenState();
}

class _HouseholdFormScreenState extends State<HouseholdFormScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _descriptionController = TextEditingController();
  final _budgetController = TextEditingController();
  final _peopleController = TextEditingController(text: '2');
  bool _saving = false;

  @override
  void dispose() {
    _nameController.dispose();
    _descriptionController.dispose();
    _budgetController.dispose();
    _peopleController.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _saving = true);
    final svc = context.read<AuthState>().householdService;
    try {
      await svc.create(
        name: _nameController.text.trim(),
        description: _descriptionController.text.trim(),
        budgetArs: double.tryParse(_budgetController.text.replaceAll(',', '.')),
        peopleCount: int.tryParse(_peopleController.text.trim()) ?? 1,
      );
      if (!mounted) return;
      Navigator.pop(context, true);
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
    return Scaffold(
      appBar: AppBar(title: const Text('Crear hogar')),
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
                    labelText: 'Nombre del hogar *',
                    hintText: 'Ej: Casa Campisi',
                    prefixIcon: Icon(Icons.home_outlined),
                  ),
                  validator: (v) =>
                      (v == null || v.trim().isEmpty) ? 'Requerido' : null,
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _descriptionController,
                  maxLines: 2,
                  decoration: const InputDecoration(
                    labelText: 'Descripción',
                    prefixIcon: Icon(Icons.description_outlined),
                  ),
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(
                      child: TextFormField(
                        controller: _budgetController,
                        keyboardType:
                            const TextInputType.numberWithOptions(decimal: true),
                        decoration: const InputDecoration(
                          labelText: 'Presupuesto mensual (\$)',
                          prefixIcon: Icon(Icons.attach_money),
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: TextFormField(
                        controller: _peopleController,
                        keyboardType: TextInputType.number,
                        decoration: const InputDecoration(
                          labelText: 'Personas',
                          prefixIcon: Icon(Icons.group_outlined),
                        ),
                        validator: (v) {
                          final n = int.tryParse((v ?? '').trim());
                          if (n == null || n < 1 || n > 100) {
                            return '1-100';
                          }
                          return null;
                        },
                      ),
                    ),
                  ],
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
                      : const Text('Crear hogar'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
