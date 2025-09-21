# Markdown Rendering Test for Model Documentation

## Testing Navigation Anchors

### Quick Navigation
- [Pure Domain Models](#pure-domain-models)
- [Integration Models](#integration--transfer-models)
- [With Special Characters](#integration--transfer-models)

## Pure Domain Models

### Product
Test content for product model

## Integration & Transfer Models
Test content with special characters in heading

## Testing Code Block Sizes

### Compact Format
```python
@dataclass
class Product:
    id: str
    name: str
```

### Verbose Format with All Fields (38 models × ~15 fields each = ~570 lines)
```python
@dataclass
class Product:
    """A product being managed

    Business Purpose: Core domain entity representing products
    DDD Purity: ⚠️ Pure Domain - No infrastructure concerns
    Business Tags: #pm #core
    """
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    vision: str = ""
    strategy: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Relationships
    features: List["Feature"] = field(default_factory=list)
    stakeholders: List["Stakeholder"] = field(default_factory=list)
    metrics: List["Metric"] = field(default_factory=list)
    work_items: List["WorkItem"] = field(default_factory=list)
```

## Testing Cross-References

### Internal Links
- See [Product model](#product) above
- Related: [Domain Services](domain-services.md)
- External: [ADR-028](adr/adr-028-verification-pyramid.md)

### Table Format for Model Overview
| Model | Layer | Business Tags | Lines |
|-------|-------|--------------|-------|
| Product | Pure Domain | #pm | 15 |
| Feature | Pure Domain | #pm | 18 |
| Document | Supporting | #knowledge | 25 |

## Testing Warning Boxes

⚠️ **DDD Purity Warning**: Models in this section should have no infrastructure dependencies

> **Note**: This is a blockquote style callout

---

## File Size Estimation

With 38 models averaging 15-20 lines each:
- Model definitions: ~700 lines
- Documentation text: ~300 lines
- Navigation/TOC: ~100 lines
- **Total estimate**: ~1100 lines (acceptable for single file)

## Navigation Patterns That Work
1. Anchor links work with kebab-case (#pure-domain-models)
2. Special characters converted (& becomes -)
3. Relative path links (../development/file.md)
4. Section anchors (#heading-name)
