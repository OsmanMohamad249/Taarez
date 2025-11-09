// lib/utils/env.ts

/**
 * Environment configuration with validation
 */

/**
 * Get and validate required environment variable
 */
function getRequiredEnvVar(key: string, defaultValue?: string): string {
  const value = process.env[key] || defaultValue;
  
  if (!value) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
  
  return value;
}

/**
 * Get optional environment variable
 */
function getOptionalEnvVar(key: string, defaultValue: string): string {
  return process.env[key] || defaultValue;
}

/**
 * Validate environment configuration on startup
 */
export function validateEnv(): void {
  try {
    getRequiredEnvVar('NEXT_PUBLIC_API_BASE_URL', 'http://localhost:8000');
  } catch (error) {
    console.error('Environment validation failed:', error);
    throw error;
  }
}

/**
 * Environment configuration
 */
export const env = {
  // API Configuration
  apiBaseUrl: getRequiredEnvVar('NEXT_PUBLIC_API_BASE_URL', 'http://localhost:8000'),
  apiV1Prefix: '/api/v1',
  
  // Computed values
  get apiUrl() {
    return `${this.apiBaseUrl}${this.apiV1Prefix}`;
  },
  
  // NextAuth (future use)
  nextAuthUrl: getOptionalEnvVar('NEXTAUTH_URL', 'http://localhost:3000'),
  nextAuthSecret: getOptionalEnvVar('NEXTAUTH_SECRET', ''),
  
  // Environment
  isDevelopment: process.env.NODE_ENV === 'development',
  isProduction: process.env.NODE_ENV === 'production',
  isTest: process.env.NODE_ENV === 'test',
};

// Validate on module load
if (typeof window === 'undefined') {
  validateEnv();
}
