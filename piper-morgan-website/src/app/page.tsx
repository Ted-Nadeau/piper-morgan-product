import type { Metadata } from 'next';
import { generateSEOMetadata } from '@/lib/domain-utils';
import { Hero, NewsletterSignup, BlogPostCard, CTAButton } from '@/components';

const seoData = generateSEOMetadata(
  'Piper Morgan - AI Product Management Assistant',
  'Building-in-public: AI-powered PM methodology that shows its work',
  { canonical: 'https://pipermorgan.ai' }
);

export const metadata: Metadata = {
  title: seoData.title,
  description: seoData.description,
  keywords: seoData.keywords,
  openGraph: seoData.openGraph,
  twitter: seoData.twitter,
  alternates: {
    canonical: seoData.canonical
  }
};

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <Hero
        headline="AI Product Management"
        highlightText="That Shows Its Work"
        subheadline="Piper Morgan demonstrates systematic excellence through building-in-public. Watch AI-powered PM methodology evolve from routine automation to strategic insights."
        primaryCTA={{
          text: "How It Works",
          href: "/how-it-works"
        }}
        secondaryCTA={{
          text: "Get Updates",
          href: "/newsletter"
        }}
      />

      {/* Value Propositions */}
      <section className="bg-surface py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-3xl font-bold text-text-dark text-center mb-12">
              Systematic Excellence in Action
            </h2>

            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-white p-8 rounded-lg shadow-sm">
                <div className="w-12 h-12 bg-primary-teal rounded-lg flex items-center justify-center mb-4">
                  <span className="text-white font-bold text-xl">✓</span>
                </div>
                <h3 className="text-xl font-semibold text-text-dark mb-3">
                  Verification First
                </h3>
                <p className="text-text-light">
                  Every implementation starts with pattern discovery. 15-minute ADR migrations
                  prove that verification accelerates rather than slows development.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-sm">
                <div className="w-12 h-12 bg-primary-orange rounded-lg flex items-center justify-center mb-4">
                  <span className="text-white font-bold text-xl">⚡</span>
                </div>
                <h3 className="text-xl font-semibold text-text-dark mb-3">
                  Multi-Agent Coordination
                </h3>
                <p className="text-text-light">
                  Strategic deployment of specialized AI agents with clear handoff protocols.
                  Building value systematically rather than working in isolation.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-sm">
                <div className="w-12 h-12 bg-primary-teal rounded-lg flex items-center justify-center mb-4">
                  <span className="text-white font-bold text-xl">📊</span>
                </div>
                <h3 className="text-xl font-semibold text-text-dark mb-3">
                  GitHub-First Tracking
                </h3>
                <p className="text-text-light">
                  All work tracked with clear issue definitions and acceptance criteria.
                  Zero architectural drift across 50+ implementations.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Building in Public */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-text-dark mb-6">
                Follow the Journey
              </h2>
              <p className="text-xl text-text-light mb-8">
                Every breakthrough documented. Every pattern captured. Every decision explained.
              </p>
            </div>

            {/* Recent Blog Posts */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
              <BlogPostCard
                title="Systematic Verification: The 15-Minute ADR Migration"
                excerpt="How our verification-first methodology reduced implementation time from 2+ hours to 15 minutes, with zero architectural drift across 50+ implementations."
                publishedAt="Dec 15, 2024"
                readingTime="5 min read"
                tags={["Methodology", "ADR", "Verification"]}
                href="https://medium.com/building-piper-morgan/systematic-verification-15-minute-adr"
                external
                compact
              />

              <BlogPostCard
                title="Multi-Agent Coordination: Building Value Systematically"
                excerpt="Deep dive into our agent coordination patterns and how GitHub-first tracking enables systematic progress across complex implementations."
                publishedAt="Dec 10, 2024"
                readingTime="7 min read"
                tags={["Coordination", "GitHub", "Process"]}
                href="https://medium.com/building-piper-morgan/multi-agent-coordination"
                external
                compact
              />

              <BlogPostCard
                title="Excellence Flywheel: From Pattern to Production"
                excerpt="The systematic approach that turns each implementation into accelerated future work, creating a flywheel of continuous improvement."
                publishedAt="Dec 5, 2024"
                readingTime="6 min read"
                tags={["Excellence", "Patterns", "Optimization"]}
                href="https://medium.com/building-piper-morgan/excellence-flywheel"
                external
                compact
              />
            </div>

            <div className="text-center">
              <CTAButton
                href="/blog"
                variant="primary"
                size="lg"
              >
                Read All Building-in-Public Updates
              </CTAButton>
            </div>
          </div>
        </div>
      </section>

      {/* Newsletter CTA */}
      <section className="bg-text-dark py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto">
            <NewsletterSignup
              title="Stay on the Cutting Edge"
              description="Get weekly insights on AI-powered PM methodology, systematic excellence patterns, and behind-the-scenes development updates."
              benefits={[
                "Weekly methodology insights and breakthroughs",
                "Behind-the-scenes development updates",
                "Early access to new features and tools",
                "Practical PM templates and frameworks"
              ]}
              background="dark"
              compact={false}
              privacyNotice="No spam, unsubscribe anytime. Join 500+ PM professionals."
            />
          </div>
        </div>
      </section>
    </main>
  );
}
