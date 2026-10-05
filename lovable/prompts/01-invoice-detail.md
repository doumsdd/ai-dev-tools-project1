# Invoice Detail Page

## Objective
Create a detailed invoice view page that displays all invoice information and allows status transitions according to business rules.

## Route
- Path: `/invoices/:invoiceId`
- File: `src/routes/invoices.$invoiceId.tsx`
- Use TanStack Router for route params

## Requirements

### 1. Invoice Header Section
Display invoice metadata in a Card:
- Invoice number (e.g., "FAC-2026-001")
- Status badge (use existing StatusBadge component)
- Project name
- Client name (fetch from clients array using clientId)
- Issue date and due date
- Paid date (if status is "paid")

### 2. Invoice Lines Table
Display all invoice lines in a Table:
- Description
- Quantity + unit (e.g., "420 m³")
- Unit price HT
- VAT rate (5.5%, 10%, or 20%)
- Line total HT (quantity × unitPriceHT)

Use the `computeTotals` function from `@/lib/invoice-calc` to calculate totals.

### 3. Totals Section
Display at the bottom:
- Subtotal HT
- Total VAT
- **Total TTC** (highlighted, larger font)

### 4. Status Actions (CRITICAL)
Show action buttons based on current status:

**Draft status:**
- "Send Invoice" button → transitions to "sent"
- "Cancel" button → transitions to "cancelled"

**Sent status:**
- "Mark as Paid" button → transitions to "paid"
- "Cancel" button → transitions to "cancelled"

**Overdue status:**
- "Mark as Paid" button → transitions to "paid"
- No cancel option (already overdue)

**Paid or Cancelled status:**
- No action buttons (read-only)
- Show message: "This invoice is finalized and cannot be modified"

Use the `canTransition` function from `@/lib/invoice-calc` to validate transitions.
Use the `reducer` from `@/lib/store` with action `{ type: "transition", id: invoiceId, to: newStatus }`.

### 5. Navigation
- "Back to Invoices" button at the top
- Breadcrumb: Invoices > FAC-2026-001

## Components to Use
- `Card`, `CardHeader`, `CardContent` for sections
- `Table`, `TableHeader`, `TableBody`, `TableRow`, `TableCell` for lines
- `Badge` for status (use existing StatusBadge)
- `Button` for actions (variant="default" for primary, variant="outline" for secondary)
- `Dialog` for confirmation before status change
- `Toast` for success/error messages

## Business Rules (ENFORCE)
- ❌ NO delete button anywhere
- ✅ Use `canTransition(from, to)` before allowing status change
- ✅ Paid/Cancelled invoices are READ-ONLY
- ✅ Show confirmation dialog before status change
- ✅ After status change, refresh the invoice data

## Acceptance Criteria
- [ ] Invoice details display correctly
- [ ] All lines shown with correct calculations
- [ ] Totals match: HT + VAT = TTC
- [ ] Action buttons only show when appropriate
- [ ] Status transitions work and persist
- [ ] Invalid transitions are blocked
- [ ] Confirmation dialog appears before changes
- [ ] Toast notification on success
- [ ] Read-only state for paid/cancelled invoices

## Example Layout
```
┌─────────────────────────────────────────┐
│ ← Back to Invoices                      │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ FAC-2026-001          [PAID]        │ │
│ │ Résidence Le Belvédère              │ │
│ │ Client: Nexity Promotion Lyon       │ │
│ │ Issued: 2026-04-05  Due: 2026-05-05 │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ Invoice Lines                       │ │
│ │ ┌─────────────────────────────────┐ │ │
│ │ │ Description    │ Qty │ Price │ T │ │ │
│ │ │ Terrassement   │ 420m³│ 28€  │...│ │ │
│ │ │ Dalle béton    │ 380m²│ 85€  │...│ │ │
│ │ │ Main d'œuvre   │ 120h │ 45€  │...│ │ │
│ │ └─────────────────────────────────┘ │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ Subtotal HT:        78,940.00 €     │ │
│ │ VAT (20%):          15,788.00 €     │ │
│ │ ─────────────────────────────────   │ │
│ │ Total TTC:          94,728.00 €     │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ [This invoice is paid and cannot be     │
│  be modified]                           │
└─────────────────────────────────────────┘
```
