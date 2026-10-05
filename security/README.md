# Sécurité

Ce dossier contient les rapports et configurations liés à la sécurité du projet.

## Outils d'audit

### bandit - Analyse statique du code

[bandit](https://bandit.readthedocs.io/) est un outil d'analyse statique qui détecte les problèmes de sécurité courants dans le code Python.

**Exécution locale** :
```bash
cd backend
bandit -r app/ -f txt
```

### pip-audit - Audit des dépendances

[pip-audit](https://github.com/pypa/pip-audit) vérifie les vulnérabilités connues (CVE) dans les packages Python installés.

**Exécution locale** :
```bash
cd backend
pip-audit -r requirements.txt
```

## Fichiers

- `audit-report.md` : Rapport complet d'audit de sécurité avec méthodologie et résultats
- `bandit-output.txt` : Sortie brute de bandit (générée par CI)
- `pip-audit-output.txt` : Sortie brute de pip-audit (générée par CI)

## Intégration CI/CD

Les audits sont exécutés automatiquement à chaque push et pull request via GitHub Actions (`.github/workflows/ci.yml`).

Le workflow :
1. Installe les dépendances de développement (bandit, pip-audit)
2. Exécute bandit sur le code source
3. Exécute pip-audit sur les dépendances
4. Upload les résultats comme artifacts

## Installation des outils

Les outils de sécurité sont inclus dans `requirements-dev.txt` :

```bash
pip install -r backend/requirements-dev.txt
```

## Bonnes pratiques

1. **Exécuter les audits régulièrement** : Avant chaque release et périodiquement
2. **Corriger les vulnérabilités rapidement** : Mettre à jour les packages dès qu'une version corrigée est disponible
3. **Surveiller les nouvelles vulnérabilités** : Consulter les bases de données CVE régulièrement
4. **Minimiser les dépendances** : Moins de packages = moins de surface d'attaque
