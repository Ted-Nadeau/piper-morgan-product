import type { Metadata } from 'next';
import { generateSEOMetadata } from '@/lib/domain-utils';
import { Hero, BlogPostCard, NewsletterSignup, CTAButton } from '@/components';

const seoData = generateSEOMetadata(
  'Building-in-Public: AI-Powered PM Methodology Development',
  'Follow our transparent journey developing systematic PM excellence through AI collaboration. Real insights, real breakthroughs, real learning.',
  { canonical: 'https://pipermorgan.ai/blog' }
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

export default function BlogPage() {
  return (
    <main>
      {/* Hero Section */}
      <Hero
        headline="Building-in-public:"
        highlightText="systematic PM excellence"
        subheadline="Follow our transparent journey as we develop AI-powered product management methodology through verified patterns, breakthrough discoveries, and systematic excellence. Every decision documented, every pattern captured, every lesson shared."
        primaryCTA={{
          text: "Read Latest Updates",
          href: "#recent-posts"
        }}
        secondaryCTA={{
          text: "Join the Journey",
          href: "/newsletter"
        }}
        background="surface"
        align="center"
      />

      {/* Recent Posts Section */}
      <section id="recent-posts" className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-text-dark mb-6">
                Building-in-Public Updates
              </h2>
              <p className="text-xl text-text-light">
                Deep dives into our methodology breakthroughs, systematic excellence patterns, and transparent AI-powered product management development. Learn from our systematic approach as we build it.
              </p>
            </div>

            {/* Featured Posts Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
              <BlogPostCard
                title="Systematic Verification: The 15-Minute ADR Migration"
                excerpt="How our verification-first methodology reduced implementation time from 2+ hours to 15 minutes, with zero architectural drift across 50+ implementations."
                publishedAt="Dec 15, 2024"
                readingTime="5 min read"
                tags={["Methodology", "ADR", "Verification"]}
                href="https://medium.com/building-piper-morgan/systematic-verification-15-minute-adr"
                external
              />

              <BlogPostCard
                title="Multi-Agent Coordination: Building Value Systematically"
                excerpt="Deep dive into our agent coordination patterns and how GitHub-first tracking enables systematic progress across complex implementations."
                publishedAt="Dec 10, 2024"
                readingTime="7 min read"
                tags={["Coordination", "GitHub", "Process"]}
                href="https://medium.com/building-piper-morgan/multi-agent-coordination"
                external
              />

              <BlogPostCard
                title="Excellence Flywheel: From Pattern to Production"
                excerpt="The systematic approach that turns each implementation into accelerated future work, creating a flywheel of continuous improvement."
                publishedAt="Dec 5, 2024"
                readingTime="6 min read"
                tags={["Excellence", "Patterns", "Optimization"]}
                href="https://medium.com/building-piper-morgan/excellence-flywheel"
                external
              />

              <BlogPostCard
                title="Domain-Driven PM: Why Architecture Matters"
                excerpt="Exploring how domain-driven design principles transform product management tools from simple automation to strategic intelligence."
                publishedAt="Nov 28, 2024"
                readingTime="8 min read"
                tags={["DDD", "Architecture", "Strategy"]}
                href="https://medium.com/building-piper-morgan/domain-driven-pm"
                external
              />

              <BlogPostCard
                title="Building in Public: Lessons from Month One"
                excerpt="Transparent reflection on our first month of building in public, including wins, challenges, and methodology refinements."
                publishedAt="Nov 20, 2024"
                readingTime="4 min read"
                tags={["Building in Public", "Reflection", "Learning"]}
                href="https://medium.com/building-piper-morgan/month-one-lessons"
                external
              />

              <BlogPostCard
                title="Test-Driven Excellence: Why TDD Accelerates AI Development"
                excerpt="How test-driven development becomes even more critical when building AI-powered systems, with concrete examples from our implementation."
                publishedAt="Nov 15, 2024"
                readingTime="6 min read"
                tags={["TDD", "Testing", "AI Development"]}
                href="https://medium.com/building-piper-morgan/test-driven-excellence"
                external
              />
            </div>

            {/* Medium Integration Notice */}
            <div className="bg-gradient-to-r from-primary-teal/5 to-primary-orange/5 p-8 rounded-card text-center mb-12">
              <h3 className="text-2xl font-semibold text-text-dark mb-4">
                Full Building-in-Public Collection on Medium
              </h3>
              <p className="text-text-light mb-6">
                All our transparent development updates, methodology breakthroughs, and systematic excellence discoveries are published on Medium for wider community engagement. Join 576+ readers following our journey from experiment to systematic practice.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <CTAButton
                  href="https://medium.com/building-piper-morgan"
                  variant="primary"
                  size="lg"
                  external
                >
                  Visit Our Medium Publication
                </CTAButton>
                <CTAButton
                  href="https://medium.com/@mediajunkie"
                  variant="outline"
                  size="lg"
                  external
                >
                  Follow Christian on Medium
                </CTAButton>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Newsletter CTA */}
      <section className="bg-text-dark py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto">
            <NewsletterSignup
              title="Get systematic excellence insights delivered weekly"
              description="Never miss a breakthrough discovery, methodology insight, or behind-the-scenes development update. Join 576+ PM professionals learning systematic excellence through our transparent building-in-public approach."
              benefits={[
                "Weekly methodology insights and breakthrough discoveries",
                "Behind-the-scenes development updates and decision rationale",
                "Early access to new systematic frameworks and tools",
                "Practical templates and patterns you can immediately apply",
                "Direct insight into human-AI collaboration patterns that actually work"
              ]}
              background="dark"
              privacyNotice="No spam, unsubscribe anytime. Join 576+ PM professionals learning systematic excellence."
            />
          </div>
        </div>
      </section>
    </main>
  );
}
