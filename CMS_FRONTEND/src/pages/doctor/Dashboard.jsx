import React, { useState, useEffect } from 'react';
import { Activity, Pill, Clock, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../../services/api';

const Dashboard = () => {
  const [consultations, setConsultations] = useState([]);
  const [prescriptions, setPrescriptions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [consRes, presRes] = await Promise.all([
          api.get('doctor/consultations/'),
          api.get('doctor/prescriptions/medicine/')
        ]);
        setConsultations(consRes.data || []);
        setPrescriptions(presRes.data || []);
      } catch (err) {
        console.error("Dashboard fetch error:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <div style={{ padding: '40px', textAlign: 'center' }}>Loading Dashboard...</div>;
  }

  return (
    <div className="animate-fade-in">
      <h2 style={{ marginBottom: '20px' }}>Doctor Overview</h2>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '30px' }}>
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div style={{ padding: '15px', borderRadius: '50%', backgroundColor: 'rgba(0, 191, 165, 0.1)' }}>
            <Activity size={28} color="var(--accent-primary)" />
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '24px' }}>{consultations.length}</h3>
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Total Consultations</p>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div style={{ padding: '15px', borderRadius: '50%', backgroundColor: 'rgba(0, 191, 165, 0.1)' }}>
            <Pill size={28} color="var(--accent-primary)" />
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '24px' }}>{prescriptions.length}</h3>
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Prescriptions Issued</p>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h3 style={{ margin: 0 }}>Recent Consultations</h3>
            <Link to="/doctor/consultations" style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '14px' }}>
              View All <ArrowRight size={14} />
            </Link>
          </div>
          {consultations.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)' }}>No consultations found.</p>
          ) : (
            <table className="custom-table">
              <thead>
                <tr>
                  <th>Appt ID</th>
                  <th>Symptoms</th>
                  <th>Diagnosis</th>
                </tr>
              </thead>
              <tbody>
                {consultations.slice(0, 5).map(cons => (
                  <tr key={cons.id}>
                    <td>{cons.appointment}</td>
                    <td>{cons.symptoms?.substring(0, 30) || 'N/A'}...</td>
                    <td>{cons.diagnosis?.substring(0, 30) || 'N/A'}...</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 style={{ margin: 0, marginBottom: '20px' }}>Quick Actions</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <Link to="/doctor/consultations" className="btn btn-primary" style={{ justifyContent: 'flex-start' }}>
              <Activity size={18} /> New Consultation
            </Link>
            <Link to="/doctor/prescriptions" className="btn btn-secondary" style={{ justifyContent: 'flex-start' }}>
              <Pill size={18} /> Prescribe Medicine
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
