// lib/api/config.ts
import axios from 'axios';
import { env } from '../utils/env';

// API Configuration using validated environment variables
export const API_BASE_URL = env.apiBaseUrl;
export const API_V1_PREFIX = env.apiV1Prefix;
export const API_URL = env.apiUrl;

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
      const detail = error.response.data?.detail || 'An error occurred';
      
      // Log errors in development
      if (env.isDevelopment) {
        console.error('API Error:', {
          status,
          detail,
          url: error.config?.url,
          method: error.config?.method,
        });
      }
      
      if (status === 401) {
        // Unauthorized - clear token and redirect to login
        if (typeof window !== 'undefined') {
          localStorage.removeItem('access_token');
          // Only redirect if not already on login page
          if (!window.location.pathname.includes('/login')) {
            window.location.href = '/login';
          }
        }
      }
      
      return Promise.reject({
        detail,
        status_code: status,
      });
    } else if (error.request) {
      // Request made but no response received
      if (env.isDevelopment) {
        console.error('Network Error:', error.message);
      }
      return Promise.reject({
        detail: 'Network error - please check your connection',
        status_code: 0,
      });
    } else {
      // Something else happened
      if (env.isDevelopment) {
        console.error('Unexpected Error:', error.message);
      }
      return Promise.reject({
        detail: error.message || 'An unexpected error occurred',
        status_code: 0,
      });
    }
  }
);
