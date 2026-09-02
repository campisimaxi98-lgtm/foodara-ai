import '../core/api_client.dart';
import '../models/household.dart';

/// Servicio de hogares (FOODARA HOME) contra la API FOODARA.
class HouseholdService {
  HouseholdService(this._api);

  final ApiClient _api;

  Future<List<Household>> listMine() async {
    final data = await _api.request('GET', '/households/my');
    return (data as List)
        .map((e) => Household.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<Household> create({
    required String name,
    String? description,
    double? budgetArs,
    int peopleCount = 1,
  }) async {
    final data = await _api.request('POST', '/households', body: {
      'name': name,
      if (description != null && description.isNotEmpty) 'description': description,
      if (budgetArs != null) 'budget_ars': budgetArs,
      'people_count': peopleCount,
    });
    return Household.fromJson(data as Map<String, dynamic>);
  }

  Future<Household> update(
    int id, {
    String? name,
    String? description,
    double? budgetArs,
    int? peopleCount,
    bool? isActive,
  }) async {
    final data = await _api.request('PATCH', '/households/$id', body: {
      if (name != null) 'name': name,
      if (description != null) 'description': description,
      if (budgetArs != null) 'budget_ars': budgetArs,
      if (peopleCount != null) 'people_count': peopleCount,
      if (isActive != null) 'is_active': isActive,
    });
    return Household.fromJson(data as Map<String, dynamic>);
  }

  Future<void> delete(int id) async {
    await _api.request('DELETE', '/households/$id');
  }
}
