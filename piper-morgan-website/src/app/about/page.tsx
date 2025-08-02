import type { Metadata } from 'next';
import { generateSEOMetadata } from '@/lib/domain-utils';
import { Hero, CTAButton, NewsletterSignup } from '@/components';

const seoData = generateSEOMetadata(
  'About Piper Morgan',
  'Learn about the project, methodology, and the team behind Piper Morgan',
  { canonical: 'https://pipermorgan.ai/about' }
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

export default function AboutPage() {
  return (
    <main>
      {/* Hero Section */}
      <Hero
        headline="About Piper Morgan"
        subheadline="Learn about the project, methodology, and the team behind the AI-powered Product Management Assistant that demonstrates systematic excellence through building-in-public."
        primaryCTA={{
          text: "See How It Works",
          href: "/how-it-works"
        }}
        secondaryCTA={{
          text: "Get Updates",
          href: "/newsletter"
        }}
        background="surface"
        align="center"
      />

      {/* Content Sections */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">

            {/* The Project */}
            <div className="mb-16">
              <h2 className="text-3xl font-bold text-text-dark mb-6">
                The Project
              </h2>
              <div className="prose prose-lg max-w-none">
                <p className="text-lg text-text-light mb-6">
                  Piper Morgan is an AI-powered Product Management Assistant that evolves from
                  automating routine PM tasks to providing strategic insights. Built with
                  domain-driven design principles, it represents a systematic approach to
                  product management excellence.
                </p>
                <p className="text-lg text-text-light mb-6">
                  The platform demonstrates how AI can enhance rather than replace human PM expertise,
                  providing transparency into decision-making processes and methodology development.
                </p>
              </div>
            </div>

            {/* The Methodology */}
            <div className="mb-16">
              <h2 className="text-3xl font-bold text-text-dark mb-6">
                The Methodology
              </h2>
              <div className="bg-surface p-8 rounded-card mb-8">
                <h3 className="text-xl font-semibold text-text-dark mb-4">
                  Building-in-Public Excellence
                </h3>
                <p className="text-text-light mb-6">
                  Our approach demonstrates systematic excellence through transparent processes,
                  multi-agent coordination, and test-driven development. Every decision is documented,
                  every pattern is captured, and every breakthrough is shared.
                </p>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-semibold text-text-dark mb-2">Four Pillars</h4>
                    <ul className="space-y-2 text-text-light">
                      <li>• Systematic Verification First</li>
                      <li>• Test-Driven Development</li>
                      <li>• Multi-Agent Coordination</li>
                      <li>• GitHub-First Tracking</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-text-dark mb-2">Proven Results</h4>
                    <ul className="space-y-2 text-text-light">
                      <li>• 15-minute ADR migrations</li>
                      <li>• 100% test coverage maintained</li>
                      <li>• Zero architectural drift</li>
                      <li>• Accelerated implementation</li>
                    </ul>
                  </div>
                </div>
              </div>

              <CTAButton
                href="/how-it-works"
                variant="outline"
                size="md"
              >
                Learn More About Our Methodology
              </CTAButton>
            </div>

            {/* Christian Rondeau */}
            <div className="mb-16">
              <h2 className="text-3xl font-bold text-text-dark mb-6">
                Christian Rondeau
              </h2>
              <div className="bg-gradient-to-r from-primary-teal/5 to-primary-orange/5 p-8 rounded-card">
                <p className="text-lg text-text-light mb-6">
                  Product management professional with expertise in civic tech, AI integration,
                  and systematic methodology development. Currently building Piper Morgan to
                  demonstrate how AI can enhance rather than replace human product management expertise.
                </p>

                <div className="grid md:grid-cols-2 gap-8">
                  <div>
                    <h4 className="font-semibold text-text-dark mb-3">Background</h4>
                    <ul className="space-y-2 text-text-light">
                      <li>• Senior PM with civic tech focus</li>
                      <li>• AI integration specialist</li>
                      <li>• Systematic methodology advocate</li>
                      <li>• Building-in-public practitioner</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-text-dark mb-3">Vision</h4>
                    <p className="text-text-light">
                      Creating AI-powered tools that augment human intelligence and demonstrate
                      their work transparently, enabling systematic excellence in product management.
                    </p>
                  </div>
                </div>

                <div className="mt-6 flex flex-wrap gap-4">
                  <CTAButton
                    href="https://twitter.com/mediajunkie"
                    variant="outline"
                    size="sm"
                    external
                  >
                    Follow on Twitter
                  </CTAButton>
                  <CTAButton
                    href="https://linkedin.com/in/christianrondeau"
                    variant="outline"
                    size="sm"
                    external
                  >
                    Connect on LinkedIn
                  </CTAButton>
                </div>
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
              title="Join the Journey"
              description="Follow our building-in-public approach and get insights into systematic PM methodology development."
              benefits={[
                "Behind-the-scenes methodology insights",
                "Weekly development updates",
                "Early access to new features",
                "Practical PM templates and frameworks"
              ]}
              background="dark"
              privacyNotice="No spam, unsubscribe anytime. Join the systematic excellence community."
            />
          </div>
        </div>
      </section>
    </main>
  );
}
