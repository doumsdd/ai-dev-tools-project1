import { describe, it, expect } from 'vitest';
import {
  calculateTotal,
  calculateLineTotal,
  calculateLineVat,
} from '../api/client';

describe('calculateLineTotal', () => {
  it('calcule le total HT sans remise', () => {
    const result = calculateLineTotal({ quantity: 10, unit_price: 100 });
    expect(result).toBe(1000);
  });

  it('calcule le total HT avec remise', () => {
    const result = calculateLineTotal({
      quantity: 10,
      unit_price: 100,
      discount: 10,
    });
    expect(result).toBe(900);
  });

  it('gère les quantités décimales', () => {
    const result = calculateLineTotal({ quantity: 2.5, unit_price: 100 });
    expect(result).toBe(250);
  });

  it('arrondit à 2 décimales', () => {
    const result = calculateLineTotal({ quantity: 1, unit_price: 33.33 });
    expect(result).toBe(33.33);
  });
});

describe('calculateLineVat', () => {
  it('calcule la TVA à 20%', () => {
    const result = calculateLineVat(1000, 20);
    expect(result).toBe(200);
  });

  it('calcule la TVA à 10%', () => {
    const result = calculateLineVat(1000, 10);
    expect(result).toBe(100);
  });

  it('calcule la TVA à 5.5%', () => {
    const result = calculateLineVat(1000, 5.5);
    expect(result).toBe(55);
  });
});

describe('calculateTotal', () => {
  it('calcule les totaux pour une facture simple', () => {
    const lines = [
      { quantity: 10, unit_price: 100, vat_rate: 20 },
    ];
    const result = calculateTotal(lines);

    expect(result.subtotal_ht).toBe(1000);
    expect(result.total_vat).toBe(200);
    expect(result.total_ttc).toBe(1200);
  });

  it('calcule les totaux avec plusieurs lignes', () => {
    const lines = [
      { quantity: 10, unit_price: 100, vat_rate: 20 }, // 1000 HT, 200 TVA
      { quantity: 5, unit_price: 80, vat_rate: 10 },    // 400 HT, 40 TVA
    ];
    const result = calculateTotal(lines);

    expect(result.subtotal_ht).toBe(1400);
    expect(result.total_vat).toBe(240);
    expect(result.total_ttc).toBe(1640);
  });

  it('calcule les totaux avec remise', () => {
    const lines = [
      { quantity: 10, unit_price: 100, vat_rate: 20, discount: 10 }, // 900 HT, 180 TVA
    ];
    const result = calculateTotal(lines);

    expect(result.subtotal_ht).toBe(900);
    expect(result.total_vat).toBe(180);
    expect(result.total_ttc).toBe(1080);
  });

  it('gère les taux de TVA mixtes', () => {
    const lines = [
      { quantity: 10, unit_price: 100, vat_rate: 20 },  // 1000 HT, 200 TVA
      { quantity: 5, unit_price: 80, vat_rate: 10 },     // 400 HT, 40 TVA
      { quantity: 20, unit_price: 50, vat_rate: 5.5 },   // 1000 HT, 55 TVA
    ];
    const result = calculateTotal(lines);

    expect(result.subtotal_ht).toBe(2400);
    expect(result.total_vat).toBe(295);
    expect(result.total_ttc).toBe(2695);
  });

  it('retourne des zéros pour une liste vide', () => {
    const result = calculateTotal([]);

    expect(result.subtotal_ht).toBe(0);
    expect(result.total_vat).toBe(0);
    expect(result.total_ttc).toBe(0);
  });

  it('arrondit correctement les résultats', () => {
    const lines = [
      { quantity: 1, unit_price: 33.33, vat_rate: 20 }, // 33.33 HT, 6.67 TVA
    ];
    const result = calculateTotal(lines);

    expect(result.subtotal_ht).toBe(33.33);
    expect(result.total_vat).toBe(6.67);
    expect(result.total_ttc).toBe(40.00);
  });
});
