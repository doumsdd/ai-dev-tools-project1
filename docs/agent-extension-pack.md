# Guide d'extension pour agents IA

Ce document explique comment les agents IA (Cline, Claude, GPT, etc.) peuvent utiliser les outils de validation du projet guestBTP pour éviter les erreurs.

## Introduction

Les agents IA peuvent commettre des erreurs de calcul ("hallucinations") lors de la création de factures. Ce projet fournit des outils pour valider automatiquement les calculs avant d'accepter une opération.

## Outil de validation mathématique

### Emplacement

```
agent-capabilities/validate_invoice_math.py
```

### Fonctionnement

Le script :
1. Lit un JSON représentant une facture
2. Recalcule tous les totaux (HT, TVA, TTC)
3. Compare avec les valeurs déclarées
4. Retourne un rapport détaillé avec code de sortie

### Utilisation par un agent IA

#### Méthode 1 : Validation avant soumission API

Avant d'appeler l'API pour créer une facture, l'agent doit :

```python
# 1. Construire la facture
invoice_data = {
    "client_id": 1,
    "issue_date": "2026-10-05",
    "lines": [
        {
            "description": "Pose de briques",
            "category": "maconnerie",
            "quantity": 10,
            "unit": "m2",
            "unit_price": 100.00,
            "vat_rate": 20,
            "discount": 0
        }
    ]
}

# 2. Valider avec le script
import subprocess
import json

validation_input = {
    "lines": invoice_data["lines"],
    "subtotal_ht": 1000.00,
    "total_vat": 200.00,
    "total_ttc": 1200.00
}

result = subprocess.run(
    ["python", "agent-capabilities/validate_invoice_math.py", "--json"],
    input=json.dumps(validation_input),
    capture_output=True,
    text=True
)

# 3. Vérifier le résultat
if result.returncode == 0:
    # Validation réussie, on peut soumettre à l'API
    response = requests.post("/api/v1/invoices", json=invoice_data)
else:
    # Erreur de calcul, corriger avant de soumettre
    print("Erreur de validation:", result.stdout)
```

#### Méthode 2 : Hook pre-commit

Créer un hook git qui valide automatiquement les factures avant commit :

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Chercher les fichiers JSON de factures modifiés
for file in $(git diff --cached --name-only | grep -E 'invoices/.*\.json$'); do
    echo "Validation de $file..."
    python agent-capabilities/validate_invoice_math.py "$file"
    if [ $? -ne 0 ]; then
        echo "❌ Validation échouée pour $file"
        exit 1
    fi
done

exit 0
```

Rendre le hook exécutable :
```bash
chmod +x .git/hooks/pre-commit

### Intégration avec le backend FastAPI

Le backend peut appeler le validateur comme middleware :

```python
# backend/app/middleware/invoice_validator.py
import subprocess
import json
from fastapi import HTTPException

def validate_invoice_math(invoice_data: dict) -> None:
    """Valide les calculs mathématiques d'une facture."""
    validation_input = {
        "lines": invoice_data["lines"],
        "subtotal_ht": invoice_data.get("subtotal_ht"),
        "total_vat": invoice_data.get("total_vat"),
        "total_ttc": invoice_data.get("total_ttc"),
    }
    
    result = subprocess.run(
        ["python", "agent-capabilities/validate_invoice_math.py", "--json"],
        input=json.dumps(validation_input),
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise HTTPException(
            status_code=400,
            detail=f"Erreur de calcul: {result.stdout}"
        )
```

### Intégration avec le frontend React

Le frontend peut valider avant l'envoi :

```typescript
// frontend/src/api/validateInvoice.ts
import { calculateTotal } from './client';

export async function validateInvoiceBeforeSubmit(lines: InvoiceLineCreate[]) {
  // Calculer les totaux avec la fonction centralisée
  const totals = calculateTotal(lines);
  
  return {
    lines,
    subtotal_ht: totals.subtotal_ht,
    total_vat: totals.total_vat,
    total_ttc: totals.total_ttc,
  };
}
```

## Bonnes pratiques pour les agents IA

### 1. Toujours valider avant de soumettre

```
❌ MAUVAIS : Créer une facture sans validation
✅ BON : Valider avec validate_invoice_math.py avant l'appel API
```

### 2. Utiliser les fonctions de calcul centralisées

```
❌ MAUVAIS : Calculer les totaux manuellement
✅ BON : Utiliser calculateTotal() (frontend) ou calculate_invoice_totals() (backend)
```

### 3. Vérifier les taux de TVA

```
❌ MAUVAIS : Utiliser vat_rate: 15
✅ BON : Utiliser uniquement 5.5, 10, ou 20
```

### 4. Gérer les erreurs de validation

```python
result = validate_invoice(data)
if not result["valid"]:
    for error in result["errors"]:
        print(f"Erreur: {error}")
    # Corriger les erreurs avant de réessayer
```

## Scénarios d'utilisation

### Scénario 1 : Agent IA crée une facture

```
1. Agent reçoit : "Créer une facture pour le client 1, 10m² de briques à 100€/m²"
2. Agent construit le JSON de la facture
3. Agent exécute : python validate_invoice_math.py invoice.json
4. Si validation OK → agent appelle POST /api/v1/invoices
5. Si validation KO → agent corrige les calculs et recommence
```

### Scénario 2 : Agent IA modifie une facture

```
1. Agent reçoit : "Ajouter une remise de 10% sur la facture FA-2026-0001"
2. Agent récupère la facture existante
3. Agent modifie les lignes avec la remise
4. Agent recalcule les totaux
5. Agent valide avec validate_invoice_math.py
6. Si OK → agent appelle PATCH /api/v1/invoices/1
```

## Dépannage

### Erreur : "vat_rate doit être 5.5, 10, ou 20"

```json
// ❌ Incorrect
{ "vat_rate": 15 }

// ✅ Correct
{ "vat_rate": 20 }
```

### Erreur : "subtotal_ht déclaré (900) != calculé (1000)"

L'agent a mal calculé le total. Le script fournit la valeur correcte à utiliser.

## Ressources

- **Script de validation** : `agent-capabilities/validate_invoice_math.py`
- **Documentation du script** : `agent-capabilities/README.md`
- **Règles du projet** : `AGENTS.md`
- **Calculs backend** : `backend/app/services/invoice_calculator.py`
- **Calculs frontend** : `frontend/src/api/client.ts`

```

#### Méthode 3 : Custom Tool pour Cline

Cline peut utiliser cet outil comme un "custom tool" dans son workflow :

```markdown
# Dans CLAUDE.md ou les instructions de l'agent

## Validation de facture

Avant de créer une facture via l'API :

1. Construire le JSON de la facture
2. Exécuter : `python agent-capabilities/validate_invoice_math.py --json < invoice.json`
3. Si le code de sortie est 0, soumettre à l'API
4. Si le code de sortie est 1, corriger les erreurs et recommencer
```
