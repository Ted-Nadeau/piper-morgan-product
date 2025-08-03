import type { Metadata } from 'next';
import { generateSEOMetadata } from '@/lib/domain-utils';
import { Hero, BlogPostCard, NewsletterSignup, CTAButton } from '@/components';

const seoData = generateSEOMetadata(
  'Blog - Building Piper Morgan',
  'Follow our building-in-public journey and PM methodology development',
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
        headline="Building Piper Morgan"
        subheadline="Follow our building-in-public journey as we develop AI-powered PM methodology through systematic excellence and transparent processes."
        primaryCTA={{
          text: "Latest Updates",
          href: "#recent-posts"
        }}
        secondaryCTA={{
          text: "Subscribe",
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
                Recent Posts
              </h2>
              <p className="text-xl text-text-light">
                Deep dives into our methodology, breakthroughs, and systematic approach to AI-powered product management.
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
                Read More on Medium
              </h3>
              <p className="text-text-light mb-6">
                All our building-in-public content is published on Medium for wider reach and engagement.
                Future versions will include RSS integration to display posts directly here.
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
              title="Never Miss an Update"
              description="Get weekly insights on our building-in-public journey, methodology breakthroughs, and behind-the-scenes development updates delivered directly to your inbox."
              benefits={[
                "Weekly methodology insights and breakthroughs",
                "Behind-the-scenes development updates",
                "Early access to new features and tools",
                "Practical PM templates and frameworks"
              ]}
              background="dark"
              privacyNotice="No spam, unsubscribe anytime. Join 500+ PM professionals following our journey."
            />
          </div>
        </div>
      </section>
    </main>
  );
}
