import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Plus } from 'lucide-react';

const Doctors = () => {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDoctors = async () => {
      try {
        const res = await api.get('doctors/');
        setDoctors(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDoctors();
  }, []);

  return (
    <div className="animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '20px' }}>
        <button className="btn btn-primary">
          <Plus size={18} /> Add Doctor
        </button>
      </div>

      <div className="glass-panel table-container">
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center' }}>Loading...</div>
        ) : (
          <table className="custom-table">
            <thead>
              <tr>
                <th>Doctor ID</th>
                <th>Staff Ref</th>
                <th>Specialization</th>
                <th>Consultation Fee</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {doctors.map((doc) => (
                <tr key={doc.id} style={{ opacity: doc.is_active ? 1 : 0.6 }}>
                  <td>{doc.id}</td>
                  <td>{doc.staff}</td>
                  <td>{doc.specialization}</td>
                  <td>${doc.consultation_fee}</td>
                  <td>
                    <span className={`badge ${doc.is_active ? 'badge-success' : 'badge-danger'}`}>
                      {doc.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                </tr>
              ))}
              {doctors.length === 0 && (
                <tr>
                  <td colSpan="5" style={{ textAlign: 'center', padding: '30px' }}>No doctors found.</td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Doctors;
