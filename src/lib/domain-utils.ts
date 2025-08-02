/**
 * Utility functions for working with domain models
 */

import type {
  Page,
  SEOMetadata,
  Component,
  BlogPost,
  PerformanceMetrics,
  WebsiteContent
} from '@/types/domain';

/**
 * Generate SEO metadata for a page
 */
export function generateSEOMetadata(
  title: string,
  description: string,
  options: Partial<SEOMetadata> = {}
): SEOMetadata {
  const baseTitle = 'Piper Morgan - AI Product Management Assistant';
  const fullTitle = title === baseTitle ? title : `${title} | ${baseTitle}`;

  return {
    title: fullTitle,
    description,
    keywords: [
      'AI',
      'Product Management',
      'Methodology',
      'Building in Public',
      'PM Tools',
      'Systematic Excellence',
      ...(options.keywords || [])
    ],
    openGraph: {
      title: fullTitle,
      description,
      url: options.canonical,
      image: '/images/og-image.png',
      ...options.openGraph
    },
    twitter: {
      card: 'summary_large_image',
      title: fullTitle,
      description,
      image: '/images/twitter-card.png',
      ...options.twitter
    },
    canonical: options.canonical
  };
}

/**
 * Create a page with sensible defaults
 */
export function createPage(
  slug: string,
  title: string,
  description: string,
  components: Component[] = []
): Page {
  return {
    slug,
    title,
    description,
    components,
    seoMetadata: generateSEOMetadata(title, description, {
      canonical: `https://pipermorgan.ai/${slug === 'home' ? '' : slug}`
    }),
    status: 'draft',
    updatedAt: new Date()
  };
}

/**
 * Create a component with type safety
 */
export function createComponent(
  type: string,
  props: Record<string, unknown> = {},
  children: Component[] = []
): Component {
  return {
    id: `${type}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    type,
    props,
    children: children.length > 0 ? children : undefined
  };
}

/**
 * Extract reading time from blog post content
 */
export function calculateReadingTime(content: string): number {
  const wordsPerMinute = 200;
  const wordCount = content.trim().split(/\s+/).length;
  return Math.ceil(wordCount / wordsPerMinute);
}

/**
 * Parse Medium RSS feed item to BlogPost
 */
export function parseMediumPost(feedItem: Record<string, unknown>): BlogPost {
  const content = feedItem.content || feedItem.description || '';

  return {
    id: String(feedItem.guid || feedItem.link || ''),
    title: String(feedItem.title || ''),
    excerpt: extractExcerpt(String(content)),
    content: String(content),
    publishedAt: new Date(String(feedItem.pubDate || feedItem.isoDate || Date.now())),
    author: String(feedItem.creator || 'Christian Rondeau'),
    readingTime: calculateReadingTime(String(content)),
    tags: Array.isArray(feedItem.categories) ? feedItem.categories.map(String) : [],
    url: `/blog/${slugify(String(feedItem.title || ''))}`,
    mediumUrl: String(feedItem.link || '')
  };
}

/**
 * Extract excerpt from HTML content
 */
function extractExcerpt(htmlContent: string, maxLength: number = 160): string {
  // Strip HTML tags and get plain text
  const textContent = htmlContent.replace(/<[^>]*>/g, '');

  if (textContent.length <= maxLength) {
    return textContent;
  }

  // Find the last complete sentence within the limit
  const truncated = textContent.substr(0, maxLength);
  const lastSentence = truncated.lastIndexOf('.');

  if (lastSentence > maxLength * 0.7) {
    return truncated.substr(0, lastSentence + 1);
  }

  // Fallback to word boundary
  const lastSpace = truncated.lastIndexOf(' ');
  return truncated.substr(0, lastSpace) + '...';
}

/**
 * Create URL-friendly slug from title
 */
export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '') // Remove special characters
    .replace(/[\s_-]+/g, '-') // Replace spaces and underscores with hyphens
    .replace(/^-+|-+$/g, ''); // Remove leading/trailing hyphens
}

/**
 * Validate performance metrics against targets
 */
export function validatePerformanceMetrics(metrics: PerformanceMetrics): {
  isValid: boolean;
  failures: string[];
} {
  const failures: string[] = [];

  // Lighthouse targets (from development brief)
  if (metrics.lighthouse.performance < 90) {
    failures.push(`Performance score ${metrics.lighthouse.performance} below target 90`);
  }
  if (metrics.lighthouse.accessibility < 95) {
    failures.push(`Accessibility score ${metrics.lighthouse.accessibility} below target 95`);
  }
  if (metrics.lighthouse.seo < 95) {
    failures.push(`SEO score ${metrics.lighthouse.seo} below target 95`);
  }

  // Core Web Vitals targets
  if (metrics.coreWebVitals.fcp > 1.5) {
    failures.push(`FCP ${metrics.coreWebVitals.fcp}s above target 1.5s`);
  }
  if (metrics.coreWebVitals.lcp > 2.5) {
    failures.push(`LCP ${metrics.coreWebVitals.lcp}s above target 2.5s`);
  }
  if (metrics.coreWebVitals.cls > 0.1) {
    failures.push(`CLS ${metrics.coreWebVitals.cls} above target 0.1`);
  }

  return {
    isValid: failures.length === 0,
    failures
  };
}

/**
 * Get default website content structure
 */
export function getDefaultWebsiteContent(): WebsiteContent {
  return {
    pages: [
      createPage('home', 'Piper Morgan - AI Product Management Assistant', 'Building-in-public: AI-powered PM methodology that shows its work'),
      createPage('about', 'About Piper Morgan', 'Learn about the project, methodology, and the team behind Piper Morgan'),
      createPage('newsletter', 'Newsletter Signup', 'Stay updated on Piper Morgan development and PM methodology insights'),
      createPage('blog', 'Blog - Building Piper Morgan', 'Follow our building-in-public journey and PM methodology development'),
      createPage('how-it-works', 'How Piper Morgan Works', 'Understanding the AI-powered PM methodology and systematic approach')
    ],
    components: [],
    integrations: [
      {
        type: 'convertkit',
        configuration: {
          formId: process.env.NEXT_PUBLIC_CONVERTKIT_FORM_ID || '',
          successUrl: '/newsletter/success',
          errorMessage: 'There was an error signing up. Please try again.'
        },
        status: 'active'
      },
      {
        type: 'medium',
        configuration: {
          feedUrl: 'https://medium.com/feed/building-piper-morgan',
          cacheDuration: 60, // 1 hour
          maxPosts: 10
        },
        status: 'active'
      },
      {
        type: 'analytics',
        configuration: {
          measurementId: process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID || '',
          trackingEvents: ['page_view', 'newsletter_signup', 'blog_click', 'external_link']
        },
        status: 'active'
      }
    ],
    siteMetadata: {
      title: 'Piper Morgan - AI Product Management Assistant',
      description: 'Building-in-public: AI-powered PM methodology that shows its work',
      url: 'https://pipermorgan.ai',
      author: 'Christian Rondeau',
      social: {
        twitter: '@mediajunkie',
        linkedin: 'christianrondeau',
        github: 'mediajunkie'
      }
    }
  };
}
