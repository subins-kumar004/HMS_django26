import React from 'react';

const Header = ({ title }) => {
  return (
    <header className="glass-panel" style={{ 
      padding: '20px 30px', 
      marginBottom: '30px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      borderTop: 'none',
      borderRight: 'none',
      borderLeft: 'none',
      borderRadius: '0 0 12px 12px'
    }}>
      <div>
        <h1 style={{ fontSize: '24px', margin: 0 }}>{title}</h1>
      </div>
      <div>
        <span style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
          {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
        </span>
      </div>
    </header>
  );
};

export default Header;
