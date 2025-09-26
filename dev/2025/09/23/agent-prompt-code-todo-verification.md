# Agent Prompt: Verify TODO Count Reality

## Mission
The 5,394 TODO count seems suspicious. Verify what's real vs false positives before accepting this number.

## Investigation Tasks

### 1. Reproduce the Count with Different Methods
```bash
cd /Users/xian/Development/piper-morgan

# Method 1: Original count (what was used?)
grep -r "TODO" . --include="*.py" | grep -v "#[0-9]" | wc -l

# Method 2: Exclude archived/backup code
grep -r "TODO" . --include="*.py" | grep -v "#[0-9]" | grep -v "archive\|backup\|deprecated" | wc -l

# Method 3: Only active code (services, tests, cli, web)
grep -r "TODO" services/ tests/ cli/ web/ --include="*.py" | grep -v "#[0-9]" | wc -l

# Method 4: Actual TODO comments (with # prefix)
grep -r "# TODO" . --include="*.py" | grep -v "#[0-9]" | wc -l
```

### 2. Analyze Where TODOs Are Located
```bash
# Count by directory
for dir in services tests cli web archive docs; do
    if [ -d "$dir" ]; then
        count=$(grep -r "TODO" "$dir" --include="*.py" 2>/dev/null | grep -v "#[0-9]" | wc -l)
        echo "$dir: $count TODOs"
    fi
done

# Check if archives are inflating count
find . -path "*/archive/*" -o -path "*/backup/*" -o -path "*/deprecated/*" | grep -c "\.py$"
```

### 3. Sample the TODOs
```bash
# Get 10 random TODO examples
grep -r "TODO" . --include="*.py" | grep -v "#[0-9]" | shuf | head -10

# Check for pattern anomalies
grep -r "TODO" . --include="*.py" | grep -v "#[0-9]" | head -20
```

### 4. Identify False Positives
```bash
# Words containing "TODO" that aren't TODO comments
grep -r "TODO" . --include="*.py" | grep -v "^.*#.*TODO" | head -20

# Function names, variables, strings containing TODO
grep -r "TODO" . --include="*.py" | grep -v "#.*TODO" | head -20
```

## Evidence Format

### Count Breakdown
```
Method 1 (original): X TODOs
Method 2 (exclude archives): Y TODOs  
Method 3 (active code only): Z TODOs
Method 4 (actual # TODO comments): W TODOs

Location Breakdown:
- services/: X
- tests/: Y
- archive/: Z
- Other: W
```

### Sample Analysis
```
Random TODO samples:
[paste 10 examples]

False positives found:
[list any non-TODO matches]

Pattern observed:
[describe what's being counted]
```

### Reality Check
```
Realistic TODO count: [final number]
False positive count: [number]
Archive inflation: [number]

Conclusion: [what's the real scope of TODO cleanup?]
```

## Success Criteria
- Understand what the 5,394 number actually represents
- Identify real TODO count for active code
- Determine if this is GREAT-1C concern or separate project

## Time Box
10 minutes - quick verification, not exhaustive analysis

Report findings with honest assessment of TODO cleanup scope.
