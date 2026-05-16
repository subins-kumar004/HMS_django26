import React, { useState, useEffect } from 'react';
import { FlaskConical, CheckCircle, Clock, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../../services/api';

const Dashboard = () => {
  const [tests, setTests] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [testsRes, resultsRes] = await Promise.all([
          api.get('labtests/'),
          api.get('labtests/results/')
        ]);
        setTests(testsRes.data || []);
        setResults(resultsRes.data || []);
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
      <h2 style={{ marginBottom: '20px' }}>Lab Technician Overview</h2>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '30px' }}>
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div style={{ padding: '15px', borderRadius: '50%', backgroundColor: 'rgba(0, 191, 165, 0.1)' }}>
            <FlaskConical size={28} color="var(--accent-primary)" />
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '24px' }}>{tests.length}</h3>
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Available Tests</p>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div style={{ padding: '15px', borderRadius: '50%', backgroundColor: 'rgba(0, 191, 165, 0.1)' }}>
            <CheckCircle size={28} color="var(--accent-primary)" />
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '24px' }}>{results.length}</h3>
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Results Recorded</p>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h3 style={{ margin: 0 }}>Recent Test Results</h3>
            <Link to="/labtech/results" style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '14px' }}>
              View All <ArrowRight size={14} />
            </Link>
          </div>
          {results.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)' }}>No results found.</p>
          ) : (
            <table className="custom-table">
              <thead>
                <tr>
                  <th>Test ID</th>
                  <th>Value</th>
                  <th>Remarks</th>
                </tr>
              </thead>
              <tbody>
                {results.slice(0, 5).map(res => (
                  <tr key={res.id}>
                    <td>{res.lab_test}</td>
                    <td>{res.test_value || 'Pending'}</td>
                    <td>{res.remarks?.substring(0, 30) || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 style={{ margin: 0, marginBottom: '20px' }}>Quick Actions</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <Link to="/labtech/results" className="btn btn-primary" style={{ justifyContent: 'flex-start' }}>
              <FlaskConical size={18} /> Record New Result
            </Link>
            <Link to="/labtech/tests" className="btn btn-secondary" style={{ justifyContent: 'flex-start' }}>
              <CheckCircle size={18} /> Manage Test Types
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
