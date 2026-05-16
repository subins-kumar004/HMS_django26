import React, { useContext } from 'react';
import { NavLink } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';
import { 
  Users, Activity, Calendar, Pill, FlaskConical, LayoutDashboard, Settings, LogOut 
} from 'lucide-react';

const Sidebar = () => {
  const { user, logout } = useContext(AuthContext);
  const role = user?.role?.toLowerCase() || '';

  const navLinks = [];

  if (role.includes('admin')) {
    navLinks.push({ path: '/admin', label: 'Admin Dashboard', icon: <LayoutDashboard size={20} /> });
    navLinks.push({ path: '/admin/staff', label: 'Staff Management', icon: <Users size={20} /> });
    navLinks.push({ path: '/admin/doctors', label: 'Doctors', icon: <Activity size={20} /> });
    navLinks.push({ path: '/admin/specializations', label: 'Specializations', icon: <Settings size={20} /> });
  } else if (role.includes('receptionist')) {
    navLinks.push({ path: '/receptionist', label: 'Dashboard', icon: <LayoutDashboard size={20} /> });
    navLinks.push({ path: '/receptionist/patients', label: 'Patients', icon: <Users size={20} /> });
    navLinks.push({ path: '/receptionist/appointments', label: 'Appointments', icon: <Calendar size={20} /> });
    navLinks.push({ path: '/receptionist/billing', label: 'Billing', icon: <Activity size={20} /> });
  } else if (role.includes('doctor')) {
    navLinks.push({ path: '/doctor', label: 'Dashboard', icon: <LayoutDashboard size={20} /> });
    navLinks.push({ path: '/doctor/consultations', label: 'Consultations', icon: <Activity size={20} /> });
    navLinks.push({ path: '/doctor/prescriptions', label: 'Prescriptions', icon: <Pill size={20} /> });
  } else if (role.includes('pharmacist')) {
    navLinks.push({ path: '/pharmacist', label: 'Dashboard', icon: <LayoutDashboard size={20} /> });
    navLinks.push({ path: '/pharmacist/medicines', label: 'Medicines Catalog', icon: <Pill size={20} /> });
    navLinks.push({ path: '/pharmacist/inventory', label: 'Inventory', icon: <Activity size={20} /> });
  } else if (role.includes('lab')) {
    navLinks.push({ path: '/labtech', label: 'Dashboard', icon: <LayoutDashboard size={20} /> });
    navLinks.push({ path: '/labtech/tests', label: 'Lab Tests', icon: <FlaskConical size={20} /> });
    navLinks.push({ path: '/labtech/results', label: 'Test Results', icon: <Activity size={20} /> });
  }

  return (
    <div className="glass-panel" style={{ 
      width: '260px', 
      height: '100vh', 
      position: 'sticky', 
      top: 0,
      display: 'flex',
      flexDirection: 'column',
      borderRight: '1px solid var(--border-color)',
      borderTop: 'none',
      borderBottom: 'none',
      borderLeft: 'none',
      borderRadius: 0
    }}>
      <div style={{ padding: '24px', display: 'flex', alignItems: 'center', gap: '12px', borderBottom: '1px solid rgba(0, 191, 165, 0.1)' }}>
        <Activity size={32} color="var(--accent-primary)" />
        <div>
          <h2 style={{ fontSize: '18px', color: 'var(--accent-primary)', margin: 0 }}>HMS Pro</h2>
          <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>{user?.role || 'Portal'}</span>
        </div>
      </div>

      <div style={{ flex: 1, padding: '20px 12px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {navLinks.map((link) => (
          <NavLink 
            key={link.path} 
            to={link.path}
            end={link.path === '/admin'}
            style={({ isActive }) => ({
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '12px 16px',
              borderRadius: '8px',
              color: isActive ? '#0a0f12' : 'var(--text-secondary)',
              backgroundColor: isActive ? 'var(--accent-primary)' : 'transparent',
              textDecoration: 'none',
              fontWeight: isActive ? '600' : '500',
              transition: 'all 0.2s ease',
            })}
          >
            {link.icon}
            {link.label}
          </NavLink>
        ))}
      </div>

      <div style={{ padding: '20px', borderTop: '1px solid rgba(0, 191, 165, 0.1)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
          <div style={{ width: '40px', height: '40px', borderRadius: '50%', backgroundColor: 'var(--accent-light)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--accent-primary)', fontWeight: 'bold' }}>
            {user?.username?.charAt(0).toUpperCase() || 'U'}
          </div>
          <div>
            <p style={{ margin: 0, fontSize: '14px', fontWeight: '600' }}>{user?.username || 'User'}</p>
            <p style={{ margin: 0, fontSize: '12px', color: 'var(--text-secondary)' }}>{user?.role}</p>
          </div>
        </div>
        <button 
          onClick={logout}
          className="btn btn-secondary" 
          style={{ width: '100%', borderColor: 'rgba(255, 82, 82, 0.3)', color: 'var(--danger)' }}
        >
          <LogOut size={16} /> Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
