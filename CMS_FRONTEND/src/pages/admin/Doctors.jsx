import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Plus, Edit2, X } from 'lucide-react';

const Doctors = () => {
  const [doctors, setDoctors] = useState([]);
  const [staffList, setStaffList] = useState([]);
  const [specsList, setSpecsList] = useState([]);
  const [loading, setLoading] = useState(true);

  // Modal state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({ staff: '', specialization: '', consultation_fee: '' });
  const [editingId, setEditingId] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [docsRes, staffRes, specsRes] = await Promise.all([
        api.get('doctors/'),
        api.get('staff/'),
        api.get('specializations/')
      ]);
      setDoctors(docsRes.data);
      // Ideally filter staff by role doctor
      setStaffList(staffRes.data); 
      setSpecsList(specsRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const openModal = (doc = null) => {
    if (doc) {
      setEditingId(doc.id);
      setFormData({ 
        staff: doc.staff, 
        specialization: doc.specialization, 
        consultation_fee: doc.consultation_fee 
      });
    } else {
      setEditingId(null);
      setFormData({ staff: '', specialization: '', consultation_fee: '' });
    }
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setFormData({ staff: '', specialization: '', consultation_fee: '' });
    setEditingId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      if (editingId) {
        await api.put(`doctors/update/${editingId}/`, formData);
      } else {
        await api.post('doctors/create/', formData);
      }
      closeModal();
      fetchData();
    } catch (err) {
      alert("Error saving doctor: " + (err.response?.data?.detail || JSON.stringify(err.response?.data)));
    } finally {
      setSubmitting(false);
    }
  };

  const getStaffName = (staffId) => {
    const s = staffList.find(x => x.id === staffId);
    return s ? `${s.first_name} ${s.last_name}` : staffId;
  };

  const getSpecName = (specId) => {
    const s = specsList.find(x => x.id === specId);
    return s ? s.specialization_name : specId;
  };

  return (
    <div className="animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
        <h2>Doctors</h2>
        <button className="btn btn-primary" onClick={() => openModal()}>
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
                <th>Staff Name</th>
                <th>Specialization</th>
                <th>Consultation Fee</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {doctors.map((doc) => (
                <tr key={doc.id} style={{ opacity: doc.is_active ? 1 : 0.6 }}>
                  <td>{doc.id}</td>
                  <td>{getStaffName(doc.staff)}</td>
                  <td>{getSpecName(doc.specialization)}</td>
                  <td>${doc.consultation_fee}</td>
                  <td>
                    <span className={`badge ${doc.is_active ? 'badge-success' : 'badge-danger'}`}>
                      {doc.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>
                    <button className="btn btn-secondary" style={{ padding: '6px' }} onClick={() => openModal(doc)}>
                      <Edit2 size={16} />
                    </button>
                  </td>
                </tr>
              ))}
              {doctors.length === 0 && (
                <tr>
                  <td colSpan="6" style={{ textAlign: 'center', padding: '30px' }}>No doctors found.</td>
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
              <h3 style={{ margin: 0 }}>{editingId ? 'Edit' : 'Add'} Doctor</h3>
              <button onClick={closeModal} style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}>
                <X size={24} />
              </button>
            </div>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Staff Member</label>
                <select 
                  className="form-input" 
                  value={formData.staff}
                  onChange={(e) => setFormData({ ...formData, staff: e.target.value })}
                  required
                >
                  <option value="">Select Staff</option>
                  {staffList.filter(s => s.is_active).map(s => (
                    <option key={s.id} value={s.id}>{s.first_name} {s.last_name} ({s.emp_id})</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Specialization</label>
                <select 
                  className="form-input" 
                  value={formData.specialization}
                  onChange={(e) => setFormData({ ...formData, specialization: e.target.value })}
                  required
                >
                  <option value="">Select Specialization</option>
                  {specsList.map(s => (
                    <option key={s.id} value={s.id}>{s.specialization_name}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Consultation Fee</label>
                <input 
                  type="number" 
                  step="0.01"
                  className="form-input" 
                  value={formData.consultation_fee}
                  onChange={(e) => setFormData({ ...formData, consultation_fee: e.target.value })}
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

export default Doctors;
