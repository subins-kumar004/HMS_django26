import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Plus } from 'lucide-react';

const Specializations = () => {
  const [specs, setSpecs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSpecs = async () => {
      try {
        const res = await api.get('specializations/');
        setSpecs(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchSpecs();
  }, []);

  return (
    <div className="animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '20px' }}>
        <button className="btn btn-primary">
          <Plus size={18} /> Add Specialization
        </button>
      </div>

      <div className="glass-panel table-container">
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center' }}>Loading...</div>
        ) : (
          <table className="custom-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Specialization Name</th>
              </tr>
            </thead>
            <tbody>
              {specs.map((spec) => (
                <tr key={spec.id}>
                  <td>{spec.id}</td>
                  <td>{spec.specialization_name}</td>
                </tr>
              ))}
              {specs.length === 0 && (
                <tr>
                  <td colSpan="2" style={{ textAlign: 'center', padding: '30px' }}>No specializations found.</td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Specializations;
