#!/usr/bin/env python3
"""Validateur mathématique de factures pour guestBTP.

Protège contre les hallucinations de calcul des agents IA en vérifiant
que les totaux HT, TVA et TTC d'une facture sont mathématiquement corrects.

Usage:
    python validate_invoice_math.py < invoice.json
    python validate_invoice_math.py invoice.json
    python validate_invoice_math.py --pretty invoice.json

Code de sortie:
    0 - Validation réussie
    1 - Erreur de validation ou de format
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any

TWO_PLACES = Decimal("0.01")
VALID_VAT_RATES = {Decimal("5.5"), Decimal("10"), Decimal("20")}


def to_decimal(value: Any, field_name: str = "value") -> Decimal:
    """Convertit une valeur en Decimal de manière sécurisée."""
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as e:
        raise ValueError(f"Valeur invalide pour '{field_name}': {value}") from e


def quantize(value: Decimal) -> Decimal:
    """Arrondit à 2 décimales."""
    return value.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


def calculate_line_ht(quantity: Decimal, unit_price: Decimal, discount: Decimal) -> Decimal:
    """Calcule le total HT d'une ligne.

    Formule: quantity × unit_price × (1 - discount/100)
    """
    subtotal = quantity * unit_price
    if discount > 0:
        subtotal = subtotal * (1 - discount / 100)
    return quantize(subtotal)


def calculate_line_vat(line_ht: Decimal, vat_rate: Decimal) -> Decimal:
    """Calcule la TVA d'une ligne."""
    return quantize(line_ht * vat_rate / 100)



def validate_invoice(data: dict[str, Any]) -> dict[str, Any]:
    """Valide les calculs mathématiques d'une facture."""
    errors: list[str] = []
    warnings: list[str] = []

    if "lines" not in data:
        return {"valid": False, "errors": ["Champ 'lines' manquant"], "warnings": []}
    if not isinstance(data["lines"], list):
        return {"valid": False, "errors": ["'lines' doit être une liste"], "warnings": []}
    if len(data["lines"]) == 0:
        return {"valid": False, "errors": ["Au moins une ligne est requise"], "warnings": []}

    line_results = []
    expected_subtotal_ht = Decimal("0")
    expected_total_vat = Decimal("0")

    for i, line in enumerate(data["lines"]):
        line_num = i + 1
        line_errors = []

        for field in ("quantity", "unit_price", "vat_rate"):
            if field not in line:
                line_errors.append(f"Ligne {line_num}: champ '{field}' manquant")

        if line_errors:
            errors.extend(line_errors)
            continue

        try:
            quantity = to_decimal(line["quantity"], f"ligne {line_num}.quantity")
            unit_price = to_decimal(line["unit_price"], f"ligne {line_num}.unit_price")
            vat_rate = to_decimal(line["vat_rate"], f"ligne {line_num}.vat_rate")
            discount = to_decimal(line.get("discount", 0), f"ligne {line_num}.discount")
        except ValueError as e:
            errors.append(str(e))
            continue

        if quantity <= 0:
            errors.append(f"Ligne {line_num}: quantity doit être > 0 (got {quantity})")
        if unit_price <= 0:
            errors.append(f"Ligne {line_num}: unit_price doit être > 0 (got {unit_price})")
        if vat_rate not in VALID_VAT_RATES:
            errors.append(f"Ligne {line_num}: vat_rate doit être 5.5, 10, ou 20 (got {vat_rate})")
        if discount < 0 or discount > 100:
            errors.append(f"Ligne {line_num}: discount doit être entre 0 et 100 (got {discount})")

        line_ht = calculate_line_ht(quantity, unit_price, discount)
        line_vat = calculate_line_vat(line_ht, vat_rate)
        expected_subtotal_ht += line_ht
        expected_total_vat += line_vat

        if "total_ht" in line:
            declared_ht = to_decimal(line["total_ht"], f"ligne {line_num}.total_ht")
            if quantize(declared_ht) != line_ht:
                errors.append(
                    f"Ligne {line_num}: total_ht déclaré ({declared_ht}) != calculé ({line_ht})"
                )

        line_results.append({
            "line": line_num, "description": line.get("description", ""),
            "quantity": str(quantity), "unit_price": str(unit_price),
            "discount": str(discount), "vat_rate": str(vat_rate),
            "ht": str(line_ht), "vat": str(line_vat),
        })

    expected_subtotal_ht = quantize(expected_subtotal_ht)
    expected_total_vat = quantize(expected_total_vat)
    expected_total_ttc = quantize(expected_subtotal_ht + expected_total_vat)

    actual = {}
    expected = {
        "subtotal_ht": str(expected_subtotal_ht),
        "total_vat": str(expected_total_vat),
        "total_ttc": str(expected_total_ttc),
    }

    for field in ("subtotal_ht", "total_vat", "total_ttc"):
        if field in data:
            declared = to_decimal(data[field], field)
            actual[field] = str(quantize(declared))
            if quantize(declared) != quantize(Decimal(expected[field])):
                errors.append(f"{field} déclaré ({actual[field]}) != calculé ({expected[field]})")
        else:
            warnings.append(f"{field} non déclaré, valeur calculée: {expected[field]}")

    return {
        "valid": len(errors) == 0, "errors": errors, "warnings": warnings,
        "expected": expected, "actual": actual, "lines": line_results,
    }



def format_report(result: dict[str, Any], pretty: bool = False) -> str:
    """Formate le rapport de validation."""
    lines = []
    if result["valid"]:
        lines.append("✅ VALIDATION RÉUSSIE")
    else:
        lines.append("❌ VALIDATION ÉCHOUÉE")
    lines.append("")

    if result["errors"]:
        lines.append(f"Erreurs ({len(result['errors'])}) :")
        for err in result["errors"]:
            lines.append(f"  • {err}")
        lines.append("")

    if result["warnings"]:
        lines.append(f"Avertissements ({len(result['warnings'])}) :")
        for warn in result["warnings"]:
            lines.append(f"  ⚠ {warn}")
        lines.append("")

    lines.append("Totaux calculés :")
    lines.append(f"  Subtotal HT : {result['expected']['subtotal_ht']} €")
    lines.append(f"  Total TVA   : {result['expected']['total_vat']} €")
    lines.append(f"  Total TTC   : {result['expected']['total_ttc']} €")

    if pretty and result.get("lines"):
        lines.append("")
        lines.append("Détail par ligne :")
        lines.append("-" * 80)
        for line in result["lines"]:
            lines.append(f"  Ligne {line['line']}: {line['description']}")
            lines.append(
                f"    {line['quantity']} × {line['unit_price']} €"
                f" (remise {line['discount']}%) = {line['ht']} € HT"
            )
            lines.append(f"    TVA {line['vat_rate']}% = {line['vat']} €")
        lines.append("-" * 80)

    return "\n".join(lines)


def main() -> int:
    """Point d'entrée principal."""
    args = sys.argv[1:]
    pretty = "--pretty" in args
    json_output = "--json" in args
    args = [a for a in args if a not in ("--pretty", "--json")]

    try:
        if args:
            path = Path(args[0])
            if not path.exists():
                print(f"Erreur: fichier '{args[0]}' introuvable", file=sys.stderr)
                return 1
            data = json.loads(path.read_text(encoding="utf-8"))
        else:
            if sys.stdin.isatty():
                print("Usage: validate_invoice_math.py [--pretty] [--json] [file.json]",
                      file=sys.stderr)
                return 1
            data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Erreur JSON: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
        return 1

    result = validate_invoice(data)
    print(format_report(result, pretty=pretty))

    if json_output:
        print("\n--- JSON ---")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
