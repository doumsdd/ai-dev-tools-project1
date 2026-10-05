# Agent Capabilities

Outils et scripts pour aider les agents IA à travailler avec le projet guestBTP.

## validate_invoice_math.py

Validateur mathématique de factures qui protège contre les erreurs de calcul des agents IA.

### Usage

```bash
# Depuis stdin
cat invoice.json | python validate_invoice_math.py

# Depuis un fichier
python validate_invoice_math.py invoice.json

# Avec détail des lignes
python validate_invoice_math.py --pretty invoice.json

# Avec sortie JSON
python validate_invoice_math.py --json invoice.json
```

### Format JSON attendu

```json
{
  "lines": [
    {
      "description": "Pose de briques",
      "quantity": 10,
      "unit_price": 100.00,
      "vat_rate": 20,
      "discount": 0
    }
  ],
  "subtotal_ht": 1000.00,
  "total_vat": 200.00,
  "total_ttc": 1200.00
}
```

### Règles de validation

- **Taux de TVA** : uniquement 5.5, 10, ou 20
- **Quantité et prix** : doivent être > 0
- **Remise** : entre 0 et 100
- **Calculs** :
  - Ligne HT = quantity × unit_price × (1 - discount/100)
  - TVA ligne = line_ht × vat_rate / 100
  - Total HT = somme des lignes HT
  - Total TVA = somme des TVA
  - Total TTC = Total HT + Total TVA

### Code de sortie

- `0` : Validation réussie
- `1` : Erreur de validation ou de format

### Intégration

Voir `docs/agent-extension-pack.md` pour l'intégration avec les agents IA.
