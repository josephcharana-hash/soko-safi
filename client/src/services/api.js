const API_URL = import.meta.env.VITE_API_URL ;

// API request helper with comprehensive error handling
const apiRequest = async (endpoint, options = {}) => {
  try {
    const url = `${API_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
    console.log(`[API] Making ${options.method || 'GET'} request to: ${url}`);
    
    const config = {
      method: 'GET',
      headers: options.headers || {},
      credentials: 'include', // Always include credentials for session-based auth
      timeout: 10000, // 10 second timeout
      ...options
    };
    
    // Only set Content-Type for non-FormData requests
    if (!(options.body instanceof FormData) && !config.headers['Content-Type']) {
      config.headers['Content-Type'] = 'application/json';
    }

    // Log request details for debugging
    if (options.body && config.method !== 'GET') {
      console.log(`[API] Request body:`, options.body instanceof FormData ? 'FormData' : options.body);
    }

    const response = await fetch(url, config);
    console.log(`[API] Response status: ${response.status} for ${endpoint}`);
    
    // Handle non-JSON responses
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      if (!response.ok) {
        // For DELETE requests, 500 errors might still mean success
        if (config.method === 'DELETE' && response.status === 500) {
          return { success: true, message: 'Deleted' };
        }
        throw new Error(`Server error: ${response.status} ${response.statusText}`);
      }
      return { success: true };
    }

    const data = await response.json();
    console.log(`[API] Response data for ${endpoint}:`, data);
    
    if (!response.ok) {
      // For DELETE requests, treat 500 errors as success silently
      if (config.method === 'DELETE' && response.status === 500) {
        return { success: true, message: 'Deleted' };
      }
      
      // Handle authentication errors
      if (response.status === 401) {
        console.warn('[API] Authentication required');
        throw new Error('Please log in to continue');
      }
      
      throw new Error(data.message || data.error || `HTTP ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error(`[API] Error for ${endpoint}:`, error.message);
    
    // Check if it's a network error
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      console.warn(`[API] Network error - backend may be unavailable`);
      throw new Error('Backend server is currently unavailable. Please try again later.');
    }
    
    throw error;
  }
};

// Helper to enhance product data
const enhanceProduct = (product) => {
  if (!product) return product;
  return {
    ...product,
    price: typeof product.price === 'string' ? parseFloat(product.price) : product.price,
    stock: typeof product.stock === 'string' ? parseInt(product.stock) : product.stock,
    currency: product.currency || 'KSh',
    image: product.image || `https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop&crop=center`,
    artisan_name: product.artisan_name || 'Unknown Artisan',
    location: product.location || 'Kenya',
    rating: product.rating || 4.5,
    review_count: product.review_count || 0,
    in_stock: product.stock > 0
  };
};

