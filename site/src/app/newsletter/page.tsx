import type { Metadata } from 'next';
import { generateSEOMetadata } from '@/lib/domain-utils';
import { Hero, NewsletterSignup, CTAButton } from '@/components';

const seoData = generateSEOMetadata(
  'Newsletter Signup',
  'Stay updated on Piper Morgan development and PM methodology insights',
  { canonical: 'https://pipermorgan.ai/newsletter' }
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

export default function NewsletterPage() {
  return (
    <main>
      {/* Hero Section */}
      <Hero
        headline="Stay Updated"
        subheadline="Get insights on AI-powered product management methodology, building-in-public learnings, and systematic excellence patterns."
        primaryCTA={{
          text: "How It Works",
          href: "/how-it-works"
        }}
        secondaryCTA={{
          text: "Read the Blog",
          href: "/blog"
        }}
        background="gradient"
      />

      {/* Main Newsletter Signup */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto">
            <NewsletterSignup
              title="Join 500+ PM Professionals"
              description="Get weekly insights delivered to your inbox. No fluff, just actionable methodology and behind-the-scenes development updates."
              benefits={[
                "Weekly methodology insights and breakthroughs",
                "Behind-the-scenes development updates",
                "Early access to new features and tools",
                "Practical PM templates and frameworks",
                "Exclusive case studies and learnings",
                "Community access and networking"
              ]}
              background="surface"
              compact={false}
              privacyNotice="No spam, unsubscribe anytime. We respect your privacy and will never share your email."
            />
          </div>
        </div>
      </section>

      {/* Value Proposition */}
      <section className="bg-surface py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl font-bold text-text-dark mb-6">
              Why Subscribe?
            </h2>
            <p className="text-xl text-text-light mb-12">
              Get exclusive access to our building-in-public methodology and systematic excellence patterns.
            </p>

            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-white p-6 rounded-card shadow-component">
                <div className="w-12 h-12 bg-primary-teal rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="text-white font-bold text-xl">📊</span>
                </div>
                <h3 className="text-xl font-semibold text-text-dark mb-3">
                  Methodology Insights
                </h3>
                <p className="text-text-light">
                  Deep dives into our systematic approach to product management,
                  including patterns, frameworks, and decision-making processes.
                </p>
              </div>

              <div className="bg-white p-6 rounded-card shadow-component">
                <div className="w-12 h-12 bg-primary-orange rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="text-white font-bold text-xl">🔍</span>
                </div>
                <h3 className="text-xl font-semibold text-text-dark mb-3">
                  Behind the Scenes
                </h3>
                <p className="text-text-light">
                  Transparent look at our development process, including challenges,
                  breakthroughs, and lessons learned building AI-powered PM tools.
                </p>
              </div>

              <div className="bg-white p-6 rounded-card shadow-component">
                <div className="w-12 h-12 bg-primary-teal rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="text-white font-bold text-xl">🚀</span>
                </div>
                <h3 className="text-xl font-semibold text-text-dark mb-3">
                  Early Access
                </h3>
                <p className="text-text-light">
                  First access to new features, templates, and tools. Plus exclusive
                  community access and networking opportunities.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Sample Content Preview */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-text-dark text-center mb-12">
              Recent Newsletter Highlights
            </h2>

            <div className="space-y-8">
              <div className="bg-gradient-to-r from-primary-teal/5 to-primary-orange/5 p-8 rounded-card">
                <h3 className="text-xl font-semibold text-text-dark mb-3">
                  &ldquo;Systematic Verification: The 15-Minute ADR Migration&rdquo;
                </h3>
                <p className="text-text-light mb-4">
                  How our verification-first methodology reduced implementation time from
                  2+ hours to 15 minutes, with zero architectural drift across 50+ implementations.
                </p>
                <div className="text-sm text-text-light">
                  📅 Issue #47 • ⏱️ 5 min read • 🎯 Implementation Strategy
                </div>
              </div>

              <div className="bg-gradient-to-r from-primary-orange/5 to-primary-teal/5 p-8 rounded-card">
                <h3 className="text-xl font-semibold text-text-dark mb-3">
                  &ldquo;Multi-Agent Coordination: Building Value Systematically&rdquo;
                </h3>
                <p className="text-text-light mb-4">
                  Deep dive into our agent coordination patterns and how GitHub-first
                  tracking enables systematic progress across complex implementations.
                </p>
                <div className="text-sm text-text-light">
                  📅 Issue #46 • ⏱️ 7 min read • 🔧 Methodology
                </div>
              </div>

              <div className="bg-surface p-8 rounded-card">
                <h3 className="text-xl font-semibold text-text-dark mb-3">
                  &ldquo;Excellence Flywheel: From Pattern to Production&rdquo;
                </h3>
                <p className="text-text-light mb-4">
                  The systematic approach that turns each implementation into accelerated
                  future work, creating a flywheel of continuous improvement.
                </p>
                <div className="text-sm text-text-light">
                  📅 Issue #45 • ⏱️ 6 min read • 📈 Process Optimization
                </div>
              </div>
            </div>

            <div className="text-center mt-12">
              <CTAButton
                href="/blog"
                variant="outline"
                size="lg"
              >
                Read More on Our Blog
              </CTAButton>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
