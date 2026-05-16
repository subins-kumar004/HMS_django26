import React, { createContext, useState, useEffect } from 'react';
import api from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const storedUser = localStorage.getItem('user');
    const token = localStorage.getItem('accessToken');
    
    if (storedUser && token) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      const response = await api.post('auth/login/', { username, password });
      
      const { access, refresh, user: returnedUser } = response.data;
      
      // Fallback role for superusers created via CLI who might not have a Role assigned
      const role = returnedUser.role || (username.toLowerCase() === 'admin' ? 'Admin' : 'Unknown');

      const userObj = {
        ...returnedUser,
        role: role
      };

      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
      localStorage.setItem('user', JSON.stringify(userObj));
      
      setUser(userObj);
      return { success: true, user: userObj };
    } catch (error) {
      console.error("Login failed:", error);
      return { 
        success: false, 
        error: error.response?.data?.error || error.response?.data?.detail || "Invalid credentials" 
      };
    }
  };

  const logout = () => {
    // Attempt backend logout if refresh token exists
    const refreshToken = localStorage.getItem('refreshToken');
    if (refreshToken) {
      api.post('auth/logout/', { refresh: refreshToken }).catch(e => console.log(e));
    }
    
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    setUser(null);
    window.location.href = '/login';
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
