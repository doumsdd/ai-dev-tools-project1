import { useInvoices } from '../api/client';

function InvoicesPage() {
  const { data, isLoading, error } = useInvoices({ limit: 50 });

  if (isLoading) return <div className="loading">Chargement...</div>;
  if (error) return <div className="error">Erreur de chargement</div>;
  if (!data) return null;

  return (
    <div>
      <h2 className="page-title">Factures</h2>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>N°</th>
              <th>Client</th>
              <th>Date</th>
              <th>Statut</th>
              <th>Total TTC</th>
            </tr>
          </thead>
          <tbody>
            {data.data.map((invoice) => (
              <tr key={invoice.id}>
                <td>{invoice.invoice_number}</td>
                <td>{invoice.client_name || `Client #${invoice.client_id}`}</td>
                <td>{new Date(invoice.issue_date).toLocaleDateString('fr-FR')}</td>
                <td>
                  <span className={`status-badge status-${invoice.status}`}>
                    {invoice.status}
                  </span>
                </td>
                <td>{invoice.total_ttc.toLocaleString('fr-FR')} €</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p style={{ marginTop: '1rem', color: '#666' }}>
          {data.pagination.total} facture(s) au total
        </p>
      </div>
    </div>
  );
}

export default InvoicesPage;
