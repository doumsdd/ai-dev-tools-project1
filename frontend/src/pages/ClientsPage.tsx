import { useClients } from '../api/client';

function ClientsPage() {
  const { data, isLoading, error } = useClients({ limit: 50 });

  if (isLoading) return <div className="loading">Chargement...</div>;
  if (error) return <div className="error">Erreur de chargement</div>;
  if (!data) return null;

  return (
    <div>
      <h2 className="page-title">Clients</h2>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Nom</th>
              <th>Email</th>
              <th>Type</th>
              <th>Téléphone</th>
            </tr>
          </thead>
          <tbody>
            {data.data.map((client) => (
              <tr key={client.id}>
                <td>{client.name}</td>
                <td>{client.email}</td>
                <td>{client.client_type}</td>
                <td>{client.phone || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p style={{ marginTop: '1rem', color: '#666' }}>
          {data.pagination.total} client(s) au total
        </p>
      </div>
    </div>
  );
}

export default ClientsPage;
