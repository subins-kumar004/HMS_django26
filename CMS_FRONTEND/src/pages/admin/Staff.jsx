import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Plus, Search, Edit2, UserX } from 'lucide-react';

const Staff = () => {
  const [staff, setStaff] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  const fetchStaff = async () => {
    try {
      const res = await api.get(`staff/${search ? `?search=${search}` : ''}`);
      setStaff(res.data);
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
        <button className="btn btn-primary">
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
                      <button className="btn btn-secondary" style={{ padding: '6px' }} title="Edit">
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
    </div>
  );
};

export default Staff;
