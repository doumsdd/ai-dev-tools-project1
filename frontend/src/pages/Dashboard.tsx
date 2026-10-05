import { useRevenueAnalytics } from '../api/client';

function Dashboard() {
  const { data, isLoading, error } = useRevenueAnalytics();

  if (isLoading) return <div className="loading">Chargement...</div>;
  if (error) return <div className="error">Erreur de chargement</div>;
  if (!data) return null;

  return (
    <div>
      <h2 className="page-title">Dashboard</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
        <div className="card">
          <h3>CA Total TTC</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#f39c12' }}>
            {data.total_revenue_ttc.toLocaleString('fr-FR')} €
          </p>
        </div>
        <div className="card">
          <h3>Factures payées</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>
            {data.paid_invoices_count}
          </p>
        </div>
        <div className="card">
          <h3>En attente</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#856404' }}>
            {data.pending_invoices_count}
          </p>
        </div>
        <div className="card">
          <h3>Montant moyen</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>
            {data.average_invoice_amount.toLocaleString('fr-FR')} €
          </p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
