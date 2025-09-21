# Asset Management Guidelines

**Created**: September 20, 2025
**Purpose**: Standardized asset organization and size management

---

## Directory Structure

### Images
- `images/architecture/` - Architecture diagrams and system visualizations
- `images/screenshots/` - UI screenshots and development captures
- `images/blog/` - Blog-related images and graphics

### Diagrams
- `diagrams/source/` - Editable diagram sources (draw.io, Figma, etc.)
- `diagrams/generated/` - Generated outputs (PNG, SVG from source)

### Documents
- `documents/templates/` - Document templates and boilerplates
- `documents/exports/` - Generated documentation exports

### Communication Assets
- `comms/blog/` - Blog images and graphics
- `comms/growing-piper/` - Project growth documentation assets
- `comms/rosenslides/` - Presentation materials
- `comms/shipping-news/` - Release and update communications

---

## File Size Guidelines

### Size Limits
- **Maximum file size**: 500KB for git performance
- **Recommended compression**: Files >100KB should be compressed
- **Automatic exclusion**: Files >500KB added to .gitignore

### Optimization Requirements
- **Images**: Use appropriate compression for content type
- **Screenshots**: Crop to relevant areas, optimize resolution
- **Diagrams**: Export optimized formats (SVG preferred for scalability)

---

## Naming Conventions

### Format
`YYYY-MM-DD-descriptive-name.extension`

### Examples
- `2025-09-20-models-hub-architecture.png`
- `2025-09-20-session-log-screenshot.png`
- `2025-09-20-restructuring-workflow.svg`

### Special Prefixes
- `arch-` - Architecture diagrams
- `ui-` - User interface screenshots
- `flow-` - Process flow diagrams
- `blog-` - Blog-specific content

---

## Usage Guidelines

### Adding New Assets
1. Choose appropriate subdirectory based on purpose
2. Follow naming conventions with date and description
3. Verify file size <500KB before commit
4. Add descriptive commit message

### Managing Large Files
1. Compress images using appropriate tools
2. Consider alternative formats (SVG for diagrams)
3. Split large documents into smaller sections
4. Use external hosting for files >500KB if necessary

### Cross-References
- Link to assets using relative paths from docs root
- Include alt text for accessibility
- Document asset purposes in relevant documentation

---

## Maintenance

### Weekly Reviews
- Audit new assets for size compliance
- Verify naming convention adherence
- Remove unused or duplicate assets

### Monthly Cleanup
- Compress large assets where possible
- Update cross-references for moved assets
- Archive old assets no longer in use

---

*Asset management guidelines established: September 20, 2025*
