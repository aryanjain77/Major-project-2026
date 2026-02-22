// src/App.jsx
import { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { auth, googleProvider } from './firebase';
import { signInWithPopup, onAuthStateChanged, signOut } from 'firebase/auth';
import Dashboard from './Dashboard';
import './index.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });
    return () => unsubscribe();
  }, []);

  const handleLogin = async () => {
    try {
      await signInWithPopup(auth, googleProvider);
    } catch (error) {
      console.error("Login failed:", error);
      alert("Could not sign in. Please try again.");
    }
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="app-container">
      <header className="header">
        <div className="container">
          <h1>ApplyWise</h1>
          {user && (
            <div className="user-info">
              <span>Hi, {user.displayName || user.email}</span>
              <button className="btn btn-danger" onClick={handleLogout}>
                Logout
              </button>
            </div>
          )}
        </div>
      </header>

      <main className="main-content">
        <div className="container">
          <Routes>
            {/* Public route: Login */}
            <Route
              path="/"
              element={
                user ? (
                  <Navigate to="/dashboard" replace /> // redirect if already logged in
                ) : (
                  <div className="login-prompt">
                    <h2>Sign in to start tracking jobs</h2>
                    <p>Organize applications, see progress, get alerts, and learn from others.</p>
                    <button className="btn btn-primary" onClick={handleLogin}>
                      Sign in with Google
                    </button>
                  </div>
                )
              }
            />

            {/* Protected route: Dashboard */}
            <Route
              path="/dashboard"
              element={
                user ? (
                  <Dashboard />
                ) : (
                  <Navigate to="/" replace /> // redirect to login if not authenticated
                )
              }
            />

            {/* Catch-all: redirect to login */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </main>
    </div>
  );
}

export default App;