# Polish & Responsive

## Objective
Final polish pass: responsive design, animations, empty states, and UX improvements across all pages.

## 1. Responsive Navigation

### Mobile Sidebar (< 1024px)
- Replace fixed sidebar with hamburger menu
- Sidebar slides in from left on click
- Overlay backdrop when open
- Close on outside click or route change
- Use `Sheet` component from shadcn/ui

**Implementation:**
```tsx
<Sheet>
  <SheetTrigger asChild>
    <Button variant="ghost" size="icon" className="lg:hidden">
      <Menu className="h-5 w-5" />
    </Button>
  </SheetTrigger>
  <SheetContent side="left" className="w-64">
    {/* Sidebar content */}
  </SheetContent>
</Sheet>
```

### Mobile Header
- Logo on left
- Hamburger menu on right (mobile)
- User avatar + logout on right (desktop)

## 2. Responsive Tables → Cards

### Pattern for all tables (invoices, clients):
**Desktop (≥ 768px):** Standard table layout
**Mobile (< 768px):** Card layout

**Implementation:**
```tsx
{/* Desktop */}
<div className="hidden md:block">
  <Table>...</Table>
</div>

{/* Mobile */}
<div className="md:hidden space-y-3">
  {items.map(item => (
    <Card key={item.id}>
      <CardContent className="p-4">
        <div className="flex justify-between">
          <span className="font-semibold">{item.number}</span>
          <StatusBadge status={item.status} />
        </div>
        <div className="mt-2 text-sm text-muted-foreground">
          {item.clientName}
        </div>
        <div className="mt-2 flex justify-between">
          <span className="font-mono">{formatCurrency(item.totalTTC)}</span>
          <span className="text-xs">{item.dueDate}</span>
        </div>
      </CardContent>
    </Card>
  ))}
</div>
```

## 3. Empty States

Add empty states for all list views:

**No Clients:**
```tsx
<Card className="text-center py-12">
  <Users className="mx-auto h-12 w-12 text-muted-foreground" />
  <h3 className="mt-4 text-lg font-semibold">No clients yet</h3>
  <p className="mt-2 text-sm text-muted-foreground">
    Get started by adding your first client.
  </p>
  <Button className="mt-4" onClick={() => navigate({ to: '/clients/new' })}>
    <Plus className="mr-2 h-4 w-4" /> Add Client
  </Button>
</Card>
```

**No Invoices:**
Similar pattern with `FileText` icon.

**No Results (with filters):**
```tsx
<Card className="text-center py-12">
  <Search className="mx-auto h-12 w-12 text-muted-foreground" />
  <h3 className="mt-4 text-lg font-semibold">No results found</h3>
  <p className="mt-2 text-sm text-muted-foreground">
    Try adjusting your filters or search criteria.
  </p>
  <Button variant="outline" className="mt-4" onClick={clearFilters}>
    Clear filters
  </Button>
</Card>
```

## 4. Loading States

Use `Skeleton` component for all loading states:

**Table skeleton:**
```tsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead><Skeleton className="h-4 w-20" /></TableHead>
      {/* ... */}
    </TableRow>
  </TableHeader>
  <TableBody>
    {Array.from({ length: 5 }).map((_, i) => (
      <TableRow key={i}>
        <TableCell><Skeleton className="h-4 w-32" /></TableCell>
        <TableCell><Skeleton className="h-4 w-24" /></TableCell>
        <TableCell><Skeleton className="h-6 w-16" /></TableCell>
        <TableCell><Skeleton className="h-4 w-20" /></TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

## 5. Animations & Transitions

### Page Transitions
Add subtle fade-in on page load:
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.page-content {
  animation: fadeIn 0.3s ease-out;
}
```

### Hover Effects
- Cards: `hover:shadow-md transition-shadow`
- Table rows: `hover:bg-muted/50 transition-colors`
- Buttons: already handled by shadcn/ui

### Status Badge Pulse (for overdue)
```tsx
{status === 'overdue' && (
  <span className="relative flex h-2 w-2">
    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-orange-400 opacity-75"></span>
    <span className="relative inline-flex rounded-full h-2 w-2 bg-orange-500"></span>
  </span>
)}
```

## 6. Toast Notifications

Add toast for all user actions:

**Success:**
```tsx
toast({
  title: "Invoice sent",
  description: "FAC-2026-001 has been marked as sent.",
});
```

**Error:**
```tsx
toast({
  variant: "destructive",
  title: "Error",
  description: "Failed to update invoice status.",
});
```

Use `useToast` hook from `@/hooks/use-toast`.

## 7. Currency & Date Formatting

**Currency:**
```typescript
const formatCurrency = (amount: number) => 
  new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'EUR',
  }).format(amount);
```

**Relative Dates:**
```typescript
const formatRelativeDate = (dateStr: string) => {
  const date = new Date(dateStr);
  const now = new Date();
  const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
  
  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
  return date.toLocaleDateString('fr-FR');
};
```

## 8. Accessibility

- All interactive elements have focus states
- Color contrast meets WCAG AA (4.5:1)
- Icons have aria-labels or aria-hidden
- Tables have proper headers
- Forms have labels linked to inputs

## Acceptance Criteria
- [ ] Mobile sidebar works (hamburger menu)
- [ ] Tables become cards on mobile
- [ ] Empty states show for all lists
- [ ] Loading skeletons display correctly
- [ ] Page transitions are smooth
- [ ] Hover effects work on cards/rows
- [ ] Toast notifications appear for actions
- [ ] Currency formatted consistently (€)
- [ ] Dates formatted correctly
- [ ] All forms have validation
- [ ] Accessibility: keyboard navigation works
- [ ] No console errors

