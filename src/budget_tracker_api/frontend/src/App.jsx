import "./App.css";
import { useGetTransactions } from "../hooks/useGetTransactions";
import { useState } from "react";

function App() {
    // Get current date as default
    const currentDate = new Date();
    const [selectedYear, setSelectedYear] = useState(
        currentDate.getFullYear().toString(),
    );
    const [selectedMonth, setSelectedMonth] = useState(
        (currentDate.getMonth() + 1).toString(),
    );
    const [sortOrder, setSortOrder] = useState("desc"); // "asc" or "desc"

    const { transactions, transactionsIsLoading, transactionsIsErrored } =
        useGetTransactions(selectedYear, selectedMonth);
    console.log(transactions);

    // Sort transactions by amount
    const sortedTransactions = [...transactions].sort((a, b) => {
        if (sortOrder === "asc") {
            return a.amount - b.amount;
        } else {
            return b.amount - a.amount;
        }
    });

    // Calculate total net value (excluding payment transactions)
    const totalNetValue = transactions.reduce((sum, transaction) => {
        // Exclude credit card payments (transaction_type === "special")
        if (transaction.transaction_type === "special") {
            return sum;
        }
        return sum + (transaction.amount || 0);
    }, 0);

    // Generate year options (current year and past 5 years)
    const yearOptions = [];
    for (let i = 0; i < 6; i++) {
        yearOptions.push(currentDate.getFullYear() - i);
    }

    const monthNames = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ];

    return (
        <div className="app">
            <header className="app-header">
                <h1>Budget Tracker</h1>
                <p className="subtitle">Track your finances with ease</p>

                <div
                    style={{
                        marginTop: "20px",
                        display: "flex",
                        gap: "10px",
                        justifyContent: "center",
                    }}
                >
                    <a href="/link" target="_blank" rel="noopener noreferrer">
                        <button
                            style={{
                                padding: "10px 20px",
                                backgroundColor: "#007bff",
                                color: "white",
                                border: "none",
                                borderRadius: "4px",
                                cursor: "pointer",
                                fontSize: "16px",
                            }}
                        >
                            Link New Account
                        </button>
                    </a>
                    <a href="/update" target="_blank" rel="noopener noreferrer">
                        <button
                            style={{
                                padding: "10px 20px",
                                backgroundColor: "#28a745",
                                color: "white",
                                border: "none",
                                borderRadius: "4px",
                                cursor: "pointer",
                                fontSize: "16px",
                            }}
                        >
                            Re-authenticate Account
                        </button>
                    </a>
                </div>
            </header>

            <main className="app-main">
                {transactionsIsLoading ? (
                    <p>Loading...</p>
                ) : (
                    <div className="transactions-table">
                        <div
                            style={{
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "space-between",
                                marginBottom: "20px",
                                flexWrap: "wrap",
                                gap: "15px",
                            }}
                        >
                            <h2 style={{ margin: 0 }}>
                                Transactions for{" "}
                                {monthNames[parseInt(selectedMonth) - 1]}{" "}
                                {selectedYear}
                            </h2>

                            <div
                                style={{
                                    display: "flex",
                                    gap: "10px",
                                    alignItems: "center",
                                    flexWrap: "wrap",
                                }}
                            >
                                <label style={{ fontWeight: "bold" }}>
                                    Sort:
                                    <select
                                        value={sortOrder}
                                        onChange={(e) =>
                                            setSortOrder(e.target.value)
                                        }
                                        style={{
                                            marginLeft: "8px",
                                            padding: "8px 12px",
                                            fontSize: "16px",
                                            borderRadius: "4px",
                                            border: "1px solid #ccc",
                                            cursor: "pointer",
                                        }}
                                    >
                                        <option value="desc">
                                            Highest First
                                        </option>
                                        <option value="asc">
                                            Lowest First
                                        </option>
                                    </select>
                                </label>

                                <label style={{ fontWeight: "bold" }}>
                                    Month:
                                    <select
                                        value={selectedMonth}
                                        onChange={(e) =>
                                            setSelectedMonth(e.target.value)
                                        }
                                        style={{
                                            marginLeft: "8px",
                                            padding: "8px 12px",
                                            fontSize: "16px",
                                            borderRadius: "4px",
                                            border: "1px solid #ccc",
                                            cursor: "pointer",
                                        }}
                                    >
                                        {monthNames.map((month, index) => (
                                            <option
                                                key={index}
                                                value={(index + 1).toString()}
                                            >
                                                {month}
                                            </option>
                                        ))}
                                    </select>
                                </label>

                                <label style={{ fontWeight: "bold" }}>
                                    Year:
                                    <select
                                        value={selectedYear}
                                        onChange={(e) =>
                                            setSelectedYear(e.target.value)
                                        }
                                        style={{
                                            marginLeft: "8px",
                                            padding: "8px 12px",
                                            fontSize: "16px",
                                            borderRadius: "4px",
                                            border: "1px solid #ccc",
                                            cursor: "pointer",
                                        }}
                                    >
                                        {yearOptions.map((year) => (
                                            <option
                                                key={year}
                                                value={year.toString()}
                                            >
                                                {year}
                                            </option>
                                        ))}
                                    </select>
                                </label>
                            </div>
                        </div>
                        <div
                            style={{
                                backgroundColor: "#f0f8ff",
                                border: "2px solid #007bff",
                                borderRadius: "8px",
                                padding: "15px",
                                marginBottom: "20px",
                                textAlign: "center",
                            }}
                        >
                            <h3 style={{ margin: "0 0 10px 0", color: "#333" }}>
                                Total Expenses
                            </h3>
                            <p
                                style={{
                                    margin: "0",
                                    fontSize: "28px",
                                    fontWeight: "bold",
                                    color:
                                        totalNetValue >= 0
                                            ? "#dc3545"
                                            : "#28a745",
                                }}
                            >
                                ${totalNetValue.toFixed(2)}
                            </p>
                            <p
                                style={{
                                    margin: "5px 0 0 0",
                                    fontSize: "14px",
                                    color: "#666",
                                }}
                            >
                                {transactions.length} transaction
                                {transactions.length !== 1 ? "s" : ""}
                            </p>
                        </div>
                        <table>
                            <thead>
                                <tr>
                                    <th>Transaction Name</th>
                                    <th>Spend Value</th>
                                </tr>
                            </thead>
                            <tbody>
                                {!transactionsIsLoading &&
                                    !transactionsIsErrored &&
                                    sortedTransactions.map((transaction) => (
                                        <tr key={transaction.transaction_id}>
                                            <td>{transaction.name}</td>
                                            <td>
                                                ${transaction.amount.toFixed(2)}
                                            </td>
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
