# Development Brief: Piper Morgan Website MVP

**Project**: pipermorgan.ai website
**Repository**: `site/` directory in main Piper Morgan project
**Timeline**: MVP launch within 5 days
**Architecture**: Claude (Strategic UX) → Christian (PM) → Lead Dev → Claude Code → Cursor Agent

---

## 🎯 **MVP Requirements (Days 1-5)**

### **Core Functionality**
- **Homepage**: Professional landing page with value proposition
- **Newsletter Signup**: ConvertKit integration with form embed
- **About Page**: Project overview + Christian's background
- **Blog Feed**: Read-only Medium publication integration
- **Mobile Responsive**: Full functionality across all devices

### **Technical Specifications**

#### **Framework Decision**
**Recommended**: Next.js with static site generation
- **Rationale**: Fast performance, excellent SEO, easy blog integration
- **Alternative**: Eleventy if preferring minimal complexity
- **Deploy Target**: Vercel/Netlify free tier (aligns with $0 stack)

#### **Content Management Strategy**
```
/pages/
  ├── index.js           # Homepage
  ├── about.js           # About/Project info
  ├── newsletter.js      # Newsletter signup (redirect from forms)
  └── blog/
      └── index.js       # Medium feed integration
```

#### **Integration Requirements**
- **Medium RSS**: Fetch and display recent posts from Building Piper Morgan publication
- **ConvertKit**: Embed signup form, handle success/error states
- **Analytics**: Google Analytics 4 setup (free tier)
- **Domain**: pipermorgan.ai (Christian will handle DNS)

---

## 🎨 **Design System Foundation**

### **Color Palette** (MVP Implementation)
```css
:root {
  --primary-teal: #2DD4BF;
  --primary-orange: #FB923C;
  --text-dark: #1F2937;
  --text-light: #6B7280;
  --background: #FFFFFF;
  --surface: #F9FAFB;
}
```

### **Typography Hierarchy**
- **Headlines**: System font stack (Inter/SF Pro/Arial fallback)
- **Body**: 16px base, 1.6 line height for readability
- **Responsive**: Fluid typography scaling

### **Component Architecture**
- **Header**: Logo + navigation (simple, 3-4 items max)
- **Hero Section**: Value proposition + CTA
- **Newsletter CTA**: Prominent placement, multiple instances
- **Footer**: Minimal links, social, copyright

---

## 📱 **Mobile-First Requirements**

### **Performance Targets**
- **Lighthouse Score**: 90+ across all metrics
- **First Contentful Paint**: <1.5s
- **Largest Contentful Paint**: <2.5s
- **Cumulative Layout Shift**: <0.1

### **Responsive Breakpoints**
```css
/* Mobile First */
@media (min-width: 640px) { /* Small */ }
@media (min-width: 768px) { /* Medium */ }
@media (min-width: 1024px) { /* Large */ }
```

---

## 🔗 **Integration Specifications**

### **ConvertKit Signup Form**
```html
<!-- Embed code provided by Christian after service setup -->
<div id="convertkit-form-container">
  <!-- ConvertKit form embed -->
</div>
```

### **Medium RSS Integration**
```javascript
// Fetch latest 5 posts from Medium publication
const MEDIUM_RSS = 'https://medium.com/feed/building-piper-morgan';
// Parse and display: title, excerpt, publish date, read link
```

### **SEO Foundation**
```html
<head>
  <title>Piper Morgan - AI Product Management Assistant</title>
  <meta name="description" content="Building-in-public: AI-powered PM methodology that shows its work" />
  <!-- Additional meta tags for social sharing -->
</head>
```

---

## 🚀 **Deployment Strategy**

### **MVP Hosting** (Free Tier)
- **Vercel**: Recommended for Next.js, automatic deployments
- **Netlify**: Alternative option, excellent for static sites
- **GitHub Pages**: Fallback option if needed

### **Domain Configuration**
- **Christian handles**: DNS setup, domain pointing
- **Dev team provides**: Deployment URL for DNS configuration
- **SSL**: Automatic through hosting provider

---

## 📋 **Success Criteria**

### **Functional Requirements**
- ✅ Professional appearance signaling competence
- ✅ Newsletter signup conversion path clear and functional
- ✅ Mobile experience equivalent to desktop
- ✅ Blog content accessible and formatted properly
- ✅ Fast loading across all connection speeds

### **Technical Requirements**
- ✅ Lighthouse scores 90+ (performance, accessibility, best practices)
- ✅ Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- ✅ Form submissions properly handled (success/error states)
- ✅ Analytics tracking operational
- ✅ Domain properly configured and SSL active

---

## 🔄 **Handoff Process**

### **Asset Dependencies**
- **Logo**: Christian provides refined logo assets (Day 2-3)
- **Copy**: Christian provides all website copy (Day 3-4)
- **ConvertKit**: Christian provides embed codes (Day 2-3)

### **Review Checkpoints**
- **Day 2**: Technical foundation review
- **Day 3**: Design implementation review
- **Day 4**: Content integration review
- **Day 5**: Final MVP approval and launch

### **Agent Coordination**
- **Claude Code**: Strategic implementation, complex features
- **Cursor Agent**: Styling polish, cross-browser testing, final fixes
- **Handoffs**: Clear specifications between agents, minimal overlap

---

## 💡 **Strategic Context**

This MVP serves as professional placeholder supporting Christian's building-in-public methodology documentation. The site should feel like a credible "soft launch" that practitioners can engage with while full content is developed.

**Audience**: Senior PMs, UX leaders, civic tech practitioners, AI-curious professionals
**Brand**: Systematic excellence, transparent process, intelligent collaboration
**Voice**: Professional warmth, approachable expertise, building-in-public authenticity

---

**Ready for development kickoff!** This brief provides comprehensive direction while preserving flexibility for implementation details and agent coordination.
