// lib/api/designs.ts
import { apiClient } from './config';
import { Design, PaginatedResponse } from '../types';

interface CreateDesignData {
  title: string;
  description: string;
  style_type: string;
  price: number;
  image_url: string;
  category_id: string;
}

interface UpdateDesignData {
  title?: string;
  description?: string;
  style_type?: string;
  price?: number;
  image_url?: string;
  category_id?: string;
}

/**
 * Design management API service
 */
export const designsApi = {
  /**
   * Get all designs with pagination
   */
  async getDesigns(page: number = 1, perPage: number = 20): Promise<PaginatedResponse<Design>> {
    const response = await apiClient.get<PaginatedResponse<Design>>('/designs', {
      params: { page, per_page: perPage },
    });
    return response.data;
  },

  /**
   * Get design by ID
   */
  async getDesignById(id: string): Promise<Design> {
    const response = await apiClient.get<Design>(`/designs/${id}`);
    return response.data;
  },

  /**
   * Create new design
   */
  async createDesign(data: CreateDesignData): Promise<Design> {
    const response = await apiClient.post<Design>('/designs', data);
    return response.data;
  },

  /**
   * Update design
   */
  async updateDesign(id: string, data: UpdateDesignData): Promise<Design> {
    const response = await apiClient.put<Design>(`/designs/${id}`, data);
    return response.data;
  },

  /**
   * Delete design
   */
  async deleteDesign(id: string): Promise<void> {
    await apiClient.delete(`/designs/${id}`);
  },
};
