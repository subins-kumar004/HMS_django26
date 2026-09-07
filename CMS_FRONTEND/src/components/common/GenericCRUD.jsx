import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Plus, Edit2, X, Trash2 } from 'lucide-react';

const GenericCRUD = ({ title, endpoint, endpoints, fields }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      let fetchUrl = '';
      if (endpoints && endpoints.list) {
        fetchUrl = endpoints.list;
      } else {
        fetchUrl = endpoint.includes('?') ? endpoint : `${endpoint.replace(/\/$/, '')}/`;
      }
      const res = await api.get(fetchUrl);
      setData(Array.isArray(res.data) ? res.data : [res.data]);
    } catch (err) {
      setError(err.message || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [endpoint]);

  const openModal = (item = null) => {
    if (item) {
      setEditingId(item.id);
      setFormData(item);
    } else {
      setEditingId(null);
      const initialData = {};
      fields.forEach(f => {
        initialData[f.name] = f.type === 'checkbox' ? false : '';
      });
      setFormData(initialData);
    }
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setFormData({});
    setEditingId(null);
  };

  const handleInputChange = (e, field) => {
    const value = field.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({ ...formData, [field.name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      let requestUrl = '';
      if (editingId) {
        // Update
        if (endpoints && endpoints.update) {
          requestUrl = endpoints.update.replace(':id', editingId);
        } else {
          requestUrl = `${endpoint.replace(/\/$/, '')}/${editingId}/`;
        }
        await api.put(requestUrl, formData);
      } else {
        // Create
        if (endpoints && endpoints.create) {
          requestUrl = endpoints.create;
        } else {
          requestUrl = `${endpoint.replace(/\/$/, '')}/`;
        }
        await api.post(requestUrl, formData);
      }
      closeModal();
      fetchData(); // Refresh list
    } catch (err) {
      alert("Error: " + (err.response?.data?.detail || JSON.stringify(err.response?.data) || err.message));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
        <h2>{title}</h2>
        <button className="btn btn-primary" onClick={() => openModal()}>
          <Plus size={18} /> Add New
        </button>
      </div>

      {/* Table */}
      <div className="glass-panel table-container">
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center' }}>Loading...</div>
        ) : error ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--danger)' }}>{error}</div>
        ) : data.length === 0 ? (
          <div style={{ padding: '40px', textAlign: 'center' }}>No records found.</div>
        ) : (
          <table className="custom-table">
            <thead>
              <tr>
                {fields.map(f => (
                  <th key={f.name}>{f.label}</th>
                ))}
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {data.map((item) => (
                <tr key={item.id}>
                  {fields.map(f => (
                    <td key={f.name}>
                      {f.type === 'checkbox' 
                        ? <span className={`badge ${item[f.name] ? 'badge-success' : 'badge-danger'}`}>{item[f.name] ? 'Yes' : 'No'}</span>
                        : item[f.name] === null ? 'N/A' : String(item[f.name])}
                    </td>
                  ))}
                  <td>
                    <button className="btn btn-secondary" style={{ padding: '6px' }} onClick={() => openModal(item)}>
                      <Edit2 size={16} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Modal */}
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
              <h3 style={{ margin: 0 }}>{editingId ? 'Edit' : 'Add'} {title.replace(/s$/, '')}</h3>
              <button onClick={closeModal} style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}>
                <X size={24} />
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              {fields.map(f => (
                <div key={f.name} className="form-group" style={{ display: f.type === 'checkbox' ? 'flex' : 'block', alignItems: 'center', gap: '10px' }}>
                  {f.type !== 'checkbox' && <label className="form-label">{f.label}</label>}
                  
                  {f.type === 'select' ? (
                    <select 
                      className="form-input" 
                      value={formData[f.name] || ''} 
                      onChange={(e) => handleInputChange(e, f)}
                      required={f.required !== false}
                    >
                      <option value="">Select {f.label}</option>
                      {f.options?.map(opt => (
                        <option key={opt.value} value={opt.value}>{opt.label}</option>
                      ))}
                    </select>
                  ) : f.type === 'textarea' ? (
                    <textarea 
                      className="form-input" 
                      value={formData[f.name] || ''} 
                      onChange={(e) => handleInputChange(e, f)}
                      required={f.required !== false}
                      rows="3"
                    />
                  ) : (
                    <input 
                      type={f.type || 'text'} 
                      className={f.type === 'checkbox' ? '' : 'form-input'} 
                      checked={f.type === 'checkbox' ? !!formData[f.name] : undefined}
                      value={f.type !== 'checkbox' ? formData[f.name] || '' : undefined}
                      onChange={(e) => handleInputChange(e, f)}
                      required={f.type !== 'checkbox' && f.required !== false}
                      style={f.type === 'checkbox' ? { width: '20px', height: '20px', accentColor: 'var(--accent-primary)' } : {}}
                    />
                  )}
                  {f.type === 'checkbox' && <label className="form-label" style={{ margin: 0 }}>{f.label}</label>}
                </div>
              ))}

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

export default GenericCRUD;
