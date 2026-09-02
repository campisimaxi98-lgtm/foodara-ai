import '../core/api_client.dart';
import '../models/pantry_item.dart';
import '../models/pantry_summary.dart';

/// Servicio de despensa (FOODARA HOME) contra la API FOODARA.
class PantryService {
  PantryService(this._api);

  final ApiClient _api;

  Future<List<PantryItem>> list({String? status, String? location}) async {
    final data = await _api.request('GET', '/pantry/items', query: {
      if (status != null) 'status': status,
      if (location != null) 'location': location,
    });
    return (data as List)
        .map((e) => PantryItem.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<List<PantryItem>> expiring({int days = 7, bool includeExpired = false}) async {
    final data = await _api.request('GET', '/pantry/expiring', query: {
      'days': days,
      'include_expired': includeExpired,
    });
    return (data as List)
        .map((e) => PantryItem.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<List<PantryItem>> expired() async {
    final data = await _api.request('GET', '/pantry/expired');
    return (data as List)
        .map((e) => PantryItem.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<PantrySummary> summary() async {
    final data = await _api.request('GET', '/pantry/summary');
    return PantrySummary.fromJson(data as Map<String, dynamic>);
  }

  Future<PantryItem> add({
    required String foodName,
    required double quantity,
    required String unit,
    String? brand,
    double? priceArs,
    DateTime? expiryDate,
    String? location,
    String? notes,
  }) async {
    final data = await _api.request('POST', '/pantry/items', body: {
      'food_name': foodName,
      'quantity': quantity,
      'unit': unit,
      if (brand != null && brand.isNotEmpty) 'brand': brand,
      if (priceArs != null) 'price_ars': priceArs,
      if (expiryDate != null) 'expiry_date': expiryDate.toUtc().toIso8601String(),
      if (location != null && location.isNotEmpty) 'location': location,
      if (notes != null && notes.isNotEmpty) 'notes': notes,
    });
    return PantryItem.fromJson(data as Map<String, dynamic>);
  }

  Future<PantryItem> update(
    int id, {
    double? quantity,
    String? unit,
    String? brand,
    double? priceArs,
    DateTime? expiryDate,
    String? location,
    String? status,
    String? notes,
  }) async {
    final data = await _api.request('PATCH', '/pantry/items/$id', body: {
      if (quantity != null) 'quantity': quantity,
      if (unit != null) 'unit': unit,
      if (brand != null) 'brand': brand,
      if (priceArs != null) 'price_ars': priceArs,
      if (expiryDate != null) 'expiry_date': expiryDate.toUtc().toIso8601String(),
      if (location != null) 'location': location,
      if (status != null) 'status': status,
      if (notes != null) 'notes': notes,
    });
    return PantryItem.fromJson(data as Map<String, dynamic>);
  }

  Future<void> delete(int id) async {
    await _api.request('DELETE', '/pantry/items/$id');
  }

  Future<PantryItem> markStatus(int id, String status) async {
    final path = status == 'consumed' ? '/pantry/items/$id/consume' : '/pantry/items/$id/waste';
    final data = await _api.request('POST', path);
    return PantryItem.fromJson(data as Map<String, dynamic>);
  }
}
