import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '/api';

// Create axios instance with default config
const axiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth
axiosInstance.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
axiosInstance.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.message || error.response?.data?.error || error.message;
    return Promise.reject(new Error(message));
  }
);

// Helper function to add fallback data to products
const enhanceProduct = (product) => {
  if (!product) return product;
  
  // Add missing fields that frontend expects
  return {
    ...product,
    // Convert price to number if it's a string
    price: typeof product.price === 'string' ? parseFloat(product.price) : product.price,
    // Ensure stock is a number
    stock: typeof product.stock === 'string' ? parseInt(product.stock) : product.stock,
    // Add currency if missing
    currency: product.currency || 'KSh'
  };
};

export const api = {
  auth: {
    login: (credentials) => axiosInstance.post('/auth/login', credentials),
    register: (userData) => axiosInstance.post('/auth/register', userData),
    logout: () => axiosInstance.post('/auth/logout'),
    getSession: () => axiosInstance.get('/auth/session'),
    getProfile: () => axiosInstance.get('/auth/profile'),
    updateProfile: (data) => axiosInstance.put('/auth/profile', data),
    changePassword: (data) => axiosInstance.post('/auth/change-password', data),
  },

  users: {
    getAll: async () => {
      try {
        return await axiosInstance.get('/users/');
      } catch (error) {
        console.warn('Users endpoint failed, returning empty array');
        return [];
      }
    },
    getById: (id) => axiosInstance.get(`/users/${id}`),
    update: (id, data) => axiosInstance.put(`/users/${id}`, data),
    updatePaymentMethod: (id, data) => axiosInstance.put(`/users/${id}/payment-method`, data),
  },

  products: {
    getAll: async (params) => {
      try {
        const products = await axiosInstance.get('/products/', { params });
        return Array.isArray(products) ? products.map(enhanceProduct) : products;
      } catch (error) {
        console.error('Products fetch failed:', error);
        throw error;
      }
    },
    getById: async (id) => {
      try {
        const product = await axiosInstance.get(`/products/${id}`);
        return enhanceProduct(product);
      } catch (error) {
        console.error('Product fetch failed:', error);
        throw error;
      }
    },
    create: (data) => axiosInstance.post('/products/', data),
    update: (id, data) => axiosInstance.put(`/products/${id}`, data),
    delete: (id) => axiosInstance.delete(`/products/${id}`),
  },

  categories: {
    _cache: null,
    getAll: async function() {
      if (this._cache) return this._cache;
      
      try {
        const result = await axiosInstance.get('/categories/');
        this._cache = result;
        return result;
      } catch (error) {
        console.warn('Categories endpoint failed, using fallback');
        const fallback = [
          { id: 1, name: 'Pottery', description: 'Handmade ceramic items' },
          { id: 2, name: 'Textiles', description: 'Woven fabrics and clothing' },
          { id: 3, name: 'Wood Crafts', description: 'Carved wooden items' },
          { id: 4, name: 'Jewelry', description: 'Handcrafted jewelry' },
          { id: 5, name: 'Baskets', description: 'Woven baskets and containers' }
        ];
        this._cache = fallback;
        return fallback;
      }
    },
    getById: (id) => axiosInstance.get(`/categories/${id}`),
    create: (data) => axiosInstance.post('/categories/', data),
    update: (id, data) => axiosInstance.put(`/categories/${id}`, data),
    delete: (id) => axiosInstance.delete(`/categories/${id}`),
  },

  payments: {
    getAll: () => axiosInstance.get('/payments/'),
    create: (data) => axiosInstance.post('/payments/', data),
    getById: (id) => axiosInstance.get(`/payments/${id}`),
    update: (id, data) => axiosInstance.put(`/payments/${id}`, data),
    delete: (id) => axiosInstance.delete(`/payments/${id}`),
    initiate: (data) => axiosInstance.post('/payments/initiate', data),
    getStatus: (id) => axiosInstance.get(`/payments/status/${id}`),
    mpesa: {
      stkPush: (data) => axiosInstance.post('/payments/mpesa/stk-push', data),
      callback: (data) => axiosInstance.post('/payments/mpesa/callback', data),
      query: (checkoutRequestId) => axiosInstance.get(`/payments/mpesa/query/${checkoutRequestId}`),
    },
  },
};