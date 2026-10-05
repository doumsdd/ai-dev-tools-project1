import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ClientsPage from './pages/ClientsPage';
import InvoicesPage from './pages/InvoicesPage';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <h1>🏗️ guestBTP</h1>
          <nav>
            <Link to="/">Dashboard</Link>
            <Link to="/clients">Clients</Link>
            <Link to="/invoices">Factures</Link>
          </nav>
        </header>
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/clients" element={<ClientsPage />} />
            <Route path="/invoices" element={<InvoicesPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