export const api = {
  // Authentication endpoints
  auth: {
    login: (credentials) => apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    }),
    register: async (userData) => {
      try {
        return await apiRequest('/auth/register', {
          method: 'POST',
          body: JSON.stringify(userData),
        });
      } catch (error) {
        console.error('[AUTH] Registration failed:', error.message);
        throw error;
      }
    },
    logout: () => apiRequest('/auth/logout', { method: 'POST' }),
    getSession: () => apiRequest('/auth/session'),
    getProfile: () => apiRequest('/auth/profile'),
    updateProfile: (data) => apiRequest('/auth/profile', {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
    changePassword: (data) => apiRequest('/auth/change-password', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  },

  // User management endpoints
  users: {
    getAll: () => apiRequest('/users/'),
    getById: (id) => apiRequest(`/users/${id}`),
    update: (id, data) => apiRequest(`/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
  },

  // Product endpoints
  products: {
    getAll: async (params) => {
      const query = params ? '?' + new URLSearchParams(params).toString() : '';
      const products = await apiRequest(`/products/${query}`);
      return Array.isArray(products) ? products.map(enhanceProduct) : [];
    },
    getById: async (id) => {
      const product = await apiRequest(`/products/${id}`);
      return enhanceProduct(product);
    },
    create: (data) => apiRequest('/products/', {
      method: 'POST',
      body: data instanceof FormData ? data : JSON.stringify(data),
    }),
    update: (id, data) => apiRequest(`/products/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
    delete: (id) => apiRequest(`/products/${id}`, { method: 'DELETE' }),
  },

  // Category endpoints
  categories: {
    getAll: async () => {
      try {
        return await apiRequest('/categories/')
      } catch (error) {
        console.warn('Categories failed:', error.message)
        return []
      }
    },
    getById: (id) => apiRequest(`/categories/${id}`),
    create: (data) => apiRequest('/categories/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    update: (id, data) => apiRequest(`/categories/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
    delete: (id) => apiRequest(`/categories/${id}`, { method: 'DELETE' }),
    
    // Subcategory endpoints
    subcategories: {
      getAll: async () => {
        try {
          return await apiRequest('/categories/subcategories/')
        } catch (error) {
          console.warn('Subcategories failed:', error.message)
          return []
        }
      },
      getById: (id) => apiRequest(`/categories/subcategories/${id}`),
      create: (data) => apiRequest('/categories/subcategories/', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
      update: (id, data) => apiRequest(`/categories/subcategories/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      }),
      delete: (id) => apiRequest(`/categories/subcategories/${id}`, { method: 'DELETE' }),
    }
  },

  // Cart endpoints
  cart: {
    get: async () => {
      const result = await apiRequest('/cart/')
      console.log('Cart get result:', result)
      // Backend returns array of cart items directly
      return { items: result, cart_items: result }
    },
    add: async (productId, quantity = 1) => {
      console.log('API: Adding to cart', { productId, quantity })
      console.log('API: Request payload:', { product_id: productId, quantity })
      const result = await apiRequest('/cart/', {
        method: 'POST',
        body: JSON.stringify({ product_id: productId, quantity }),
      })
      console.log('API: Cart add successful', result)
      return result
    },
    update: (itemId, quantity) => apiRequest(`/cart/${itemId}`, {
      method: 'PUT',
      body: JSON.stringify({ quantity }),
    }),
    remove: (itemId) => apiRequest(`/cart/${itemId}`, { method: 'DELETE' }),
    clear: () => apiRequest('/cart/clear', { method: 'DELETE' }),
  },

  // Order endpoints
  orders: {
    getAll: async () => {
      try {
        return await apiRequest('/orders/')
      } catch (error) {
        console.warn('Orders failed:', error.message)
        return []
      }
    },
    getById: (id) => apiRequest(`/orders/${id}`),
    create: (orderData) => apiRequest('/orders/', {
      method: 'POST',
      body: JSON.stringify(orderData),
    }),
    createItem: (itemData) => apiRequest('/orders/items/', {
      method: 'POST',
      body: JSON.stringify(itemData),
    }),
    updateStatus: (id, status) => apiRequest(`/orders/${id}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    }),
  },

  // Review endpoints
  reviews: {
    getByProduct: (productId) => apiRequest(`/reviews/product/${productId}`),
    create: (data) => apiRequest('/reviews/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    update: (id, data) => apiRequest(`/reviews/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
    delete: (id) => apiRequest(`/reviews/${id}`, { method: 'DELETE' }),
  },

  // Message endpoints
  messages: {
    getConversations: async () => {
      try {
        return await apiRequest('/messages/conversations')
      } catch (error) {
        console.warn('Messages failed:', error.message)
        return []
      }
    },
    getMessages: (userId) => apiRequest(`/messages/${userId}`),
    send: (receiverId, content) => apiRequest('/messages/', {
      method: 'POST',
      body: JSON.stringify({ receiver_id: receiverId, content }),
    }),
  },

  // Favorite endpoints
  favorites: {
    getAll: async () => {
      try {
        return await apiRequest('/favorites/')
      } catch (error) {
        console.warn('Favorites failed:', error.message)
        return []
      }
    },
    add: (productId) => apiRequest('/favorites/', {
      method: 'POST',
      body: JSON.stringify({ product_id: productId }),
    }),
    remove: (productId) => apiRequest(`/favorites/${productId}`, { method: 'DELETE' }),
  },

  // Follow endpoints
  follows: {
    follow: (artisanId) => apiRequest('/follows/', {
      method: 'POST',
      body: JSON.stringify({ artisan_id: artisanId }),
    }),
    unfollow: (artisanId) => apiRequest(`/follows/${artisanId}`, { method: 'DELETE' }),
    getFollowing: () => apiRequest('/follows/following'),
    getFollowers: () => apiRequest('/follows/followers'),
  },

  // Notification endpoints
  notifications: {
    getAll: () => apiRequest('/notifications/'),
    markAsRead: (id) => apiRequest(`/notifications/${id}/read`, { method: 'PUT' }),
    markAllAsRead: () => apiRequest('/notifications/read-all', { method: 'PUT' }),
  },

  // Artisan endpoints
  artisan: {
    getProfile: (id) => apiRequest(`/artisan/${id}`),
    getProducts: (id) => apiRequest(`/artisan/${id}/products`),
    updateProfile: (data) => apiRequest('/artisan/profile', {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
    getDashboard: async () => {
      try {
        return await apiRequest('/artisan/dashboard')
      } catch (error) {
        console.warn('Artisan dashboard failed:', error.message)
        return { stats: { total_products: 0, total_orders: 0, total_revenue: 0 } }
      }
    },
    getOrders: async () => {
      try {
        return await apiRequest('/artisan/orders')
      } catch (error) {
        console.warn('Artisan orders failed:', error.message)
        return []
      }
    },
    getMessages: async () => {
      try {
        return await apiRequest('/artisan/messages')
      } catch (error) {
        console.warn('Artisan messages failed:', error.message)
        return []
      }
    },
  },

  // User profile endpoints
  profile: {
    get: async () => {
      try {
        const response = await apiRequest('/auth/profile')
        // Backend returns { user: { ... } }, extract the user data
        return response.user || { full_name: '', description: '', location: '', phone: '', profile_picture_url: '' }
      } catch (error) {
        console.warn('Profile get failed:', error.message)
        return { full_name: '', description: '', location: '', phone: '', profile_picture_url: '' }
      }
    },
    update: async (data) => {
      const response = await apiRequest('/auth/profile', {
        method: 'PUT',
        body: JSON.stringify(data),
      })
      // Backend returns { user: { ... } }, extract the user data
      return response.user || response
    },
    uploadImage: async (file) => {
      // Use Cloudinary directly for profile pictures
      const { uploadToCloudinary } = await import('./cloudinary');
      return uploadToCloudinary(file);
    },
  },

  // Payment endpoints
  payments: {
    getAll: async () => {
      try {
        return await apiRequest('/payments/')
      } catch (error) {
        console.warn('Payments failed:', error.message)
        return []
      }
    },
    create: (data) => apiRequest('/payments/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    getById: (id) => apiRequest(`/payments/${id}`),
    initiate: (data) => apiRequest('/payments/initiate', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    getStatus: (id) => apiRequest(`/payments/status/${id}`),
    mpesa: {
      stkPush: (data) => apiRequest('/payments/initiate', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    },
  },

  // Upload endpoints
  upload: {
    image: async (file) => {
      // Use Cloudinary directly for better performance
      const { uploadToCloudinary } = await import('./cloudinary');
      return uploadToCloudinary(file);
    },
  },
};
