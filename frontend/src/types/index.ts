/** Types pour les entités de l'API guestBTP */

// ============ Client ============

export type ClientType = 'particulier' | 'entreprise' | 'maitre_ouvrage';

export interface Client {
  id: number;
  name: string;
  email: string;
  phone?: string | null;
  address?: string | null;
  siret?: string | null;
  client_type: ClientType;
  archived: boolean;
  created_at: string;
  updated_at: string;
}

export interface ClientCreate {
  name: string;
  email: string;
  phone?: string;
  address?: string;
  siret?: string;
  client_type: ClientType;
}

export interface ClientUpdate {
  name?: string;
  phone?: string;
  address?: string;
  siret?: string;
  client_type?: ClientType;
}

// ============ Invoice ============

export type InvoiceStatus = 'brouillon' | 'envoyee' | 'payee' | 'annulee' | 'en_retard';

export type LineCategory =
  | 'maconnerie'
  | 'plomberie'
  | 'electricite'
  | 'peinture'
  | 'terrassement'
  | 'couverture'
  | 'autre';

export type LineUnit = 'm2' | 'm3' | 'heure' | 'jour' | 'forfait' | 'unite';

export type VatRate = 5.5 | 10 | 20;

export interface InvoiceLine {
  id: number;
  description: string;
  category: LineCategory;
  quantity: number;
  unit: LineUnit;
  unit_price: number;
  vat_rate: VatRate;
  discount: number;
  total_ht: number;
}

export interface InvoiceLineCreate {
  description: string;
  category: LineCategory;
  quantity: number;
  unit: LineUnit;
  unit_price: number;
  vat_rate: VatRate;
  discount?: number;
}

export interface Invoice {
  id: number;
  invoice_number: string;
  client_id: number;
  status: InvoiceStatus;
  issue_date: string;
  due_date?: string | null;
  paid_at?: string | null;
  subtotal_ht: number;
  total_vat: number;
  total_ttc: number;
  notes?: string | null;
  created_at: string;
  updated_at: string;
  lines: InvoiceLine[];
}

export interface InvoiceSummary {
  id: number;
  invoice_number: string;
  client_id: number;
  client_name?: string | null;
  status: InvoiceStatus;
  issue_date: string;
  due_date?: string | null;
  total_ttc: number;
  created_at: string;
}

export interface InvoiceCreate {
  client_id: number;
  issue_date: string;
  due_date?: string;
  lines: InvoiceLineCreate[];
  notes?: string;
}

// ============ Analytics ============

export interface MonthlyRevenue {
  month: number;
  month_name: string;
  revenue_ht: number;
  revenue_ttc: number;
  invoices_count: number;
}

export interface TopClient {
  client_id: number;
  client_name: string;
  total_revenue_ttc: number;
  invoices_count: number;
}

export interface AnalyticsRevenue {
  year: number;
  total_revenue_ht: number;
  total_revenue_ttc: number;
  total_vat_collected: number;
  paid_invoices_count: number;
  pending_invoices_count: number;
  cancelled_invoices_count: number;
  average_invoice_amount: number;
  monthly_breakdown: MonthlyRevenue[];
  top_clients: TopClient[];
}

// ============ Pagination ============

export interface Pagination {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: Pagination;
}

// ============ Errors ============

export interface ApiError {
  error: string;
  message: string;
}

export interface ValidationDetail {
  field: string;
  message: string;
}

export interface ValidationError {
  error: string;
  message: string;
  details: ValidationDetail[];
}
