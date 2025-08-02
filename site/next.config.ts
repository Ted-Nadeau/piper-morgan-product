import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable static exports for deployment to static hosting
  output: 'export',

  // No basePath - deploy website to root of GitHub Pages
  // (docs will be at /docs subdirectory)

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
