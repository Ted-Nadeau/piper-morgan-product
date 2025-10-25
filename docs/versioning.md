# Piper Morgan Versioning Strategy

## Current Version: 0.8.0-alpha

## Versioning Scheme

Piper Morgan follows [Semantic Versioning (SemVer)](https://semver.org/) with the following format:

```
MAJOR.MINOR.PATCH[-PRERELEASE]
```

### Version Components

- **MAJOR**: Incremented for incompatible API changes
- **MINOR**: Incremented for backwards-compatible functionality additions
- **PATCH**: Incremented for backwards-compatible bug fixes
- **PRERELEASE**: Optional suffix for pre-release versions (alpha, beta, rc)

### Current Versioning Strategy

#### Pre-1.0 (Alpha Phase)

- **0.x.y-alpha**: Alpha releases leading to MVP
- **0.x.y-beta**: Beta releases for final testing before MVP
- **1.0.0**: First MVP release

#### Post-1.0 (Production)

- **1.x.y**: Production releases following standard SemVer
- **2.0.0+**: Major version increments for breaking changes

## Version Sources of Truth

### Primary Version Definition

- **`VERSION` file**: Single source of truth in project root
- **`pyproject.toml`**: Python package version (must match VERSION file)

### Version References

- **Alpha documents**: Reference current semantic version
- **API responses**: Include version in metadata
- **Documentation**: Version-specific guides and references

## Roadmap vs. Version Separation

**Important**: Roadmap positions (e.g., "2.7.5", "Sprint A8") are **separate** from software versions.

- **Roadmap positions**: Track project progress and sprint completion
- **Software versions**: Track actual software releases and compatibility

This separation allows:

- Flexible roadmap adjustments without version confusion
- Clear software compatibility communication
- Independent roadmap and release planning

## Version Management

### Manual Process (Current)

1. Update `VERSION` file
2. Update `pyproject.toml` version field
3. Update relevant documentation
4. Create git tag for releases

### Future Automation (Planned)

- Automated version bumping scripts
- CI validation of version consistency
- Automatic changelog generation
- Integration with release workflows

## Alpha Testing Versions

During alpha testing, versions follow this pattern:

- `0.8.0-alpha`: Current alpha version
- `0.8.1-alpha`: Bug fixes and minor improvements
- `0.9.0-alpha`: New features and capabilities
- `1.0.0-beta`: Beta testing before MVP
- `1.0.0`: MVP release

## Version History

| Version     | Date     | Milestone | Notes                               |
| ----------- | -------- | --------- | ----------------------------------- |
| 0.8.0-alpha | Oct 2025 | Sprint A8 | Alpha tester onboarding preparation |
| 1.0.0       | TBD      | MVP       | Target MVP release                  |

## Guidelines for Contributors

1. **Never tie versions to roadmap positions**
2. **Update VERSION file first, then pyproject.toml**
3. **Use semantic versioning principles**
4. **Document breaking changes clearly**
5. **Test version references in documentation**

---

_Last updated: October 24, 2025_
_Current version: 0.8.0-alpha_
