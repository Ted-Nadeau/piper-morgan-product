# Claude Code Deployment - pipermorgan.ai Website Sprint

Please execute the pipermorgan.ai website foundation setup following our systematic methodology.

## VERIFY FIRST (mandatory):

```bash
# Check current repository state
pwd
ls -la
find . -name "site" -type d 2>/dev/null || echo "No site directory found"
git status
git branch
gh auth status
```

STOP CONDITIONS:
- If not in correct repository → STOP and confirm location
- If gh CLI not authenticated → STOP and authenticate first
- If uncommitted changes exist → STOP and check with lead dev

## OBJECTIVE: GitHub Issues Creation & Foundation Setup

### Phase 1: Create GitHub Issues (Priority)

Create 5 tracking issues for website sprint using the specifications below. Each issue should be created with:
- **Status**: "Sprint Backlog"
- **Labels**: "website", "sprint-01"
- **Milestone**: Create "Website MVP" milestone first

```bash
# Create milestone
gh api repos/:owner/:repo/milestones -f title="Website MVP" -f description="5-day sprint to launch pipermorgan.ai" -f due_on="2025-08-06T23:59:59Z"

# Create issues (use these exact specifications)
```

#### Issue 1: SITE-001 Technical Foundation
```bash
gh issue create \
  --title "SITE-001: Technical Foundation & Architecture Setup" \
  --label "website,sprint-01,P0-critical" \
  --milestone "Website MVP" \
  --body "**Priority**: P0 - Critical Path
**Estimate**: 8 points
**Agent Assignment**: Claude Code (High Context)

## Description
Establish the technical foundation for pipermorgan.ai website following Domain-Driven Design principles. Create the domain model for website content, set up Next.js with static site generation, and establish the deployment pipeline.

## Acceptance Criteria
- [ ] Domain model created for website content (pages, components, integrations)
- [ ] Next.js project initialized in \`site/\` directory with TypeScript
- [ ] Static site generation configured for performance
- [ ] Build pipeline established (dev, build, export commands)
- [ ] Deployment configuration for Vercel/Netlify
- [ ] Basic routing structure for 5 pages (Home, About, Newsletter, Blog, How It Works)
- [ ] Component architecture following atomic design principles
- [ ] Performance baseline established (Lighthouse CI integration)

## Domain Model Requirements
\`\`\`typescript
// Core domain entities
interface WebsiteContent {
  pages: Page[]
  components: Component[]
  integrations: Integration[]
}

interface Page {
  slug: string
  title: string
  description: string
  components: Component[]
  seoMetadata: SEOMetadata
}

interface Integration {
  type: 'convertkit' | 'medium' | 'analytics'
  configuration: IntegrationConfig
  status: 'active' | 'inactive'
}
\`\`\`

## Technical Specifications
- **Framework**: Next.js 14+ with App Router
- **Styling**: Tailwind CSS with custom design system
- **Performance**: Static site generation for all pages
- **SEO**: Built-in metadata API and sitemap generation
- **Testing**: Jest + Testing Library for component testing

## Success Criteria
- All builds pass without errors
- Basic page routing functional
- Performance: Lighthouse score >85 on initial setup
- Domain models clearly defined and documented
- Ready for parallel component development"
```

#### Issue 2: SITE-002 Design System
```bash
gh issue create \
  --title "SITE-002: Design System & Component Library" \
  --label "website,sprint-01,P0-critical" \
  --milestone "Website MVP" \
  --body "**Priority**: P0 - Critical Path
**Estimate**: 5 points
**Agent Assignment**: Cursor Agent (Limited Context)

## Description
Implement the design system foundation based on established brand guidelines. Create reusable UI components following the teal-orange palette and professional aesthetic established in strategic planning.

## MANDATORY VERIFICATION FIRST
\`\`\`bash
# Check existing patterns
find site/ -name \"*.css\" -o -name \"*.scss\" -o -name \"*.module.css\"
grep -r \"color\\|font\\|spacing\" site/ --include=\"*.ts\" --include=\"*.tsx\"
cat site/tailwind.config.js 2>/dev/null || echo \"No Tailwind config found\"
\`\`\`

## Acceptance Criteria
- [ ] Design tokens implemented (colors, typography, spacing)
- [ ] Component library structure established
- [ ] Core components built: Header, Footer, Her
