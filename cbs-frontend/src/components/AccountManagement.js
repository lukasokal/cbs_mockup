import React, { useState, useEffect } from 'react';

function AccountManagement() {
  const [accounts, setAccounts] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    customerId: '',
    accountType: 'CURRENT',
    currency: 'EUR',
    balance: 0,
    iban: '',
  });

  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = async () => {
    try {
      // Mock data - replace with API call
      const mockAccounts = [
        {
          accountId: 'ACC001',
          customerId: 'CUST001',
          accountType: 'CURRENT',
          currency: 'EUR',
          balance: 5250.75,
          status: 'ACTIVE',
          iban: 'SK9212345678901234567890',
          createdAt: '2024-01-15T10:30:00',
        },
        {
          accountId: 'ACC002',
          customerId: 'CUST001',
          accountType: 'SAVINGS',
          currency: 'EUR',
          balance: 12500.00,
          status: 'ACTIVE',
          iban: 'SK9212345678901234567891',
          createdAt: '2024-02-20T14:45:00',
        },
      ];
      setAccounts(mockAccounts);
    } catch (error) {
      console.error('Error fetching accounts:', error);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      // TODO: Call API Gateway POST /api/accounts
      console.log('Creating account:', formData);
      setShowCreateForm(false);
      setFormData({
        customerId: '',
        accountType: 'CURRENT',
        currency: 'EUR',
        balance: 0,
        iban: '',
      });
      // fetchAccounts();
    } catch (error) {
      console.error('Error creating account:', error);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Account Management</h2>
          <p>Manage your retail and corporate accounts</p>
        </div>
        <button
          className="btn-secondary"
          onClick={() => setShowCreateForm(!showCreateForm)}
          style={{ width: 'auto', padding: '10px 20px', fontSize: '14px' }}
        >
          {showCreateForm ? '✕ Cancel' : '+ Open New Account'}
        </button>
      </div>

      {showCreateForm && (
        <div className="card" style={{ marginBottom: '20px' }}>
          <h3>New Account</h3>
          <form onSubmit={handleCreate}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div className="form-group">
                <label>Customer ID</label>
                <input
                  type="text"
                  value={formData.customerId}
                  placeholder="CUST001"
                  onChange={(e) =>
                    setFormData({ ...formData, customerId: e.target.value })
                  }
                  required
                />
              </div>
              <div className="form-group">
                <label>Account Type</label>
                <select
                  value={formData.accountType}
                  onChange={(e) =>
                    setFormData({ ...formData, accountType: e.target.value })
                  }
                >
                  <option>CURRENT</option>
                  <option>SAVINGS</option>
                  <option>CORPORATE</option>
                </select>
              </div>
              <div className="form-group">
                <label>Currency</label>
                <input
                  type="text"
                  value={formData.currency}
                  onChange={(e) =>
                    setFormData({ ...formData, currency: e.target.value })
                  }
                />
              </div>
              <div className="form-group">
                <label>Initial Balance</label>
                <input
                  type="number"
                  value={formData.balance}
                  onChange={(e) =>
                    setFormData({ ...formData, balance: parseFloat(e.target.value) })
                  }
                />
              </div>
            </div>
            <button type="submit" className="btn-primary" style={{ width: 'auto', padding: '10px 28px' }}>
              Open Account
            </button>
          </form>
        </div>
      )}

      <div className="card">
        <h3>All Accounts</h3>
        <table className="table">
          <thead>
            <tr>
              <th>Account ID</th>
              <th>Type</th>
              <th>IBAN</th>
              <th>Balance</th>
              <th>Status</th>
              <th>Opened</th>
            </tr>
          </thead>
          <tbody>
            {accounts.map((acc) => (
              <tr key={acc.accountId}>
                <td style={{ fontFamily: 'monospace', fontSize: 13 }}>{acc.accountId}</td>
                <td>{acc.accountType}</td>
                <td style={{ fontFamily: 'monospace', fontSize: 12 }}>{acc.iban}</td>
                <td style={{ fontWeight: 600 }}>€{acc.balance.toFixed(2)}</td>
                <td>
                  <span className={`badge badge-${acc.status === 'ACTIVE' ? 'active' : 'blocked'}`}>
                    {acc.status}
                  </span>
                </td>
                <td>{new Date(acc.createdAt).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default AccountManagement;
