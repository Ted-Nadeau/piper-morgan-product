import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable static exports for deployment to static hosting
  output: 'export',

  // GitHub Pages deployment configuration
  basePath: process.env.NODE_ENV === 'production' ? '/piper-morgan' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/piper-morgan' : '',

  // Disable image optimization for static export
  images: {
    unoptimized: true,
  },

  // Configure trailing slashes for better URL consistency
  trailingSlash: true,

  // Skip build-time linting (handled separately)
  eslint: {
    ignoreDuringBuilds: false,
  },

  // Skip build-time type checking (handled separately)
  typescript: {
    ignoreBuildErrors: false,
  },

  // Experimental features (disabled for static export compatibility)
  // experimental: {
  //   optimizeCss: true,
  // },
};

export default nextConfig;
