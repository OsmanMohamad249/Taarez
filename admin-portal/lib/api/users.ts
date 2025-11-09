// lib/api/users.ts
import { apiClient } from './config';
import { User, PaginatedResponse } from '../types';

interface UpdateUserData {
  first_name?: string;
  last_name?: string;
  email?: string;
}

/**
 * User management API service
 */
export const usersApi = {
  /**
   * Get all users (admin only)
   */
  async getUsers(page: number = 1, perPage: number = 20): Promise<PaginatedResponse<User>> {
    const response = await apiClient.get<PaginatedResponse<User>>('/users', {
      params: { page, per_page: perPage },
    });
    return response.data;
  },

  /**
   * Get user by ID
   */
  async getUserById(id: string): Promise<User> {
    const response = await apiClient.get<User>(`/users/${id}`);
    return response.data;
  },

  /**
   * Get current user
   */
  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<User>('/users/me');
    return response.data;
  },

  /**
   * Update user profile
   */
  async updateProfile(data: UpdateUserData): Promise<User> {
    const response = await apiClient.put<User>('/users/me', data);
    return response.data;
  },
};
