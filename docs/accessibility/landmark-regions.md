# G59: Landmark Regions Implementation
**WCAG 2.2 AA Compliance**: Provide semantic landmark regions for screen reader navigation

## Overview
Landmark regions help screen reader users quickly navigate to different sections of a page. They use semantic HTML elements and ARIA roles to create a page structure.

## Landmark Types

### 1. Banner (Header)
- **HTML**: `<header>`
- **ARIA Role**: `role="banner"` (implicit)
- **Purpose**: Contains site logo, main title, tagline
- **Usage**: Should appear once per page, at the top
- **Note**: Only use `<header>` at document level (not within `<main>`, `<section>`, etc.)

```html
<header role="banner">
  <img src="/logo.png" alt="Piper Morgan Logo" />
  <h1>Piper Morgan - AI PM Assistant</h1>
</header>
```

### 2. Navigation
- **HTML**: `<nav>`
- **ARIA Role**: `role="navigation"` (implicit)
- **Purpose**: Links to major sections (main navigation only)
- **Usage**: Can have multiple but primary nav should be labeled
- **Note**: Don't use for every link group - only major navigation

```html
<nav role="navigation" aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/standup">Standup</a></li>
    <li><a href="/settings">Settings</a></li>
  </ul>
</nav>
```

### 3. Main Content
- **HTML**: `<main>`
- **ARIA Role**: `role="main"` (implicit)
- **Purpose**: Primary content of the page
- **Usage**: One per page, should contain page-specific content
- **Note**: Skip links should link to `id="main-content"` on `<main>`

```html
<main id="main-content" role="main">
  <h1>Page Title</h1>
  <!-- Page content here -->
</main>
```

### 4. Sections
- **HTML**: `<section>`
- **ARIA Role**: `role="region"` (when needs to be landmark)
- **Purpose**: Thematic grouping of content within main
- **Usage**: Useful for major content sections
- **Note**: Use `aria-labelledby` to label the section

```html
<section aria-labelledby="preferences-heading" role="region">
  <h2 id="preferences-heading">Personality Preferences</h2>
  <!-- Section content -->
</section>
```

### 5. Complementary (Sidebar)
- **HTML**: `<aside>`
- **ARIA Role**: `role="complementary"` (implicit)
- **Purpose**: Content tangentially related to main (sidebars, related links)
- **Usage**: Optional, not all pages have sidebars

```html
<aside role="complementary" aria-label="Related information">
  <!-- Sidebar content -->
</aside>
```

### 6. Content Info (Footer)
- **HTML**: `<footer>`
- **ARIA Role**: `role="contentinfo"` (implicit when document-level)
- **Purpose**: Footer information (copyright, links, contact)
- **Usage**: One per page, at the bottom
- **Note**: Only use at document level (not within `<main>`, `<article>`, etc.)

```html
<footer role="contentinfo">
  <p>&copy; 2024 Piper Morgan. All rights reserved.</p>
</footer>
```

## Page Structure Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Head content -->
</head>
<body>
  <!-- 1. Skip Link (first in DOM, first in tab order) -->
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <!-- 2. Banner/Header -->
  <header role="banner">
    <h1>Site Title</h1>
  </header>

  <!-- 3. Primary Navigation -->
  <nav role="navigation" aria-label="Main navigation">
    <!-- Navigation content -->
  </nav>

  <!-- 4. Main Content (with ID for skip link target) -->
  <main id="main-content" role="main">
    <!-- Page title and content -->
  </main>

  <!-- 5. Optional: Complementary Content -->
  <aside role="complementary" aria-label="Sidebar">
    <!-- Sidebar content -->
  </aside>

  <!-- 6. Footer -->
  <footer role="contentinfo">
    <!-- Footer content -->
  </footer>
</body>
</html>
```

## Landmark Testing

### Screen Reader Testing
1. **NVDA (Windows)**: Press `R` to jump to landmarks
2. **JAWS (Windows)**: Press `;` to bring up landmarks list
3. **VoiceOver (Mac)**: Use rotor (VO+U) to access landmarks

### Manual Testing
1. Open DevTools > Accessibility panel
2. Look for "Landmarks" section
3. Verify all expected landmarks are listed
4. Click each landmark to highlight on page

### axe DevTools Check
- Run axe scan and look for landmark issues
- Common violations:
  - Missing `<main>` element
  - Multiple `<header>` or `<footer>` elements at document level
  - `<nav>` without distinguishing label (if multiple navs)
  - Landmark misuse (e.g., `<header>` inside `<main>`)

## Best Practices

### ✅ DO:
- Use semantic HTML elements (`<header>`, `<nav>`, `<main>`, `<footer>`, `<section>`, `<aside>`)
- Use one `<header>` and `<footer>` per document
- Label regions with `aria-label` or `aria-labelledby` if unclear
- Use `id="main-content"` on `<main>` for skip links
- Test with actual screen readers

### ❌ DON'T:
- Use `role="region"` on elements that don't need it
- Create multiple `<header>` or `<footer>` at document level
- Use `<nav>` for every link group
- Forget `aria-label` for unlabeled landmarks
- Use landmarks without proper content inside

## Implementation Checklist

**For each page template**:
- [ ] `<header role="banner">` at top with site branding
- [ ] `<nav role="navigation" aria-label="Main navigation">` for main nav
- [ ] `<main id="main-content" role="main">` with page content
- [ ] `<section role="region" aria-labelledby="...">` for major sections (optional)
- [ ] `<footer role="contentinfo">` at bottom (if applicable)
- [ ] Skip link at top: `<a href="#main-content" class="skip-link">`

## WCAG 2.2 Success Criteria

### 1.3.1 Info and Relationships (Level A)
- ✅ Landmark regions indicate document structure
- ✅ Helps screen reader users understand page organization

### 1.3.6 Identify Purpose (Level AAA)
- ✅ Landmark labels make region purpose clear
- ✅ Users understand role of each section

### 2.4.1 Bypass Blocks (Level A)
- ✅ Skip links (part of skip-link component)
- ✅ Landmark regions (this feature)
- ✅ Allow users to skip repetitive content

## Related Standards
- [W3C Using ARIA Landmarks](https://www.w3.org/WAI/ARIA/apg/practices/landmarks/)
- [WUHCAG Landmark Regions](https://www.wuhcag.com/landmark-regions/)
- [WebAIM Landmark Regions](https://webaim.org/articles/semanticstructure/)
