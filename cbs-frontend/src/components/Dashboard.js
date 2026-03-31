import React, { useState, useEffect } from 'react';

function Dashboard() {
  const [accounts, setAccounts] = useState([]);
  const [totalBalance, setTotalBalance] = useState(0);
  const [recentTransactions, setRecentTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      // Mock data - in production, call API Gateway
      const mockAccounts = [
        {
          accountId: 'ACC001',
          accountType: 'CURRENT',
          currency: 'EUR',
          balance: 5250.75,
          iban: 'SK9212345678901234567890',
        },
        {
          accountId: 'ACC002',
          accountType: 'SAVINGS',
          currency: 'EUR',
          balance: 12500.00,
          iban: 'SK9212345678901234567891',
        },
      ];
      
      setAccounts(mockAccounts);
      setTotalBalance(mockAccounts.reduce((sum, acc) => sum + acc.balance, 0));
      
      const mockTransactions = [
        {
          id: 'TXN001',
          type: 'TRANSFER',
          amount: 250.00,
          description: 'Payment to Supplier Inc.',
          date: new Date().toLocaleDateString(),
        },
        {
          id: 'TXN002',
          type: 'DEBIT',
          amount: 45.50,
          description: 'ATM Withdrawal',
          date: new Date().toLocaleDateString(),
        },
      ];
      
      setRecentTransactions(mockTransactions);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="card">Loading...</div>;
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Account Overview</h2>
          <p>Good morning — here's your financial summary</p>
        </div>
      </div>
      <div className="dashboard">
        <div className="card card-stat">
          <div className="card-stat-label">Total Balance</div>
          <div className="card-stat-value">€{totalBalance.toFixed(2)}</div>
          <div className="card-stat-sub">across all accounts</div>
          <div className="card-stat-accent"></div>
        </div>

        <div className="card card-stat">
          <div className="card-stat-label">Active Accounts</div>
          <div className="card-stat-value">{accounts.length}</div>
          <div className="card-stat-sub">current &amp; savings</div>
          <div className="card-stat-accent"></div>
        </div>

        <div className="card card-stat">
          <div className="card-stat-label">Transactions (7 days)</div>
          <div className="card-stat-value">{recentTransactions.length}</div>
          <div className="card-stat-sub">recent activity</div>
          <div className="card-stat-accent"></div>
        </div>

      </div>{/* end .dashboard grid */}

      <div style={{ marginTop: '20px', display: 'grid', gap: '20px' }}>
        <div className="card" style={{ gridColumn: '1 / -1' }}>
          <h3>Your Accounts</h3>
        <table className="table">
          <thead>
            <tr>
              <th>Type</th>
              <th>IBAN</th>
              <th>Balance</th>
            </tr>
          </thead>
          <tbody>
            {accounts.map((acc) => (
              <tr key={acc.accountId}>
                <td>{acc.accountType}</td>
                <td>{acc.iban}</td>
                <td>€{acc.balance.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h3>Recent Transactions</h3>
        <table className="table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Description</th>
              <th>Amount</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {recentTransactions.map((txn) => (
              <tr key={txn.id}>
                <td>{txn.type}</td>
                <td>{txn.description}</td>
                <td>€{txn.amount.toFixed(2)}</td>
                <td>{txn.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      </div>{/* end bottom cards */}
    </div>
  );
}

export default Dashboard;
