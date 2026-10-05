# Dashboard Page

## Objective
Create a comprehensive dashboard that displays key business metrics and insights for the construction billing app.

## Route
- Path: `/` (home page)
- File: `src/routes/index.tsx` or `src/routes/dashboard.tsx`

## Requirements

### 1. KPI Cards (Top Section)
Display 4 metric cards in a grid (2x2 on mobile, 4 columns on desktop):

**Card 1: Total Revenue (Paid)**
- Icon: `DollarSign` (green)
- Label: "Total Revenue"
- Value: Sum of TTC for all paid invoices
- Subtitle: "From X paid invoices"
- Color: green accent

**Card 2: Outstanding (Sent + Overdue)**
- Icon: `Clock` (orange)
- Label: "Outstanding"
- Value: Sum of TTC for sent + overdue invoices
- Subtitle: "X invoices awaiting payment"
- Color: orange accent

**Card 3: Overdue**
- Icon: `AlertTriangle` (red)
- Label: "Overdue"
- Value: Sum of TTC for overdue invoices
- Subtitle: "X invoices past due"
- Color: red accent

**Card 4: Draft**
- Icon: `FileEdit` (gray)
- Label: "Drafts"
- Value: Count of draft invoices
- Subtitle: "Ready to send"
- Color: gray accent

### 2. Revenue Chart (Main Section)
Monthly revenue chart using Recharts:

**Chart Type:** Area chart or Bar chart
**Data:** Last 6 months of revenue (paid invoices only)
**X-axis:** Month names (e.g., "May", "Jun", "Jul")
**Y-axis:** Amount in €
**Tooltip:** Show exact amount on hover
**Responsive:** Chart should resize with container

Use `AreaChart`, `Area`, `XAxis`, `YAxis`, `CartesianGrid`, `Tooltip`, `ResponsiveContainer` from Recharts.

### 3. Recent Invoices (Side Section)
List of 5 most recent invoices:
- Invoice number
- Client name
- Status badge
- Amount TTC
- Issue date (relative: "2 days ago", "1 week ago")

Clicking navigates to invoice detail.

### 4. Top Clients (Side Section)
Top 3 clients by revenue (paid invoices):
- Client company name
- Total revenue (TTC)
- Number of invoices
- Progress bar showing % of total revenue

### 5. Quick Stats (Bottom Section)
Small stats row:
- Average invoice amount
- Average payment time (days between issue and paid)
- Win rate: paid / (paid + cancelled)

## Data Calculations

Use the existing data from `@/lib/store`:
```typescript
const { state } = useStore();
const { invoices, clients } = state;
```

**Calculations:**
```typescript
// Total revenue (paid only)
const totalRevenue = invoices
  .filter(inv => inv.status === 'paid')
  .reduce((sum, inv) => sum + computeTotals(inv.lines).totalTTC, 0);

// Outstanding (sent + overdue)
const outstanding = invoices
  .filter(inv => ['sent', 'overdue'].includes(inv.status))
  .reduce((sum, inv) => sum + computeTotals(inv.lines).totalTTC, 0);

// Monthly data for chart
const monthlyData = last6Months.map(month => ({
  month: month.name,
  revenue: invoices
    .filter(inv => inv.status === 'paid' && isInMonth(inv.paidAt, month))
    .reduce((sum, inv) => sum + computeTotals(inv.lines).totalTTC, 0)
}));
```

Use `computeTotals` from `@/lib/invoice-calc`.

## Components to Use
- `Card`, `CardHeader`, `CardContent` for KPI cards
- `AreaChart` or `BarChart` from Recharts
- `Table` for recent invoices
- `Progress` for top clients
- Icons: `DollarSign`, `Clock`, `AlertTriangle`, `FileEdit`, `TrendingUp`

## Layout
```
┌─────────────────────────────────────────────────────┐
│ Dashboard                                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│ │ Revenue  │ │Outstand. │ │ Overdue  │ │ Drafts │ │
│ │ 245,680€ │ │ 68,450€  │ │ 22,190€  │ │   2    │ │
│ │ 5 paid   │ │ 3 invoices│ │ 1 invoice│ │        │ │
│ └──────────┘ └──────────┘ └──────────┘ └────────┘ │
│                                                     │
│ ┌─────────────────────────────┐ ┌─────────────────┐│
│ │ Revenue (Last 6 Months)     │ │ Recent Invoices ││
│ │                             │ │                 ││
│ │     ╱\      ╱\              │ │ FAC-010  2,180€ ││
│ │    ╱  \    ╱  \   ╱\        │ │ FAC-009 18,420€ ││
│ │   ╱    \  ╱    \ ╱  \       │ │ FAC-008 45,680€ ││
│ │  ╱      ╲╱      ╲    \      │ │ FAC-007 82,340€ ││
│ │ ╱                          │ │ FAC-006 68,900€ ││
│ │ May  Jun  Jul  Aug  Sep  Oct│ │                 ││
│ └─────────────────────────────┘ └─────────────────┘│
│                                                     │
│ ┌─────────────────────────────┐ ┌─────────────────┐│
│ │ Top Clients                 │ │ Quick Stats     ││
│ │                             │ │                 ││
│ │ Nexity      ████████ 45%    │ │ Avg: 24,568€    ││
│ │ Mairie      ██████   35%    │ │ Pay time: 28d   ││
│ │ OPAC        ████     20%    │ │ Win rate: 80%   ││
│ └─────────────────────────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────┘
```

## Acceptance Criteria
- [ ] 4 KPI cards display correct values
- [ ] Revenue chart shows last 6 months
- [ ] Chart is responsive
- [ ] Recent invoices list shows 5 items
- [ ] Top clients show top 3 by revenue
- [ ] Quick stats calculate correctly
- [ ] All amounts formatted as EUR currency
- [ ] Loading states while data loads
- [ ] Empty state if no invoices
