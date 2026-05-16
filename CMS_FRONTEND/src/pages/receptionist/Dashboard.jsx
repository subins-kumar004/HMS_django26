import React, { useState, useEffect } from 'react';
import { Users, Calendar, FileText, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../../services/api';

const Dashboard = () => {
  const [patients, setPatients] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [patientsRes, apptsRes] = await Promise.all([
          api.get('receptionist/patients/'),
          api.get('receptionist/appointments/')
        ]);
        setPatients(patientsRes.data || []);
        setAppointments(apptsRes.data || []);
      } catch (err) {
        console.error("Dashboard fetch error:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const today = new Date().toISOString().split('T')[0];
  const todayAppointments = appointments.filter(a => a.appointment_date === today);

  if (loading) {
    return <div style={{ padding: '40px', textAlign: 'center' }}>Loading Dashboard...</div>;
  }

  return (
    <div className="animate-fade-in">
      <h2 style={{ marginBottom: '20px' }}>Receptionist Overview</h2>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '30px' }}>
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div style={{ padding: '15px', borderRadius: '50%', backgroundColor: 'rgba(0, 191, 165, 0.1)' }}>
            <Users size={28} color="var(--accent-primary)" />
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '24px' }}>{patients.length}</h3>
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Total Patients</p>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div style={{ padding: '15px', borderRadius: '50%', backgroundColor: 'rgba(0, 191, 165, 0.1)' }}>
            <Calendar size={28} color="var(--accent-primary)" />
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '24px' }}>{todayAppointments.length}</h3>
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Appointments Today</p>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div style={{ padding: '15px', borderRadius: '50%', backgroundColor: 'rgba(0, 191, 165, 0.1)' }}>
            <FileText size={28} color="var(--accent-primary)" />
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '24px' }}>{appointments.length}</h3>
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Total Appointments</p>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h3 style={{ margin: 0 }}>Today's Appointments</h3>
            <Link to="/receptionist/appointments" style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '14px' }}>
              View All <ArrowRight size={14} />
            </Link>
          </div>
          {todayAppointments.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)' }}>No appointments scheduled for today.</p>
          ) : (
            <table className="custom-table">
              <thead>
                <tr>
                  <th>Patient ID</th>
                  <th>Time</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {todayAppointments.slice(0, 5).map(appt => (
                  <tr key={appt.id}>
                    <td>{appt.patient}</td>
                    <td>{appt.appointment_time}</td>
                    <td><span className="badge badge-success">{appt.status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 style={{ margin: 0, marginBottom: '20px' }}>Quick Actions</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <Link to="/receptionist/patients" className="btn btn-primary" style={{ justifyContent: 'flex-start' }}>
              <Users size={18} /> Register Patient
            </Link>
            <Link to="/receptionist/appointments" className="btn btn-secondary" style={{ justifyContent: 'flex-start' }}>
              <Calendar size={18} /> Schedule Appointment
            </Link>
            <Link to="/receptionist/billing" className="btn btn-secondary" style={{ justifyContent: 'flex-start' }}>
              <FileText size={18} /> Generate Bill
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
