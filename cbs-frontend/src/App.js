import React, { useState } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import AccountManagement from './components/AccountManagement';
import PaymentCenter from './components/PaymentCenter';
import Navigation from './components/Navigation';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleNavigate = (page) => {
    setCurrentPage(page);
  };

  const handleLogin = (credentials) => {
    // TODO: Call API for authentication
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setCurrentPage('dashboard');
  };

  if (!isAuthenticated) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <div className="app">
      <Navigation onNavigate={handleNavigate} onLogout={handleLogout} />
      <div className="content">
        {currentPage === 'dashboard' && <Dashboard />}
        {currentPage === 'accounts' && <AccountManagement />}
        {currentPage === 'payments' && <PaymentCenter />}
      </div>
    </div>
  );
}

function LoginPage({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin({ email, password });
  };

  return (
    <div className="login-container">
      <div className="login-left">
        <div className="login-brand">
          <div className="login-brand-logo">
            <div className="logo-mark">T</div>
          </div>
          <h1>Tatra Banka</h1>
          <p>Internet Banking — Core Banking Platform<br />Secure · Reliable · Trusted since 1990</p>
        </div>
      </div>
      <div className="login-right">
        <div className="login-card">
          <h2>Sign in</h2>
          <p className="login-subtitle">Enter your credentials to access your account</p>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={email}
                placeholder="your@email.sk"
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                value={password}
                placeholder="••••••••"
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="btn-primary">Sign In to Internet Banking</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
