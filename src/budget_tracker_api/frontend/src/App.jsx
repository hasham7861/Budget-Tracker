import './App.css';
import { useGetTransactions } from '../hooks/useGetTransactions';

function App() {

  const {transactions, transactionsIsLoading, transactionsIsErrored} = useGetTransactions();
  console.log(transactions)

  return (
    <div className="app">
      <header className="app-header">
        <h1>Budget Tracker</h1>
        <p className="subtitle">Track your finances with ease</p>
      </header>

      <main className="app-main">
        {transactionsIsLoading ? (
          <p>Loading...</p>
        ) : (
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
                {!transactionsIsLoading && !transactionsIsErrored && transactions.map((transaction)=> (
                  <tr key={transaction.id}>
                    <td>{transaction.name}</td>
                    <td>{transaction.amount}</td>
                  </tr>
                ))}

              </tbody>
            </table>
          </div>
        )}

      </main>
    </div>
  );
}

export default App;
