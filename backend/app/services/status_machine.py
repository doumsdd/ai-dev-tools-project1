"""Service de gestion des transitions de statut."""

# Matrice des transitions valides
VALID_TRANSITIONS = {
    "brouillon": {"envoyee", "annulee"},
    "envoyee": {"payee", "en_retard"},
    "en_retard": {"payee"},
    "payee": set(),  # Lecture seule
    "annulee": set(),  # Lecture seule
}


def validate_transition(current_status: str, target_status: str) -> bool:
    """Valide si une transition de statut est autorisée.

    Args:
        current_status: Statut actuel
        target_status: Statut cible

    Returns:
        True si la transition est valide, False sinon
    """
    if current_status not in VALID_TRANSITIONS:
        return False

    return target_status in VALID_TRANSITIONS[current_status]


def get_allowed_transitions(current_status: str) -> set[str]:
    """Retourne les transitions autorisées depuis un statut donné.

    Args:
        current_status: Statut actuel

    Returns:
        Ensemble des statuts cibles autorisés
    """
    return VALID_TRANSITIONS.get(current_status, set())
