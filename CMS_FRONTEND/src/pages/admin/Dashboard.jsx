import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Users, Activity, Settings } from 'lucide-react';

const Dashboard = () => {
  const [stats, setStats] = useState({ staff: 0, doctors: 0, specializations: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [staffRes, docRes, specRes] = await Promise.all([
          api.get('staff/'),
          api.get('doctors/'),
          api.get('specializations/')
        ]);
        
        setStats({
          staff: staffRes.data.length || 0,
          doctors: docRes.data.length || 0,
          specializations: specRes.data.length || 0
        });
      } catch (err) {
        console.error("Error fetching stats:", err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchStats();
  }, []);

  return (
    <div className="animate-fade-in">
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '30px' }}>
        
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', alignItems: 'center', gap: '20px' }}>
          <div style={{ backgroundColor: 'rgba(0, 191, 165, 0.15)', padding: '16px', borderRadius: '12px', color: 'var(--accent-primary)' }}>
            <Users size={32} />
          </div>
          <div>
            <h3 style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '5px' }}>Total Staff</h3>
            <p style={{ fontSize: '32px', fontWeight: '700', margin: 0 }}>{loading ? '...' : stats.staff}</p>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px', display: 'flex', alignItems: 'center', gap: '20px' }}>
          <div style={{ backgroundColor: 'rgba(0, 191, 165, 0.15)', padding: '16px', borderRadius: '12px', color: 'var(--accent-primary)' }}>
            <Activity size={32} />
          </div>
          <div>
            <h3 style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '5px' }}>Total Doctors</h3>
            <p style={{ fontSize: '32px', fontWeight: '700', margin: 0 }}>{loading ? '...' : stats.doctors}</p>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '24px', display: 'flex', alignItems: 'center', gap: '20px' }}>
          <div style={{ backgroundColor: 'rgba(0, 191, 165, 0.15)', padding: '16px', borderRadius: '12px', color: 'var(--accent-primary)' }}>
            <Settings size={32} />
          </div>
          <div>
            <h3 style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '5px' }}>Specializations</h3>
            <p style={{ fontSize: '32px', fontWeight: '700', margin: 0 }}>{loading ? '...' : stats.specializations}</p>
          </div>
        </div>

      </div>

      <div className="glass-panel" style={{ padding: '24px' }}>
        <h2 style={{ marginBottom: '20px', fontSize: '18px' }}>Welcome to HMS Pro</h2>
        <p style={{ color: 'var(--text-secondary)', lineHeight: '1.6' }}>
          Use the sidebar navigation to manage staff members, register doctors, and configure medical specializations.
          The interface is fully connected to the Django backend APIs with secure JWT authentication.
        </p>
      </div>
    </div>
  );
};

export default Dashboard;
