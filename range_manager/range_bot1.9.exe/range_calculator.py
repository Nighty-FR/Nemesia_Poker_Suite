# range_calculator.py

from range_data import RANGES

TOTAL_COMBINATIONS = 1326


def calculate_combinations(hands):
    """Calcule le nombre total de combinaisons pour un ensemble de mains."""
    total = 0
    for hand in hands:
        if len(hand) == 2:  # Paires
            total += 6
        elif hand.endswith("s"):  # Suited
            total += 4
        else:  # Offsuit
            total += 12
    return total


def calculate_percentage(hands):
    """Calcule le pourcentage des mains jouées."""
    total_combinations = calculate_combinations(hands)
    return (total_combinations / TOTAL_COMBINATIONS) * 100


def interpolate_ranges(lower_percentage, upper_percentage, target_percentage):
    """Interpole les mains entre deux pourcentages connus pour atteindre un pourcentage cible."""
    lower_hands = set(RANGES[lower_percentage])
    upper_hands = set(RANGES[upper_percentage])

    # Mains supplémentaires nécessaires pour interpoler
    total_combinations_lower = calculate_combinations(lower_hands)
    total_combinations_target = int((target_percentage / 100) * TOTAL_COMBINATIONS)

    additional_combinations_needed = total_combinations_target - total_combinations_lower

    # Ajouter des mains du range supérieur jusqu'à atteindre le nombre nécessaire de combinaisons
    additional_hands = []
    for hand in upper_hands - lower_hands:
        weight = 6 if len(hand) == 2 else 4 if hand.endswith("s") else 12
        if calculate_combinations(lower_hands | set(additional_hands)) + weight > total_combinations_target:
            break
        additional_hands.append(hand)

    return lower_hands | set(additional_hands)


def get_hands_for_percentage(percentage):
    """Retourne les mains correspondant au pourcentage donné."""
    if percentage in RANGES:
        return set(RANGES[percentage])

    # Déterminer les bornes connues pour interpolation
    lower_bound = max(p for p in RANGES if p < percentage)
    upper_bound = min(p for p in RANGES if p > percentage)

    # Interpoler les mains entre les bornes
    return interpolate_ranges(lower_bound, upper_bound, percentage)
