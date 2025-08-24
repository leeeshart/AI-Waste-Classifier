// Environment configuration for production builds
const config = {
  development: {
    API_BASE_URL: 'http://localhost:5000',
    API_TIMEOUT: 30000,
    MAX_FILE_SIZE_MB: 16,
    ENABLE_DEBUG: true,
    SENTRY_DSN: '',
  },
  production: {
    API_BASE_URL: process.env.VITE_API_BASE_URL || 'https://api.ecosort.app',
    API_TIMEOUT: 60000,
    MAX_FILE_SIZE_MB: 16,
    ENABLE_DEBUG: false,
    SENTRY_DSN: process.env.VITE_SENTRY_DSN || '',
  }
};

const environment = process.env.NODE_ENV || 'development';

export default {
  ...config[environment],
  NODE_ENV: environment,
  VERSION: process.env.npm_package_version || '1.0.0',
  BUILD_TIME: process.env.VITE_BUILD_TIME || new Date().toISOString(),
};