# Improve Invoice List Page

## Objective
Enhance the existing invoice list page with better interactivity, filtering, and visual feedback.

## Route
- Path: `/invoices`
- File: `src/routes/invoices.tsx`

## Requirements

### 1. Clickable Rows
- Each invoice row should be clickable
- Clicking navigates to `/invoices/:invoiceId` (detail page)
- Add hover effect: `hover:bg-muted/50 cursor-pointer`
- Add chevron icon on the right: `ChevronRight` from lucide-react

### 2. Status Badge Colors
Ensure StatusBadge uses these colors consistently:
- `draft`: gray (`bg-gray-100 text-gray-800`)
- `sent`: blue (`bg-blue-100 text-blue-800`)
- `paid`: green (`bg-green-100 text-green-800`)
- `cancelled`: red (`bg-red-100 text-red-800`)
- `overdue`: orange (`bg-orange-100 text-orange-800`)

### 3. Filters Section
Add a filter bar above the table:

**Status Filter (Select dropdown):**
- All statuses (default)
- Draft
- Sent
- Paid
- Cancelled
- Overdue

**Client Filter (Select dropdown):**
- All clients (default)
- List of all clients (companyName)

**Search Input:**
- Search by invoice number or project name
- Debounced input (300ms)

### 4. Sorting
Add clickable column headers for sorting:
- Invoice number (alphabetical)
- Issue date (newest/oldest)
- Due date (newest/oldest)
- Total TTC (highest/lowest)

Show sort indicator (arrow up/down) on sorted column.

### 5. Summary Stats
Show a summary bar above the table:
- Total invoices: X
- Total amount: XX,XXX €
- Filtered: X invoices (when filters active)

### 6. Empty States
Show appropriate messages when:
- No invoices at all: "No invoices yet. Create your first invoice!"
- No results with filters: "No invoices match your filters. Try adjusting your criteria."
- Loading state: Skeleton loader for table rows

### 7. Quick Actions (Optional)
Add a "Quick Actions" dropdown menu on each row:
- View details
- If draft: "Send" action
- If sent: "Mark as paid" action
- Use `DropdownMenu` from shadcn/ui

## Components to Use
- `Table` for the invoice list
- `Select` for filters
- `Input` for search
- `Badge` for status
- `DropdownMenu` for quick actions
- `Skeleton` for loading states
- Icons: `ChevronRight`, `Filter`, `Search`, `ArrowUpDown`

## Implementation Notes
- Use `useMemo` for filtered/sorted data (performance)
- Keep URL params in sync with filters (optional but nice)
- Use `useNavigate` from TanStack Router for navigation
- Format currency: `new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' })`

## Acceptance Criteria
- [ ] Rows are clickable and navigate to detail
- [ ] Status badges have correct colors
- [ ] Filters work (status, client, search)
- [ ] Sorting works on all columns
- [ ] Summary stats display correctly
- [ ] Empty states show appropriate messages
- [ ] Responsive: table scrolls horizontally on mobile
- [ ] Quick actions work (if implemented)

## Example Layout
```
┌─────────────────────────────────────────────────────┐
│ Invoices                              [+ New]       │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Total: 10 invoices  |  Amount: 245,680 €        │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ ┌──────────────┬──────────────┬──────────────────┐ │
│ │ Status: [All]│ Client: [All]│ 🔍 Search...     │ │
│ └──────────────┴──────────────┴──────────────────┘ │
│                                                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Number  │ Client   │ Status │ Amount   │ Due    │ │
│ ├─────────────────────────────────────────────────┤ │
│ │ FAC-001 │ Nexity   │ [Paid] │ 94,728 € │ 05-05 →│ │
│ │ FAC-002 │ Mairie   │ [Paid] │ 68,450 € │ 05-18 →│ │
│ │ FAC-003 │ OPAC     │ [Sent] │ 12,672 € │ 06-10 →│ │
│ │ FAC-004 │ SCI      │ [Over] │ 22,190 € │ 07-02 →│ │
│ │ ...     │ ...      │ ...    │ ...      │ ...    │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```
