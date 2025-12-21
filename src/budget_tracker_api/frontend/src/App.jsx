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

      fetch('/api/transactions')
        .then(res => res.json())
        .then(data => {
          console.log('Transactions:', data);
        })
        .catch(err => {
          console.error('Transactions API Error:', err);
        });
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <h1>Budget Tracker</h1>
        <p className="subtitle">Track your finances with ease</p>
      </header>

      <main className="app-main">
        {loading ? (
          <p>Loading...</p>
        ) : status ? (
          <div className="transactions-table">
            <h2>Transactions for December</h2>
            <table>
              <thead>
                <tr>
                  <th>Transaction Name</th>
                  <th>Spend Value</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Groceries</td>
                  <td>$45.50</td>
                </tr>
                <tr>
                  <td>Gas</td>
                  <td>$32.00</td>
                </tr>
                <tr>
                  <td>Coffee</td>
                  <td>$5.25</td>
                </tr>
              </tbody>
            </table>
          </div>
        ) : (
          <p>Error connecting to the API. Please try again later.</p>
        )}

      </main>
    </div>
  );
}

export default App;
