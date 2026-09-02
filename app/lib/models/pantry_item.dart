import 'package:intl/intl.dart';

/// Item de la despensa digital (FOODARA HOME).
class PantryItem {
  PantryItem({
    required this.id,
    required this.foodName,
    required this.quantity,
    required this.unit,
    required this.status,
    this.brand,
    this.priceArs,
    this.expiryDate,
    this.location,
    this.notes,
  });

  final int id;
  final String? foodName;
  final double quantity;
  final String unit;
  final String status; // available | consumed | wasted
  final String? brand;
  final double? priceArs;
  final DateTime? expiryDate;
  final String? location;
  final String? notes;

  factory PantryItem.fromJson(Map<String, dynamic> json) {
    return PantryItem(
      id: json['id'] as int,
      foodName: json['food_name'] as String?,
      quantity: (json['quantity'] as num).toDouble(),
      unit: json['unit'] as String,
      status: (json['status'] ?? 'available') as String,
      brand: json['brand'] as String?,
      priceArs: (json['price_ars'] as num?)?.toDouble(),
      expiryDate: _parseDate(json['expiry_date'] as String?),
      location: json['location'] as String?,
      notes: json['notes'] as String?,
    );
  }

  static DateTime? _parseDate(String? raw) {
    if (raw == null || raw.isEmpty) return null;
    final parsed = DateTime.tryParse(raw);
    if (parsed == null) return null;
    return parsed.toLocal();
  }

  /// Mensaje amigable sobre el vencimiento:
  /// "El yogur vence en 2 días" / "El pan venció hace 3 días" / null si no vence.
  String? get expiryMessage {
    final date = expiryDate;
    if (date == null) return null;

    final now = DateTime.now();
    final diff = date.difference(now).inDays;

    if (diff < 0) {
      return '${foodName ?? 'Ítem'} venció hace ${diff.abs()} día${diff.abs() == 1 ? '' : 's'}';
    }
    if (diff == 0) return '${foodName ?? 'Ítem'} vence hoy';
    if (diff == 1) return '${foodName ?? 'Ítem'} vence mañana';
    return '${foodName ?? 'Ítem'} vence en $diff días';
  }

  String get quantityLabel {
    final q = quantity.toStringAsFixed(quantity == quantity.round() ? 0 : 2);
    return '$q $unit';
  }

  String? get priceLabel {
    final p = priceArs;
    if (p == null || p <= 0) return null;
    final format = NumberFormat.currency(symbol: r'$', decimalDigits: 2, locale: 'es_AR');
    return format.format(p);
  }
}
