import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Plus, Search, Edit2, UserX, X } from 'lucide-react';

const Staff = () => {
  const [staff, setStaff] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    username: '', first_name: '', last_name: '', email: '', 
    contact: '', gender: '', address: '', salary: '', 
    emp_id: '', role: '', password: ''
  });
  const [editingId, setEditingId] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const fetchStaff = async () => {
    try {
      setLoading(true);
      const [staffRes, rolesRes] = await Promise.all([
        api.get(`staff/${search ? `?search=${search}` : ''}`),
        api.get('roles/')
      ]);
      setStaff(staffRes.data);
      if (rolesRes.data) setRoles(rolesRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStaff();
  }, [search]);

  const handleDeactivate = async (id) => {
    if (window.confirm("Are you sure you want to deactivate this staff member?")) {
      try {
        await api.patch(`staff/deactivate/${id}/`);
        fetchStaff();
      } catch (err) {
        console.error(err);
      }
    }
  };

  const openModal = (member = null) => {
    if (member) {
      setEditingId(member.id);
      setFormData({
        username: member.username,
        first_name: member.first_name,
        last_name: member.last_name,
        email: member.email,
        contact: member.contact,
        gender: member.gender,
        address: member.address,
        salary: member.salary,
        emp_id: member.emp_id,
        role: member.role,
        password: '' // Don't populate password
      });
    } else {
      setEditingId(null);
      setFormData({
        username: '', first_name: '', last_name: '', email: '', 
        contact: '', gender: '', address: '', salary: '', 
        emp_id: '', role: '', password: ''
      });
    }
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditingId(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const dataToSubmit = { ...formData };
      if (editingId && !dataToSubmit.password) {
        delete dataToSubmit.password;
      }

      if (editingId) {
        await api.put(`staff/update/${editingId}/`, dataToSubmit);
      } else {
        await api.post('staff/create/', dataToSubmit);
      }
      closeModal();
      fetchStaff();
    } catch (err) {
      alert("Error saving staff: " + (err.response?.data?.detail || JSON.stringify(err.response?.data)));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div style={{ position: 'relative', width: '300px' }}>
          <Search size={18} color="var(--text-secondary)" style={{ position: 'absolute', top: '12px', left: '12px' }} />
          <input 
            type="text" 
            className="form-input" 
            placeholder="Search staff..." 
            style={{ paddingLeft: '40px' }}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <button className="btn btn-primary" onClick={() => openModal()}>
          <Plus size={18} /> Add Staff
        </button>
      </div>

      <div className="glass-panel table-container">
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center' }}>Loading...</div>
        ) : (
          <table className="custom-table">
            <thead>
              <tr>
                <th>Emp ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Contact</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {staff.map((member) => (
                <tr key={member.id} style={{ opacity: member.is_active ? 1 : 0.6 }}>
                  <td>{member.emp_id}</td>
                  <td>{member.username}</td>
                  <td>{member.email}</td>
                  <td>{member.contact}</td>
                  <td>
                    <span className={`badge ${member.is_active ? 'badge-success' : 'badge-danger'}`}>
                      {member.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '10px' }}>
                      <button className="btn btn-secondary" style={{ padding: '6px' }} title="Edit" onClick={() => openModal(member)}>
                        <Edit2 size={16} />
                      </button>
                      {member.is_active && (
                        <button 
                          className="btn btn-danger" 
                          style={{ padding: '6px' }} 
                          title="Deactivate"
                          onClick={() => handleDeactivate(member.id)}
                        >
                          <UserX size={16} />
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
              {staff.length === 0 && (
                <tr>
                  <td colSpan="6" style={{ textAlign: 'center', padding: '30px' }}>No staff found.</td>
                </tr>
              )}
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
            width: '100%', maxWidth: '800px', 
            padding: '30px', 
            margin: '0 auto' 
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
              <h3 style={{ margin: 0 }}>{editingId ? 'Edit' : 'Add'} Staff</h3>
              <button onClick={closeModal} style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}>
                <X size={24} />
              </button>
            </div>
            <form onSubmit={handleSubmit}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Username</label>
                  <input type="text" name="username" className="form-input" value={formData.username} onChange={handleInputChange} required />
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Password {editingId && '(Leave blank to keep)'}</label>
                  <input type="password" name="password" className="form-input" value={formData.password} onChange={handleInputChange} required={!editingId} />
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">First Name</label>
                  <input type="text" name="first_name" className="form-input" value={formData.first_name} onChange={handleInputChange} required />
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Last Name</label>
                  <input type="text" name="last_name" className="form-input" value={formData.last_name} onChange={handleInputChange} required />
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Email</label>
                  <input type="email" name="email" className="form-input" value={formData.email} onChange={handleInputChange} required />
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Contact Number</label>
                  <input type="text" name="contact" className="form-input" value={formData.contact} onChange={handleInputChange} />
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Gender</label>
                  <select name="gender" className="form-input" value={formData.gender} onChange={handleInputChange}>
                    <option value="">Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Role</label>
                  <select name="role" className="form-input" value={formData.role} onChange={handleInputChange}>
                    <option value="">Select Role</option>
                    {roles.map(r => (
                      <option key={r.id} value={r.id}>{r.role_name}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Salary</label>
                  <input type="number" name="salary" step="0.01" className="form-input" value={formData.salary} onChange={handleInputChange} />
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Employee ID</label>
                  <input type="text" name="emp_id" className="form-input" value={formData.emp_id} onChange={handleInputChange} />
                </div>
                <div className="form-group" style={{ gridColumn: 'span 2', marginBottom: 0 }}>
                  <label className="form-label">Address</label>
                  <textarea name="address" className="form-input" rows="2" value={formData.address} onChange={handleInputChange}></textarea>
                </div>
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

export default Staff;
