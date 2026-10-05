/**
 * Client API centralisé pour guestBTP.
 *
 * Tous les appels API de l'application DOIVENT passer par ce module.
 */

import axios from 'axios';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import type {
  Client,
  ClientCreate,
  ClientUpdate,
  Invoice,
  InvoiceCreate,
  InvoiceStatus,
  PaginatedResponse,
  InvoiceSummary,
  AnalyticsRevenue,
} from '../types';

// ============ Instance Axios ============

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.message ||
      error.response?.data?.detail ||
      error.message ||
      'Une erreur est survenue';
    console.error('[API Error]', message);
    return Promise.reject(error);
  }
);

// ============ Clients API ============

export const clientsApi = {
  list: async (params?: {
    page?: number;
    limit?: number;
    search?: string;
    include_archived?: boolean;
  }): Promise<PaginatedResponse<Client>> => {
    const { data } = await apiClient.get('/clients', { params });
    return data;
  },

  get: async (id: number): Promise<Client> => {
    const { data } = await apiClient.get(`/clients/${id}`);
    return data;
  },

  create: async (client: ClientCreate): Promise<Client> => {
    const { data } = await apiClient.post('/clients', client);
    return data;
  },

  update: async (id: number, client: ClientUpdate): Promise<Client> => {
    const { data } = await apiClient.patch(`/clients/${id}`, client);
    return data;
  },

  archive: async (id: number): Promise<void> => {
    await apiClient.delete(`/clients/${id}`);
  },
};

// ============ Invoices API ============

export const invoicesApi = {
  list: async (params?: {
    page?: number;
    limit?: number;
    status?: InvoiceStatus;
    client_id?: number;
  }): Promise<PaginatedResponse<InvoiceSummary>> => {
    const { data } = await apiClient.get('/invoices', { params });
    return data;
  },

  get: async (id: number): Promise<Invoice> => {
    const { data } = await apiClient.get(`/invoices/${id}`);
    return data;
  },

  create: async (invoice: InvoiceCreate): Promise<Invoice> => {
    const { data } = await apiClient.post('/invoices', invoice);
    return data;
  },

  transitionStatus: async (
    id: number,
    status: InvoiceStatus
  ): Promise<Invoice> => {
// ============ Fonctions utilitaires ============

/**
 * Calcule le total HT d'une ligne de facture.
 * Formule : quantity × unit_price × (1 - discount/100)
 */
export function calculateLineTotal(line: {
  quantity: number;
  unit_price: number;
  discount?: number;
}): number {
  const subtotal = line.quantity * line.unit_price;
  const discount = line.discount ?? 0;
  const total = subtotal * (1 - discount / 100);
  return Math.round(total * 100) / 100;
}

/**
 * Calcule la TVA d'une ligne de facture.
 */
export function calculateLineVat(lineTotalHt: number, vatRate: number): number {
  const vat = lineTotalHt * (vatRate / 100);
  return Math.round(vat * 100) / 100;
}

/**
 * Calcule les totaux d'une facture à partir de ses lignes.
 * @returns { subtotal_ht, total_vat, total_ttc }
 */
export function calculateTotal(lines: Array<{
  quantity: number;
  unit_price: number;
  vat_rate: number;
  discount?: number;
}>): { subtotal_ht: number; total_vat: number; total_ttc: number } {
  let subtotal_ht = 0;
  let total_vat = 0;

  for (const line of lines) {
    const lineHt = calculateLineTotal(line);
    const lineVat = calculateLineVat(lineHt, line.vat_rate);
    subtotal_ht += lineHt;
    total_vat += lineVat;
  }

  subtotal_ht = Math.round(subtotal_ht * 100) / 100;
  total_vat = Math.round(total_vat * 100) / 100;
  const total_ttc = Math.round((subtotal_ht + total_vat) * 100) / 100;

  return { subtotal_ht, total_vat, total_ttc };
}

    const { data } = await apiClient.patch(`/invoices/${id}/status`, {
      status,
    });
    return data;
  },
};

// ============ Analytics API ============

export const analyticsApi = {
  getRevenue: async (year?: number): Promise<AnalyticsRevenue> => {
    const { data } = await apiClient.get('/analytics/revenue', {
      params: year ? { year } : undefined,
    });
    return data;
  },

// ============ Hooks TanStack Query ============

export function useClients(params?: {
  page?: number;
  limit?: number;
  search?: string;
  include_archived?: boolean;
}) {
  return useQuery({
    queryKey: ['clients', params],
    queryFn: () => clientsApi.list(params),
  });
}

export function useClient(id: number) {
  return useQuery({
    queryKey: ['client', id],
    queryFn: () => clientsApi.get(id),
    enabled: id > 0,
  });
}

export function useCreateClient() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (client: ClientCreate) => clientsApi.create(client),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['clients'] }),
  });
}

export function useUpdateClient() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: ClientUpdate }) =>
      clientsApi.update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['clients'] }),
  });
}

export function useArchiveClient() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => clientsApi.archive(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['clients'] }),
  });
}

export function useInvoices(params?: {
  page?: number;
  limit?: number;
  status?: InvoiceStatus;
  client_id?: number;
}) {
  return useQuery({
    queryKey: ['invoices', params],
    queryFn: () => invoicesApi.list(params),
  });
}

export function useInvoice(id: number) {
  return useQuery({
    queryKey: ['invoice', id],
    queryFn: () => invoicesApi.get(id),
    enabled: id > 0,
  });
}

export function useCreateInvoice() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (invoice: InvoiceCreate) => invoicesApi.create(invoice),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['invoices'] }),
  });
}

export function useTransitionInvoiceStatus() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, status }: { id: number; status: InvoiceStatus }) =>
      invoicesApi.transitionStatus(id, status),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['invoices'] }),
  });
}

export function useRevenueAnalytics(year?: number) {
  return useQuery({
    queryKey: ['analytics', 'revenue', year],
    queryFn: () => analyticsApi.getRevenue(year),
  });
}

};
