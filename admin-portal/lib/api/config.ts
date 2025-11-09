// lib/api/config.ts
import axios from 'axios';

// API Configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
export const API_V1_PREFIX = '/api/v1';
export const API_URL = `${API_BASE_URL}${API_V1_PREFIX}`;

// Create axios instance with default config
export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor to add JWT token
apiClient.interceptors.request.use(
  (config) => {
    // Get token from localStorage or session storage
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      
      if (status === 401) {
        // Unauthorized - clear token and redirect to login
        if (typeof window !== 'undefined') {
          localStorage.removeItem('access_token');
          window.location.href = '/auth/login';
        }
      }
      
      return Promise.reject({
        detail: error.response.data?.detail || 'An error occurred',
        status_code: status,
      });
    } else if (error.request) {
      // Request made but no response received
      return Promise.reject({
        detail: 'Network error - please check your connection',
        status_code: 0,
      });
    } else {
      // Something else happened
      return Promise.reject({
        detail: error.message || 'An unexpected error occurred',
        status_code: 0,
      });
    }
  }
);
