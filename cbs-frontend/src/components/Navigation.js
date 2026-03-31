import React from 'react';

function Navigation({ onNavigate, onLogout }) {
  const [activePage, setActivePage] = React.useState('dashboard');

  const handleNavigate = (page) => {
    setActivePage(page);
    onNavigate(page);
  };

  return (
    <div className="navigation">
      <div className="nav-header">
        <div className="nav-logo-mark">T</div>
        <div className="nav-title">
          <span>Tatra Banka</span>
          <span>Internet Banking</span>
        </div>
      </div>

      <div className="nav-section">Main Menu</div>
      <div className="nav-menu">
        <button
          className={`nav-item ${activePage === 'dashboard' ? 'active' : ''}`}
          onClick={() => handleNavigate('dashboard')}
        >
          <span className="nav-icon">▦</span>
          Overview
        </button>
        <button
          className={`nav-item ${activePage === 'accounts' ? 'active' : ''}`}
          onClick={() => handleNavigate('accounts')}
        >
          <span className="nav-icon">◈</span>
          Accounts
        </button>
        <button
          className={`nav-item ${activePage === 'payments' ? 'active' : ''}`}
          onClick={() => handleNavigate('payments')}
        >
          <span className="nav-icon">⇄</span>
          Payments
        </button>
      </div>

      <div className="nav-footer">
        <div className="nav-user">
          <div className="nav-user-avatar">JN</div>
          <div className="nav-user-info">
            <span>Ján Novák</span>
            <span>Premium Client</span>
          </div>
        </div>
        <button className="nav-item" onClick={onLogout}>
          <span className="nav-icon">⏻</span>
          Sign Out
        </button>
      </div>
    </div>
  );
}

export default Navigation;
