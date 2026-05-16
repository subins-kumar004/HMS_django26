import React, { useState, useEffect } from 'react';
import { Pill, AlertTriangle, Archive, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../../services/api';

const Dashboard = () => {
  const [medicines, setMedicines] = useState([]);
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [medRes, invRes] = await Promise.all([
          api.get('pharmacist/medicines/'), // Assuming trailing slash based on GenericCRUD setup
          api.get('pharmacist/inventory/')
        ]);
        setMedicines(medRes.data || []);
        setInventory(invRes.data || []);
      } catch (err) {
        console.error("Dashboard fetch error:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const lowStockItems = inventory.filter(inv => inv.quantity <= inv.reorder_level);

  if (loading) {
    return <div style={{ padding: '40px', textAlign: 'center' }}>Loading Dashboard...</div>;
  }

  return (
    <div className="animate-fade-in">
      <h2 style={{ marginBottom: '20px' }}>Pharmacist Overview</h2>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '30px' }}>
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div style={{ padding: '15px', borderRadius: '50%', backgroundColor: 'rgba(0, 191, 165, 0.1)' }}>
            <Pill size={28} color="var(--accent-primary)" />
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '24px' }}>{medicines.length}</h3>
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Total Medicines</p>
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '15px', borderColor: lowStockItems.length > 0 ? 'rgba(255,82,82,0.5)' : undefined }}>
          <div style={{ padding: '15px', borderRadius: '50%', backgroundColor: lowStockItems.length > 0 ? 'rgba(255, 82, 82, 0.1)' : 'rgba(0, 191, 165, 0.1)' }}>
            <AlertTriangle size={28} color={lowStockItems.length > 0 ? "var(--danger)" : "var(--accent-primary)"} />
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '24px', color: lowStockItems.length > 0 ? "var(--danger)" : "inherit" }}>{lowStockItems.length}</h3>
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Low Stock Alerts</p>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h3 style={{ margin: 0 }}>Inventory Items</h3>
            <Link to="/pharmacist/inventory" style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '14px' }}>
              View All <ArrowRight size={14} />
            </Link>
          </div>
          {inventory.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)' }}>No inventory found.</p>
          ) : (
            <table className="custom-table">
              <thead>
                <tr>
                  <th>Medicine ID</th>
                  <th>Quantity</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {inventory.slice(0, 5).map(inv => (
                  <tr key={inv.id}>
                    <td>{inv.medicine}</td>
                    <td>{inv.quantity}</td>
                    <td>
                      {inv.quantity <= inv.reorder_level ? (
                        <span className="badge badge-danger">Low Stock</span>
                      ) : (
                        <span className="badge badge-success">Sufficient</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 style={{ margin: 0, marginBottom: '20px' }}>Quick Actions</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <Link to="/pharmacist/inventory" className="btn btn-primary" style={{ justifyContent: 'flex-start' }}>
              <Archive size={18} /> Update Stock
            </Link>
            <Link to="/pharmacist/medicines" className="btn btn-secondary" style={{ justifyContent: 'flex-start' }}>
              <Pill size={18} /> Manage Catalog
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
