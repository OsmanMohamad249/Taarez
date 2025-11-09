// lib/api/auth.ts
import { apiClient } from './config';
import { AuthResponse, User } from '../types';

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
  role?: 'customer' | 'designer' | 'admin' | 'tailor';
}

/**
 * Authentication API service
 */
export const authApi = {
  /**
   * Login user
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      // OAuth2 format expects form data
      const formData = new URLSearchParams();
      formData.append('username', credentials.email);
      formData.append('password', credentials.password);
      
      const response = await apiClient.post<AuthResponse>('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      
      // Store token in localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', response.data.access_token);
      }
      
      return response.data;
    } catch (error: any) {
      // Re-throw with better error message
      throw {
        detail: error.detail || 'Login failed. Please check your credentials.',
        status_code: error.status_code || 500,
      };
    }
  },

  /**
   * Register new user
   */
  async register(data: RegisterData): Promise<User> {
    try {
      const response = await apiClient.post<User>('/auth/register', data);
      return response.data;
    } catch (error: any) {
      throw {
        detail: error.detail || 'Registration failed. Please try again.',
        status_code: error.status_code || 500,
      };
    }
  },

  /**
   * Get current user
   */
  async getCurrentUser(): Promise<User> {
    try {
      const response = await apiClient.get<User>('/users/me');
      return response.data;
    } catch (error: any) {
      throw {
        detail: error.detail || 'Failed to fetch user information.',
        status_code: error.status_code || 500,
      };
    }
  },

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
  },
};
