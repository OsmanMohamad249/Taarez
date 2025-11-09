// lib/api/categories.ts
import { apiClient } from './config';
import { Category } from '../types';

/**
 * Category management API service
 */
export const categoriesApi = {
  /**
   * Get all categories
   */
  async getCategories(): Promise<Category[]> {
    const response = await apiClient.get<Category[]>('/categories');
    return response.data;
  },

  /**
   * Get category by ID
   */
  async getCategoryById(id: string): Promise<Category> {
    const response = await apiClient.get<Category>(`/categories/${id}`);
    return response.data;
  },
};
