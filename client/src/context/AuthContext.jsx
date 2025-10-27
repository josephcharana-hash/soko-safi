import { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const data = await api.auth.getSession();
      if (data.authenticated) setUser(data.user);
    } catch (error) {
      // Silently fail if backend is not running
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    const data = await api.auth.login(credentials);
    setUser(data.user);
    return data;
  };

  const register = async (userData) => {
    const data = await api.auth.register(userData);
    setUser(data.user);
    return data;
  };

  const logout = async () => {
    await api.auth.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
