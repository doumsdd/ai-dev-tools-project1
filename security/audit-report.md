# Rapport d'Audit de Sécurité

**Date de l'audit** : 05/10/2026  
**Outils utilisés** : bandit 1.7.10, pip-audit 2.7.3

## Méthodologie

Cet audit de sécurité est effectué en deux étapes :

1. **Analyse statique du code source** avec [bandit](https://bandit.readthedocs.io/)
   - Détecte les problèmes de sécurité courants dans le code Python
   - Analyse les patterns vulnérables (injections SQL, utilisation dangereuse de fonctions, etc.)
   - Scanne récursivement tout le dossier `backend/app/`

2. **Audit des dépendances** avec [pip-audit](https://github.com/pypa/pip-audit)
   - Vérifie les vulnérabilités connues (CVE) dans les packages Python installés
   - Consulte la base de données OSV (Open Source Vulnerabilities)
   - Analyse les fichiers `requirements.txt` et `requirements-dev.txt`

## Résultats

### Analyse statique (bandit)

```
Test results:
	No issues identified.

Code scanned:
	Total lines of code: 961
	Total lines skipped (#nosec): 0
	Total potential issues skipped due to specifically being disabled (e.g., #nosec BXXX): 0

Run metrics:
	Total issues (by severity):
		Undefined: 0
		Low: 0
		Medium: 0
		High: 0
	Total issues (by confidence):
		Undefined: 0
		Low: 0
		Medium: 0
		High: 0
```

**Statut** : ✅ Aucun problème de sécurité détecté dans le code source.

### Audit des dépendances (pip-audit)

```
Found 8 known vulnerabilities in 2 packages

Name          Version ID              Fix Versions
------------- ------- --------------- ------------
python-dotenv 1.0.1   PYSEC-2026-2270 1.2.2
starlette     0.38.6  PYSEC-2026-161  1.0.1
starlette     0.38.6  PYSEC-2026-249  1.3.1
starlette     0.38.6  PYSEC-2026-248  1.3.0
starlette     0.38.6  PYSEC-2026-1943 0.40.0
starlette     0.38.6  PYSEC-2026-1941 0.47.2
starlette     0.38.6  PYSEC-2026-2281 1.1.0
starlette     0.38.6  PYSEC-2026-2280 1.1.0
```

**Statut** : ⚠️ 8 vulnérabilités détectées dans les dépendances.

#### Actions recommandées

1. **python-dotenv** : Mettre à jour vers la version 1.2.2 ou supérieure
   ```bash
   pip install python-dotenv>=1.2.2
   ```

2. **starlette** : Mettre à jour vers la version 1.3.1 ou supérieure
   ```bash
   pip install starlette>=1.3.1
   ```
   
   Note : starlette est une dépendance de FastAPI. La mise à jour peut nécessiter de mettre à jour FastAPI également.

## Exécution locale

Pour reproduire cet audit localement :

```bash
# Installer les outils
pip install bandit pip-audit

# Lancer bandit sur le code source
cd backend
bandit -r app/ -f txt

# Lancer pip-audit sur les dépendances
pip-audit -r requirements.txt
```

## Intégration CI/CD

Ces audits sont également exécutés automatiquement dans le workflow GitHub Actions (`.github/workflows/ci.yml`) à chaque push et pull request.
