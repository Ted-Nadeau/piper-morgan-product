# Piper Morgan Website

This repository contains the public-facing website for Piper Morgan AI Product Management Assistant.

## 🌐 Live Site

- **Production**: https://pipermorgan.ai (will point to GitHub Pages)
- **GitHub Pages**: https://mediajunkie.github.io/piper-morgan-website/

## 🏗️ Architecture

- **Framework**: Next.js 15 with App Router
- **Styling**: Tailwind CSS with custom design system
- **Deployment**: Static Site Generation to GitHub Pages
- **Domain Models**: TypeScript with Domain-Driven Design

## 🚀 Development

```bash
npm install
npm run dev    # Start development server
npm run build  # Build for production
```

## 📁 Structure

```
├── src/
│   ├── app/           # Next.js app router pages
│   ├── components/    # React components (atomic design)
│   ├── lib/          # Utility functions
│   └── types/        # TypeScript type definitions
├── public/           # Static assets
└── out/             # Build output (generated)
```

## 🎨 Design System

- **Colors**: Teal primary (#2DD4BF), Orange accent (#FB923C)
- **Typography**: System fonts with semantic scale
- **Components**: Atomic design pattern (atoms → molecules → organisms)
- **Accessibility**: WCAG 2.1 AA compliant

## 📄 Pages

1. **Home** (`/`) - Landing page with value propositions
2. **About** (`/about`) - Project and team information
3. **How It Works** (`/how-it-works`) - Methodology deep dive
4. **Blog** (`/blog`) - Building-in-public content
5. **Newsletter** (`/newsletter`) - Subscription and updates

## 🤖 Generated with Claude Code

This website was built using systematic methodology and AI-powered development practices.

Co-Authored-By: Claude <noreply@anthropic.com> and @mediajunkie
