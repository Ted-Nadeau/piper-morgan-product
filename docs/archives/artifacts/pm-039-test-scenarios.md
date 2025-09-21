# PM-039 Test Scenarios & Validation Framework

## Objective

Prepare comprehensive testing approach for Code's intent pattern implementation for PM-039 (Intent Classification Coverage Improvements).

---

## Phase 1: Natural Language Test Scenarios

### Core Gaps (from previous validation)

- "search for requirements files"
- "find technical specifications"

### Variations

- "find X documents" (e.g., "find architecture documents")
- "search for Y files" (e.g., "search for meeting notes files")
- "locate Z specifications" (e.g., "locate API specifications")
- "show me all project plans"
- "get all design docs"
- "find docs about onboarding"
- "search for budget analysis documents"

### Edge Cases

- Typos: "serach for requirments files", "find tehcnical specfications"
- Partial phrases: "find requirements", "search files"
- Complex queries: "find all documents about project timeline and budget analysis"
- Ambiguous: "find stuff", "search"
- Negative: "find documents that do not mention budget"

### Positive Test Cases

- Each scenario above with expected intent/action and query extraction

### Negative Test Cases

- Unsupported queries: "draw a picture", "send an email"
- Malformed input: empty string, only whitespace, non-text input
- Out-of-domain: "what's the weather?"

---

## Phase 2: Validation Framework

### Systematic Validation Scripts

- Prepare curl commands for each scenario:
  - POST /api/v1/intent with {"message": "<test query>"}
  - Validate response: correct intent/action, query extraction, no "Unknown query action"
- Script to batch-run all curl commands and summarize results
- Monitor frequency of "Unknown query action" in responses
- Log all failures for review

### Success Criteria

- All core and variation queries return correct intent/action
- Edge cases handled gracefully (typos, partials, ambiguous)
- No regression in existing intent classification
- "Unknown query action" only for truly unsupported queries
- 95%+ accuracy for supported patterns

---

## Phase 3: Integration Test Preparation

### Full Pipeline Testing

- Natural language → intent classification → query router → FileQueryService → search results
- Validate end-to-end flow for all positive scenarios
- Confirm correct routing and search execution

### Performance Validation

- Ensure response times remain within 642x improvement window (<500ms, target: ~60ms)
- Monitor for any performance regressions during batch testing

### Regression Testing

- Re-run all existing intent and search tests
- Confirm no breakage of prior functionality
- Add tests for new patterns to test_intent_classification.py and integration suites

---

## Deliverables

- [ ] Comprehensive test scenario matrix (this document)
- [ ] Validation scripts (curl commands, batch runner)
- [ ] Success criteria checklist
- [ ] Integration test plan (documented here)

---

_Last updated: July 21, 2025_
