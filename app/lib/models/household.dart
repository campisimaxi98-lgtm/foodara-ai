// Modelo de hogar (FOODARA HOME) devuelto por la API.

class HouseholdMember {
  HouseholdMember({
    required this.id,
    required this.userId,
    required this.role,
  });

  final int id;
  final int userId;
  final String role;

  factory HouseholdMember.fromJson(Map<String, dynamic> json) {
    return HouseholdMember(
      id: json['id'] as int,
      userId: json['user_id'] as int,
      role: json['role'] as String,
    );
  }
}

class Household {
  Household({
    required this.id,
    required this.name,
    this.description,
    this.budgetArs,
    this.currency = 'ARS',
    this.peopleCount = 1,
    this.isActive = true,
    this.members = const [],
  });

  final int id;
  final String name;
  final String? description;
  final double? budgetArs;
  final String currency;
  final int peopleCount;
  final bool isActive;
  final List<HouseholdMember> members;

  factory Household.fromJson(Map<String, dynamic> json) {
    return Household(
      id: json['id'] as int,
      name: json['name'] as String,
      description: json['description'] as String?,
      budgetArs: (json['budget_ars'] as num?)?.toDouble(),
      currency: (json['currency'] ?? 'ARS') as String,
      peopleCount: (json['people_count'] ?? 1) as int,
      isActive: (json['is_active'] ?? true) as bool,
      members: ((json['members'] ?? []) as List)
          .map((e) => HouseholdMember.fromJson(e as Map<String, dynamic>))
          .toList(),
    );
  }
}
