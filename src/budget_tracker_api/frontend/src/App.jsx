import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Test API connection
    fetch('/api/status')
      .then(res => res.json())
      .then(data => {
        setStatus(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('API Error:', err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <h1>Budget Tracker</h1>
        <p className="subtitle">Track your finances with ease</p>
      </header>

      <main className="app-main">
        <div className="api-status">
          <h2>API Status</h2>
          {loading ? (
            <p>Checking connection...</p>
          ) : status ? (
            <p className="status-ok">✓ {status.status}</p>
          ) : (
            <p className="status-error">✗ Failed to connect</p>
          )}
        </div>

        <div className="content">
          <p>Welcome to your Budget Tracker application.</p>
          <p>Start building your financial dashboard here!</p>
        </div>
      </main>
    </div>
  );
}

export default App;
