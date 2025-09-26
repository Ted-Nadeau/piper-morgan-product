# Integrated Pattern & RAG Analysis Instructions
## September 15, 2025

### Phase 1: Pattern Sweep Data Generation (COMPLETE)
```bash
./scripts/run_pattern_sweep.sh --learn-usage-patterns --verbose
```
Output: `rag/pattern-sweeps/pattern-sweep-09-15/pattern_sweep_data.json`

### Phase 2: Binocular Analysis with Pattern Data Integration

#### For Claude Code (Network/Semantic Analysis):
```markdown
Please conduct a comprehensive network/semantic analysis combining:
1. The pattern sweep data at `rag/pattern-sweeps/pattern-sweep-09-15/pattern_sweep_data.json`
2. Session logs from September 9-15, 2025
3. The OMNIBUS synthesis documents (GENESIS-DOCUMENTS-PACKAGE.md, PATTERNS-AND-INSIGHTS.md, etc.)

**METHODOLOGY: Network/Semantic Lens**
- Start by analyzing the pattern_sweep_data.json for code evolution patterns
- Map concept dependency relationships from session logs
- Track breakthrough moments (especially Friday's DDD refactoring)
- Identify knowledge architecture from this week's work
- Compare patterns detected by script vs. patterns in lived experience

**DELIVERABLES:**
1. Pattern validation report (script findings vs. actual experience)
2. Semantic network of this week's concepts
3. Critical path analysis (what led to 9/9 validation success)
4. Knowledge dependency graph
5. Gap analysis between automated detection and human insight

**OUTPUT**: Create analysis document at `rag/pattern-sweeps/pattern-sweep-09-15/code-semantic-analysis.md`
```

#### For Cursor (Thematic/Evolution Analysis):
```markdown
Please conduct a comprehensive thematic analysis combining:
1. The pattern sweep data at `rag/pattern-sweeps/pattern-sweep-09-15/pattern_sweep_data.json`
2. Session logs from September 9-15, 2025
3. The OMNIBUS synthesis documents

**METHODOLOGY: Spiral/Thematic Lens**
- Start by categorizing patterns from pattern_sweep_data.json
- Identify recurring themes across the week
- Map evolution from Monday's standup fixes to Friday's DDD victory
- Track methodology maturation patterns
- Validate the Excellence Flywheel in action

**DELIVERABLES:**
1. Theme clustering from both automated and manual analysis
2. Abstraction level progression (tactical fixes → architectural transformation)
3. Phase identification (what triggered the DDD cascade?)
4. Pattern categories with confidence scores
5. Methodology evolution insights

**OUTPUT**: Create analysis document at `rag/pattern-sweeps/pattern-sweep-09-15/cursor-thematic-analysis.md`
```

### Phase 3: Synthesis
After both agents complete their analysis, we synthesize into:
- Binocular synthesis document
- Pattern catalog updates
- Methodology refinements
