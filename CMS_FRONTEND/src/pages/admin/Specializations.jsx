import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Plus, Edit2, X } from 'lucide-react';

const Specializations = () => {
  const [specs, setSpecs] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Modal state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({ specialization_name: '' });
  const [editingId, setEditingId] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const fetchSpecs = async () => {
    try {
      setLoading(true);
      const res = await api.get('specializations/');
      setSpecs(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSpecs();
  }, []);

  const openModal = (spec = null) => {
    if (spec) {
      setEditingId(spec.id);
      setFormData({ specialization_name: spec.specialization_name });
    } else {
      setEditingId(null);
      setFormData({ specialization_name: '' });
    }
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setFormData({ specialization_name: '' });
    setEditingId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      if (editingId) {
        await api.put(`specializations/${editingId}/`, formData);
      } else {
        await api.post('specializations/create/', formData);
      }
      closeModal();
      fetchSpecs();
    } catch (err) {
      alert("Error saving specialization: " + (err.response?.data?.detail || JSON.stringify(err.response?.data)));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
        <h2>Specializations</h2>
        <button className="btn btn-primary" onClick={() => openModal()}>
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
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {specs.map((spec) => (
                <tr key={spec.id}>
                  <td>{spec.id}</td>
                  <td>{spec.specialization_name}</td>
                  <td>
                    <button className="btn btn-secondary" style={{ padding: '6px' }} onClick={() => openModal(spec)}>
                      <Edit2 size={16} />
                    </button>
                  </td>
                </tr>
              ))}
              {specs.length === 0 && (
                <tr>
                  <td colSpan="3" style={{ textAlign: 'center', padding: '30px' }}>No specializations found.</td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>

      {isModalOpen && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.6)', 
          zIndex: 1000, backdropFilter: 'blur(4px)',
          overflowY: 'auto',
          padding: '40px 20px'
        }}>
          <div className="glass-panel animate-fade-in" style={{ 
            width: '100%', maxWidth: '500px', 
            padding: '30px', 
            margin: '0 auto' 
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
              <h3 style={{ margin: 0 }}>{editingId ? 'Edit' : 'Add'} Specialization</h3>
              <button onClick={closeModal} style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}>
                <X size={24} />
              </button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Specialization Name</label>
                <input 
                  type="text" 
                  className="form-input" 
                  value={formData.specialization_name}
                  onChange={(e) => setFormData({ ...formData, specialization_name: e.target.value })}
                  required
                />
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '30px' }}>
                <button type="button" className="btn btn-secondary" onClick={closeModal}>Cancel</button>
                <button type="submit" className="btn btn-primary" disabled={submitting}>
                  {submitting ? 'Saving...' : 'Save'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Specializations;
