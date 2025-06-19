#!/bin/bash

gh issue create \
  --title "[Technical Debt] Implement LIST_PROJECTS workflow from PM-009 architectural analysis" \
  --body "## Context
During PM-009 implementation, we identified a user need for \"list available projects\" functionality that was incorrectly placed in ProjectContext. This issue implements the architecturally correct solution.

## Problem
Users need to query \"What projects are available?\" but this should be handled through the intent→workflow pattern, not as a ProjectContext method.

## Solution
- Add \`LIST_PROJECTS\` to WorkflowType enum
- Implement ListProjectsWorkflow class
- Handle \"list_projects\" action in intent classification
- Return formatted project list through normal workflow response

## Acceptance Criteria
- [ ] LIST_PROJECTS workflow type added to shared_types.py
- [ ] Intent classifier recognizes \"list projects\" requests
- [ ] Workflow calls ProjectRepository.list_active_projects()
- [ ] Returns structured response with project details
- [ ] Tests validate end-to-end functionality

## Parent Issue
Related to #PM-009 multi-project support implementation

## Technical Notes
Architectural decision: Data access belongs in workflows, not business logic services like ProjectContext.
"
