import React, { useState, useEffect } from 'react';

function PaymentCenter() {
  const [payments, setPayments] = useState([]);
  const [showPaymentForm, setShowPaymentForm] = useState(false);
  const [formData, setFormData] = useState({
    initiatorAccountId: '',
    beneficiaryIban: '',
    beneficiaryName: '',
    amount: 0,
    currency: 'EUR',
    paymentType: 'SEPA_SCT',
    remittanceInformation: '',
  });

  useEffect(() => {
    fetchPayments();
  }, []);

  const fetchPayments = async () => {
    try {
      // Mock data - replace with API call
      const mockPayments = [
        {
          paymentId: 'PAY001',
          initiatorAccountId: 'ACC001',
          beneficiaryIban: 'DE89370400440532013000',
          beneficiaryName: 'John Doe',
          amount: 500.00,
          currency: 'EUR',
          paymentType: 'SEPA_SCT',
          paymentStatus: 'ACCEPTED',
          createdAt: '2024-03-10T09:15:00',
        },
        {
          paymentId: 'PAY002',
          initiatorAccountId: 'ACC001',
          beneficiaryIban: 'CZ2020100000000656430200',
          beneficiaryName: 'Jane Smith',
          amount: 1200.00,
          currency: 'EUR',
          paymentType: 'SEPA_SCT',
          paymentStatus: 'PENDING',
          createdAt: '2024-03-11T14:30:00',
        },
      ];
      setPayments(mockPayments);
    } catch (error) {
      console.error('Error fetching payments:', error);
    }
  };

  const handleInitiatePayment = async (e) => {
    e.preventDefault();
    if (formData.amount <= 0) {
      alert('Amount must be greater than zero.');
      return;
    }
    try {
      // TODO: Call API Gateway POST /api/payments
      setShowPaymentForm(false);
      setFormData({
        initiatorAccountId: '',
        beneficiaryIban: '',
        beneficiaryName: '',
        amount: 0,
        currency: 'EUR',
        paymentType: 'SEPA_SCT',
        remittanceInformation: '',
      });
      // fetchPayments();
    } catch (error) {
      console.error('Error initiating payment:', error);
    }
  };

  const handleApprovePayment = async (paymentId) => {
    try {
      // TODO: Call API Gateway POST /api/payments/{paymentId}/approve
      // fetchPayments();
    } catch (error) {
      console.error('Error approving payment:', error);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Payment Center</h2>
          <p>Send SEPA, SWIFT, and instant payments</p>
        </div>
        <button
          className="btn-secondary"
          onClick={() => setShowPaymentForm(!showPaymentForm)}
          style={{ width: 'auto', padding: '10px 20px', fontSize: '14px' }}
        >
          {showPaymentForm ? '✕ Cancel' : '+ New Payment'}
        </button>
      </div>

      {showPaymentForm && (
        <div className="card" style={{ marginBottom: '20px' }}>
          <h3>New Payment Order</h3>
          <form onSubmit={handleInitiatePayment}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div className="form-group">
                <label>Debit Account ID</label>
                <input
                  type="text"
                  value={formData.initiatorAccountId}
                  placeholder="ACC001"
                  onChange={(e) =>
                    setFormData({ ...formData, initiatorAccountId: e.target.value })
                  }
                  required
                />
              </div>
              <div className="form-group">
                <label>Payment Type</label>
                <select
                  value={formData.paymentType}
                  onChange={(e) =>
                    setFormData({ ...formData, paymentType: e.target.value })
                  }
                >
                  <option>SEPA_SCT</option>
                  <option>SEPA_SDD</option>
                  <option>SWIFT</option>
                  <option>INSTANT</option>
                </select>
              </div>
              <div className="form-group">
                <label>Beneficiary IBAN</label>
                <input
                  type="text"
                  value={formData.beneficiaryIban}
                  placeholder="SK9212345678901234567890"
                  onChange={(e) =>
                    setFormData({ ...formData, beneficiaryIban: e.target.value })
                  }
                  required
                />
              </div>
              <div className="form-group">
                <label>Beneficiary Name</label>
                <input
                  type="text"
                  value={formData.beneficiaryName}
                  placeholder="John Doe"
                  onChange={(e) =>
                    setFormData({ ...formData, beneficiaryName: e.target.value })
                  }
                  required
                />
              </div>
              <div className="form-group">
                <label>Amount (EUR)</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.amount}
                  onChange={(e) =>
                    setFormData({ ...formData, amount: parseFloat(e.target.value) })
                  }
                  required
                />
              </div>
              <div className="form-group">
                <label>Remittance Information</label>
                <input
                  type="text"
                  value={formData.remittanceInformation}
                  placeholder="Invoice #123"
                  onChange={(e) =>
                    setFormData({ ...formData, remittanceInformation: e.target.value })
                  }
                />
              </div>
            </div>
            <button type="submit" className="btn-primary" style={{ width: 'auto', padding: '10px 28px' }}>
              Send Payment
            </button>
          </form>
        </div>
      )}

      <div className="card">
        <h3>Payment History</h3>
        <table className="table">
          <thead>
            <tr>
              <th>Reference</th>
              <th>Beneficiary</th>
              <th>Amount</th>
              <th>Type</th>
              <th>Status</th>
              <th>Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {payments.map((payment) => (
              <tr key={payment.paymentId}>
                <td style={{ fontFamily: 'monospace', fontSize: 13 }}>{payment.paymentId}</td>
                <td>{payment.beneficiaryName}</td>
                <td style={{ fontWeight: 600 }}>€{payment.amount.toFixed(2)}</td>
                <td><span style={{ fontSize: 12 }}>{payment.paymentType}</span></td>
                <td>
                  <span className={`badge badge-${
                    payment.paymentStatus === 'ACCEPTED' ? 'active' :
                    payment.paymentStatus === 'REJECTED' ? 'rejected' : 'pending'
                  }`}>
                    {payment.paymentStatus}
                  </span>
                </td>
                <td>{new Date(payment.createdAt).toLocaleDateString()}</td>
                <td>
                  {payment.paymentStatus === 'PENDING' && (
                    <button
                      onClick={() => handleApprovePayment(payment.paymentId)}
                      className="btn-secondary"
                      style={{ padding: '6px 14px', fontSize: '12px' }}
                    >
                      Approve
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default PaymentCenter;
