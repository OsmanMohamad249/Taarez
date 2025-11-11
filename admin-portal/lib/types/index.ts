// lib/types/index.ts
/**
 * Shared TypeScript interfaces for the Taarez admin portal
 */

export type UserRole = 'customer' | 'designer' | 'admin' | 'tailor';

export interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  is_superuser: boolean;
  role: UserRole;
  created_at: string;
}

export interface Design {
  id: string;
  title: string;
  description: string;
  style_type: string;
  price: number;
  image_url: string;
  designer_id: string;
  category_id: string;
  created_at: string;
}

export interface Category {
  id: string;
  name: string;
  description: string;
  image_url?: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface ApiError {
  detail: string;
  status_code?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}
