import React, { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';
import Sidebar from './Sidebar';
import Header from './Header';

const Layout = ({ allowedRoles = [], title = "Dashboard" }) => {
  const { user, loading } = useContext(AuthContext);

  if (loading) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', color: 'var(--accent-primary)' }}>Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  const role = user.role?.toLowerCase() || '';
  
  if (allowedRoles.length > 0 && !allowedRoles.some(r => role.includes(r.toLowerCase())) && !role.includes('admin')) {
    return <Navigate to="/unauthorized" replace />;
  }

  return (
    <div className="app-container">
      <Sidebar />
      <div className="main-content">
        <Header title={title} />
        <Outlet />
      </div>
    </div>
  );
};

export default Layout;
