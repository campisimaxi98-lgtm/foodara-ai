import 'package:intl/intl.dart';

/// Resumen determinístico de la despensa (FOODARA HOME).
class PantrySummary {
  PantrySummary({
    required this.totalItems,
    required this.itemsAvailable,
    required this.itemsConsumed,
    required this.itemsWasted,
    required this.expirySoonCount,
    required this.expiredCount,
    required this.estimatedValueArs,
    required this.estimatedExpiringValueArs,
  });

  final int totalItems;
  final int itemsAvailable;
  final int itemsConsumed;
  final int itemsWasted;
  final int expirySoonCount;
  final int expiredCount;
  final double estimatedValueArs;
  final double estimatedExpiringValueArs;

  factory PantrySummary.fromJson(Map<String, dynamic> json) {
    return PantrySummary(
      totalItems: (json['total_items'] ?? 0) as int,
      itemsAvailable: (json['items_available'] ?? 0) as int,
      itemsConsumed: (json['items_consumed'] ?? 0) as int,
      itemsWasted: (json['items_wasted'] ?? 0) as int,
      expirySoonCount: (json['expiry_soon_count'] ?? 0) as int,
      expiredCount: (json['expired_count'] ?? 0) as int,
      estimatedValueArs: (json['estimated_value_ars'] as num? ?? 0).toDouble(),
      estimatedExpiringValueArs:
          (json['estimated_expiring_value_ars'] as num? ?? 0).toDouble(),
    );
  }

  String get valueLabel {
    final format = NumberFormat.currency(
        symbol: r'$', decimalDigits: 0, locale: 'es_AR');
    return format.format(estimatedValueArs);
  }
}
