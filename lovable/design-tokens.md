# Design System - BuildRight Billing

## 🎨 Color Palette

| Name | Hex | Usage |
|------|-----|-------|
| Anthracite Gray | `#2C3E50` | Primary, navigation, headings |
| Construction Yellow | `#F39C12` | Accent, CTA buttons, alerts |
| Success Green | `#27AE60` | Paid status, success messages |
| Error Red | `#E74C3C` | Cancelled status, errors |
| Info Blue | `#3498DB` | Sent status, links |
| Warning Orange | `#E67E22` | Overdue status, warnings |
| Light Gray | `#ECF0F1` | Background |
| White | `#FFFFFF` | Cards, forms |

## 📝 Typography

- **Headings**: Inter Bold (700) - clean, modern
- **Body**: Inter Regular (400) - readable
- **Monospace**: JetBrains Mono - invoice numbers, codes

## 🎯 Status Colors

| Status | Color | Tailwind Classes |
|--------|-------|------------------|
| Draft | Gray | `bg-gray-100 text-gray-800` |
| Sent | Blue | `bg-blue-100 text-blue-800` |
| Paid | Green | `bg-green-100 text-green-800` |
| Cancelled | Red | `bg-red-100 text-red-800` |
| Overdue | Orange | `bg-orange-100 text-orange-800` |

## 🧩 shadcn/ui Components

### Core Components
- `Button` - variants: default (yellow), outline, ghost, destructive
- `Card` - for KPIs, invoice details, forms
- `Table` - for clients/invoices lists
- `Badge` - for statuses
- `Dialog` - for create/edit forms, confirmations
- `Input` - form fields
- `Select` - dropdowns (client type, VAT rate, category)
- `Tabs` - organize sections
- `DropdownMenu` - actions menu
- `Toast` - notifications
- `Sheet` - mobile sidebar
- `Skeleton` - loading states

### Icons (Lucide React)
- `HardHat` - logo
- `Dashboard` - navigation
- `Users` - clients
- `FileText` - invoices
- `DollarSign` - revenue
- `Clock` - outstanding
- `AlertTriangle` - overdue
- `FileEdit` - drafts
- `Plus` - add new
- `ChevronRight` - navigation
- `Menu` - mobile menu
- `Search` - search
- `Filter` - filters
- `LogIn` - login
- `UserRound` - guest user

## 🎨 Logo

Simple text logo:
- Text: "guestBTP" (or "BuildRight")
- Font: Inter Bold
- Icon: Hard hat (Lucide icon: `HardHat`)
- Color: Anthracite + Yellow accent

Example:
```tsx
<div className="flex items-center gap-2">
  <span className="grid h-10 w-10 place-items-center rounded-sm bg-primary text-primary-foreground">
    <HardHat className="h-6 w-6" />
  </span>
  <span className="font-display text-2xl font-bold">
    guest<span className="text-primary">BTP</span>
  </span>
</div>
```

## 📐 Spacing

- Cards: `rounded-lg shadow-sm p-6`
- Buttons: `rounded-md px-4 py-2`
- Inputs: `rounded-md px-3 py-2`
- Tables: `rounded-lg border`
- Badges: `rounded-full px-2.5 py-0.5 text-xs`

## 🎬 Animations

- Subtle transitions: `transition-all duration-200`
- Hover effects on cards/buttons
- Smooth page transitions
- Pulse animation for overdue status

## 📱 Responsive Breakpoints

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Mobile Adaptations
- Sidebar → hamburger menu (Sheet component)
- Tables → cards
- Grid layouts → stacked
- Font sizes reduced

## 💡 Design Principles

1. **Clarity**: Information hierarchy is clear
2. **Consistency**: Same patterns everywhere
3. **Feedback**: Every action has visual feedback
4. **Accessibility**: WCAG AA compliant
5. **Professional**: Industrial/construction aesthetic
