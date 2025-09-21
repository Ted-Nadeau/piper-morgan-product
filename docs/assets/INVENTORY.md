# Asset Inventory

**Created**: September 20, 2025
**Purpose**: Track asset organization and size compliance

---

## Asset Organization Summary

### Images (`images/`)
- **Architecture diagrams**: 0 files
- **Screenshots**: 0 files
- **Blog images**: 186+ files (includes large robot series and presentation slides)
- **Logos and favicons**: 15+ files (organized from scattered locations)

### Diagrams (`diagrams/`)
- **Source files**: Available for editable formats
- **Generated outputs**: PNG/SVG exports from source

### Documents (`documents/`)
- **Templates**: Document boilerplates and frameworks
- **Exports**: Generated documentation and reports
- **PDFs**: Editorial calendars and planning documents

---

## Size Compliance Status

### Files >500KB (86 files identified)
**Blog Images - Robot Series**: 70+ files
- Location: `images/blog/comms/blog/robot-*.png`
- Status: ⚠️ **Size compliance issue** - Consider compression
- Note: Historical blog content, may need optimization for git performance

**Presentation Slides - "The Pygmalion Effect" Rosenverse Talk**: 16+ files
- Location: `images/blog/comms/rosenslides/*.png`
- Status: ⚠️ **Size compliance issue** - Communications materials, managed separately
- Note: High-resolution presentation materials from Rosenverse talk, not core project docs

### Compliant Files (<500KB)
**Logos and Favicons**: 15+ files
- Location: `images/`
- Status: ✅ **Compliant** - Optimized for web use

---

## Asset Management Actions

### Completed
- ✅ **Organized scattered assets** from multiple docs locations
- ✅ **Created directory structure** by asset type and purpose
- ✅ **Established naming conventions** with date prefixes
- ✅ **Implemented .gitignore** for large file management

### Recommended
- 🔄 **Compress large blog images** to <500KB where possible
- 🔄 **Consider external hosting** for presentation slides
- 🔄 **Implement automated compression** in asset workflow
- 🔄 **Regular size audits** for new assets

---

## Usage Guidelines

### Adding New Assets
1. **Place in appropriate subdirectory** based on purpose
2. **Follow naming convention**: `YYYY-MM-DD-descriptive-name.ext`
3. **Verify size <500KB** before committing
4. **Update this inventory** for major additions

### Managing Large Files
1. **Compress using appropriate tools** (PNG optimization, JPEG quality)
2. **Consider SVG for diagrams** (scalable and smaller)
3. **Use external hosting** for files that must remain large
4. **Document exceptions** in this inventory

---

## Cross-References

### Related Documentation
- **Asset Management Guidelines**: [README.md](README.md)
- **Git Management**: [.gitignore](.gitignore)
- **Blog Content**: Historical robot series and presentation materials

### Integration Points
- Blog publishing pipeline
- Documentation generation
- Presentation material management
- Archaeological research asset preservation

---

*Asset inventory established: September 20, 2025*
