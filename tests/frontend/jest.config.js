/**
 * Jest Configuration for Piper Morgan Frontend Tests
 *
 * Tests vanilla JavaScript files in web/static/js/
 * Uses jsdom for DOM simulation
 */

module.exports = {
  // Use jsdom for DOM testing
  testEnvironment: 'jsdom',

  // Run setup file before each test
  setupFilesAfterEnv: ['./setup.js'],

  // Test file patterns
  testMatch: ['**/unit/**/*.test.js'],

  // Root directory for tests
  rootDir: '.',

  // Source files for coverage reporting
  collectCoverageFrom: [
    '../../web/static/js/**/*.js',
    '!../../web/static/js/**/*.min.js'
  ],

  // Coverage output directory
  coverageDirectory: './coverage',

  // Coverage thresholds (start conservative, increase over time)
  coverageThreshold: {
    global: {
      statements: 10,
      branches: 10,
      functions: 10,
      lines: 10
    }
  },

  // Module resolution
  moduleDirectories: ['node_modules'],

  // Clear mocks between tests
  clearMocks: true,

  // Verbose output for debugging
  verbose: true,

  // Test timeout (5 seconds)
  testTimeout: 5000
};
