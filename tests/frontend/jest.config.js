module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  moduleNameMapping: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy'
  },
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest',
    '^.+\\.(js|jsx)$': 'babel-jest'
  },
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
  collectCoverageFrom: [
    '../../frontend/src/**/*.{ts,tsx}',
    '!../../frontend/src/index.tsx',
    '!../../frontend/src/reportWebVitals.ts'
  ],
  testMatch: [
    '<rootDir>/src/**/*.test.{ts,tsx}'
  ],
  preset: 'ts-jest'
};