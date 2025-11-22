# SEC-RBAC Phase 3: Method Inventory for `is_admin` Parameter

**Task**: Add `is_admin: bool = False` parameter to all repository/service methods with ownership checks.

**Pattern**:
```python
# FROM:
async def update_list(self, list_id: str, updates: Dict, owner_id: Optional[str] = None) -> ...:
    filters = [Model.id == list_id]
    if owner_id:
        filters.append(Model.owner_id == owner_id)

# TO:
async def update_list(
    self, list_id: str, updates: Dict, owner_id: Optional[str] = None, is_admin: bool = False
) -> ...:
    filters = [Model.id == list_id]
    if owner_id and not is_admin:  # Skip ownership check if admin
        filters.append(Model.owner_id == owner_id)
```

---

## 1. UniversalListRepository
**File**: `/Users/xian/Development/piper-morgan/services/repositories/universal_list_repository.py`

### Methods to Modify:

#### `get_list_by_id` (Lines 39-49)
```python
async def get_list_by_id(
    self, list_id: str, owner_id: Optional[str] = None, is_admin: bool = False
) -> Optional[domain.List]:
```
- **Current check**: Line 44-45
- **Modification**: `if owner_id and not is_admin:`

#### `update_list` (Lines 141-155)
```python
async def update_list(
    self, list_id: str, updates: Dict, owner_id: Optional[str] = None, is_admin: bool = False
) -> Optional[domain.List]:
```
- **Current check**: Line 148-149
- **Modification**: `if owner_id and not is_admin:`

#### `update_item_counts` (Lines 157-189)
```python
async def update_item_counts(
    self, list_id: str, owner_id: Optional[str] = None, is_admin: bool = False
) -> None:
```
- **Current check**: Line 180-181
- **Modification**: `if owner_id and not is_admin:`

#### `delete_list` (Lines 191-203)
```python
async def delete_list(
    self, list_id: str, owner_id: Optional[str] = None, is_admin: bool = False
) -> bool:
```
- **Current check**: Line 194-195
- **Modification**: `if owner_id and not is_admin:`

**Total**: 4 methods

---

## 2. TodoRepository (in todo_repository.py)
**File**: `/Users/xian/Development/piper-morgan/services/repositories/todo_repository.py`

### TodoListRepository (Lines 24-171)

#### `get_list_by_id` (Lines 40-50)
```python
async def get_list_by_id(
    self, list_id: str, owner_id: Optional[str] = None, is_admin: bool = False
) -> Optional[domain.TodoList]:
```
- **Current check**: Line 45-46
- **Modification**: `if owner_id and not is_admin:`

#### `update_list` (Lines 97-111)
```python
async def update_list(
    self, list_id: str, updates: Dict, owner_id: Optional[str] = None, is_admin: bool = False
) -> Optional[domain.TodoList]:
```
- **Current check**: Line 104-105
- **Modification**: `if owner_id and not is_admin:`

#### `update_todo_counts` (Lines 113-140)
```python
async def update_todo_counts(
    self, list_id: str, owner_id: Optional[str] = None, is_admin: bool = False
) -> None:
```
- **Current check**: Line 131-132
- **Modification**: `if owner_id and not is_admin:`

#### `delete_list` (Lines 142-154)
```python
async def delete_list(
    self, list_id: str, owner_id: Optional[str] = None, is_admin: bool = False
) -> bool:
```
- **Current check**: Line 145-146
- **Modification**: `if owner_id and not is_admin:`

**Total**: 4 methods

---

## 3. FileRepository
**File**: `/Users/xian/Development/piper-morgan/services/repositories/file_repository.py`

### Methods to Modify:

#### `get_file_by_id` (Lines 54-62)
```python
async def get_file_by_id(
    self, file_id: str, owner_id: str = None, is_admin: bool = False
) -> Optional[UploadedFile]:
```
- **Current check**: Line 57-58
- **Modification**: `if owner_id and not is_admin:`

#### `increment_reference_count` (Lines 75-93)
```python
async def increment_reference_count(
    self, file_id: str, owner_id: str = None, is_admin: bool = False
):
```
- **Current check**: Line 78-79
- **Modification**: `if owner_id and not is_admin:`

#### `delete_file` (Lines 163-175)
```python
async def delete_file(
    self, file_id: str, owner_id: str = None, is_admin: bool = False
) -> bool:
```
- **Current check**: Line 166-167
- **Modification**: `if owner_id and not is_admin:`

**Total**: 3 methods

---

## 4. ProjectRepository
**File**: `/Users/xian/Development/piper-morgan/services/database/repositories.py`

### Methods to Modify:

#### `get_by_id` (Lines 179-193)
```python
async def get_by_id(
    self, project_id: str, owner_id: Optional[str] = None, is_admin: bool = False
) -> Optional[domain.Project]:
```
- **Current check**: Line 183-185
- **Modification**: `if owner_id and not is_admin:`

#### `list_active_projects` (Lines 202-211)
```python
async def list_active_projects(
    self, owner_id: Optional[str] = None, is_admin: bool = False
) -> List[domain.Project]:
```
- **Current check**: Line 205-206
- **Modification**: `if owner_id and not is_admin:`

#### `count_active_projects` (Lines 213-220)
```python
async def count_active_projects(
    self, owner_id: Optional[str] = None, is_admin: bool = False
) -> int:
```
- **Current check**: Line 216-217
- **Modification**: `if owner_id and not is_admin:`

#### `find_by_name` (Lines 222-232)
```python
async def find_by_name(
    self, name: str, owner_id: Optional[str] = None, is_admin: bool = False
) -> Optional[domain.Project]:
```
- **Current check**: Line 227-228
- **Modification**: `if owner_id and not is_admin:`

#### `get_project_with_integrations` (Lines 251-263)
```python
async def get_project_with_integrations(
    self, project_id: str, owner_id: Optional[str] = None, is_admin: bool = False
) -> Optional[domain.Project]:
```
- **Current check**: Line 256-257
- **Modification**: `if owner_id and not is_admin:`

**Total**: 5 methods

---

## 5. ProjectIntegrationRepository
**File**: `/Users/xian/Development/piper-morgan/services/database/repositories.py`

### Methods to Modify:

#### `get_by_project_and_type` (Lines 271-295)
```python
async def get_by_project_and_type(
    self,
    project_id: str,
    integration_type: IntegrationType,
    owner_id: Optional[str] = None,
    is_admin: bool = False
) -> Optional[domain.ProjectIntegration]:
```
- **Current check**: Line 282-290 (complex - joins with ProjectDB)
- **Modification**: Add `and not is_admin` to the owner_id conditional block

#### `list_by_project` (Lines 297-314)
```python
async def list_by_project(
    self,
    project_id: str,
    active_only: bool = True,
    owner_id: Optional[str] = None,
    is_admin: bool = False
) -> List[domain.ProjectIntegration]:
```
- **Current check**: Line 305-311 (complex - joins with ProjectDB)
- **Modification**: Add `and not is_admin` to the owner_id conditional block

**Total**: 2 methods

---

## 6. ConversationRepository
**File**: `/Users/xian/Development/piper-morgan/services/database/repositories.py`

### Status: No Methods with Ownership Checks

Lines 601-628 show ConversationRepository but it has no ownership checks:
- `get_conversation_turns` - no owner_id parameter
- `save_turn` - no owner_id parameter
- `get_next_turn_number` - no owner_id parameter

**Total**: 0 methods (no changes needed)

---

## 7. KnowledgeGraphService
**File**: `/Users/xian/Development/piper-morgan/services/knowledge/knowledge_graph_service.py`

### Methods to Modify:

#### `get_node` (Lines 86-90)
```python
async def get_node(
    self, node_id: str, owner_id: Optional[str] = None, is_admin: bool = False
) -> Optional[KnowledgeNode]:
```
- **Current check**: Delegates to `self.repo.get_node_by_id(node_id, owner_id)`
- **Modification**: Pass `is_admin` to repository method

#### `get_neighbors` (Lines 191-207)
```python
async def get_neighbors(
    self,
    node_id: str,
    edge_type: Optional[EdgeType] = None,
    direction: str = "both",
    owner_id: Optional[str] = None,
    is_admin: bool = False,
) -> List[KnowledgeNode]:
```
- **Current check**: Delegates to `self.repo.find_neighbors(node_id, edge_type, direction, owner_id)`
- **Modification**: Pass `is_admin` to repository method

#### `extract_subgraph` (Lines 209-308)
```python
async def extract_subgraph(
    self,
    node_ids: List[str],
    max_depth: int = 2,
    edge_types: Optional[List[EdgeType]] = None,
    node_types: Optional[List[NodeType]] = None,
    owner_id: Optional[str] = None,
    is_admin: bool = False,
) -> Dict[str, Any]:
```
- **Current check**: Line 230 - delegates to `self.repo.get_subgraph(node_ids, max_depth, owner_id)`
- **Modification**: Pass `is_admin` to repository method

#### `find_paths` (Lines 310-330)
```python
async def find_paths(
    self,
    source_id: str,
    target_id: str,
    max_paths: int = 5,
    max_depth: int = 5,
    owner_id: Optional[str] = None,
    is_admin: bool = False,
) -> List[List[KnowledgeNode]]:
```
- **Current check**: Delegates to `self.repo.find_paths(source_id, target_id, max_paths, owner_id)`
- **Modification**: Pass `is_admin` to repository method

#### `search_nodes` (Lines 472-534)
```python
async def search_nodes(
    self,
    node_type: Optional[NodeType] = None,
    search_term: Optional[str] = None,
    owner_id: Optional[str] = None,
    is_admin: bool = False,
    limit: int = 10,
) -> List[KnowledgeNode]:
```
- **Current check**: Lines 499-505 use owner_id for filtering
- **Modification**: `if node_type and owner_id and not is_admin:` (and other conditionals)

#### `traverse_relationships` (Lines 540-623)
```python
async def traverse_relationships(
    self,
    start_node_id: str,
    max_depth: Optional[int] = None,
    edge_types: Optional[List[EdgeType]] = None,
    owner_id: Optional[str] = None,
    is_admin: bool = False,
) -> List[Dict]:
```
- **Current check**: Line 598, 604 - uses owner_id in repo calls
- **Modification**: Pass `is_admin` to repository methods

#### `expand` (Lines 625-686)
```python
async def expand(
    self,
    node_ids: List[str],
    max_hops: int = 2,
    edge_types: Optional[List[str]] = None,
    owner_id: Optional[str] = None,
    is_admin: bool = False,
) -> Dict[str, Any]:
```
- **Current check**: Line 658, 682 - uses owner_id in repo calls
- **Modification**: Pass `is_admin` to repository methods

#### `get_relevant_context` (Lines 730-799)
```python
async def get_relevant_context(
    self,
    user_query: str,
    user_id: UUID,
    max_nodes: int = 10,
    is_admin: bool = False,
) -> Dict[str, Any]:
```
- **Current check**: Line 757, 779 - uses `str(user_id)` as owner_id
- **Modification**: Pass `is_admin` to `search_nodes` and `expand` methods

**Total**: 8 methods

### KnowledgeGraphRepository Methods (from repositories.py)

These are the underlying repository methods that also need updates:

#### `get_node_by_id` (Lines 331-341)
```python
async def get_node_by_id(
    self, node_id: str, owner_id: Optional[str] = None, is_admin: bool = False
) -> Optional[domain.KnowledgeNode]:
```

#### `get_edge_by_id` (Lines 372-382)
```python
async def get_edge_by_id(
    self, edge_id: str, owner_id: Optional[str] = None, is_admin: bool = False
) -> Optional[domain.KnowledgeEdge]:
```

#### `find_neighbors` (Lines 395-443)
```python
async def find_neighbors(
    self,
    node_id: str,
    edge_type: Optional[EdgeType] = None,
    direction: str = "both",
    owner_id: Optional[str] = None,
    is_admin: bool = False,
) -> List[domain.KnowledgeNode]:
```

#### `get_subgraph` (Lines 445-511)
```python
async def get_subgraph(
    self,
    node_ids: List[str],
    max_depth: int = 2,
    owner_id: Optional[str] = None,
    is_admin: bool = False
) -> Dict[str, Any]:
```

#### `find_paths` (Lines 513-540)
```python
async def find_paths(
    self,
    source_id: str,
    target_id: str,
    max_paths: int = 5,
    owner_id: Optional[str] = None,
    is_admin: bool = False
) -> List[List[domain.KnowledgeNode]]:
```

**Repository Total**: 5 additional methods in KnowledgeGraphRepository

---

## 8. FeedbackService
**File**: `/Users/xian/Development/piper-morgan/services/feedback/feedback_service.py`

### Methods to Modify:

#### `get_feedback` (Lines 77-92)
```python
async def get_feedback(
    self, feedback_id: str, user_id: Optional[UUID] = None, is_admin: bool = False
) -> Optional[Feedback]:
```
- **Current check**: Line 83-84
- **Modification**: `if user_id and not is_admin:`

#### `update_feedback` (Lines 126-162)
```python
async def update_feedback(
    self,
    feedback_id: str,
    update_data: FeedbackUpdateRequest,
    user_id: Optional[UUID] = None,
    is_admin: bool = False,
) -> Optional[Feedback]:
```
- **Current check**: Line 135-136
- **Modification**: `if user_id and not is_admin:`

#### `delete_feedback` (Lines 164-180)
```python
async def delete_feedback(
    self, feedback_id: str, user_id: Optional[UUID] = None, is_admin: bool = False
) -> bool:
```
- **Current check**: Line 168-169
- **Modification**: `if user_id and not is_admin:`

**Total**: 3 methods

---

## 9. PersonalityProfileRepository
**File**: `/Users/xian/Development/piper-morgan/services/personality/repository.py`

### Status: No Methods with Ownership Checks

The PersonalityProfileRepository uses `user_id` as a primary lookup key, not an ownership check:
- `get_by_user_id` - retrieves profile FOR a user (not verifying ownership)
- `save` - creates/updates profile (no ownership check)
- `delete` - deletes by user_id (no ownership check)

These are user-scoped operations, not shared resources with ownership validation.

**Total**: 0 methods (no changes needed)

---

## 10. TodoListRepository (wrapper in universal_list_repository.py)
**File**: `/Users/xian/Development/piper-morgan/services/repositories/universal_list_repository.py`

### Status: Wrapper - Delegates to UniversalListRepository

Lines 581-695 show TodoListRepository is a wrapper that delegates all operations to UniversalListRepository. The methods `get_list_by_id`, `update_list`, etc. all call the universal repo methods.

Since UniversalListRepository is already being updated (item #1 above), the TodoListRepository wrapper will automatically inherit the `is_admin` parameter through delegation.

**Total**: 0 methods (changes inherited from UniversalListRepository)

---

## Summary by Repository

| Repository/Service | File | Methods to Modify |
|-------------------|------|-------------------|
| UniversalListRepository | universal_list_repository.py | 4 |
| TodoListRepository (in todo_repository.py) | todo_repository.py | 4 |
| FileRepository | file_repository.py | 3 |
| ProjectRepository | repositories.py | 5 |
| ProjectIntegrationRepository | repositories.py | 2 |
| ConversationRepository | repositories.py | 0 (no ownership checks) |
| KnowledgeGraphService | knowledge_graph_service.py | 8 |
| KnowledgeGraphRepository | repositories.py | 5 |
| FeedbackService | feedback_service.py | 3 |
| PersonalityProfileRepository | repository.py | 0 (user-scoped, not ownership) |
| TodoListRepository (wrapper) | universal_list_repository.py | 0 (inherits from Universal) |

**Grand Total**: 34 methods across 7 repositories/services

---

## MODIFIED_METHODS Output

```python
MODIFIED_METHODS = {
    "UniversalListRepository": [
        "get_list_by_id",
        "update_list",
        "update_item_counts",
        "delete_list"
    ],
    "TodoListRepository": [
        "get_list_by_id",
        "update_list",
        "update_todo_counts",
        "delete_list"
    ],
    "FileRepository": [
        "get_file_by_id",
        "increment_reference_count",
        "delete_file"
    ],
    "ProjectRepository": [
        "get_by_id",
        "list_active_projects",
        "count_active_projects",
        "find_by_name",
        "get_project_with_integrations"
    ],
    "ProjectIntegrationRepository": [
        "get_by_project_and_type",
        "list_by_project"
    ],
    "ConversationRepository": [],
    "KnowledgeGraphService": [
        "get_node",
        "get_neighbors",
        "extract_subgraph",
        "find_paths",
        "search_nodes",
        "traverse_relationships",
        "expand",
        "get_relevant_context"
    ],
    "KnowledgeGraphRepository": [
        "get_node_by_id",
        "get_edge_by_id",
        "find_neighbors",
        "get_subgraph",
        "find_paths"
    ],
    "FeedbackService": [
        "get_feedback",
        "update_feedback",
        "delete_feedback"
    ],
    "PersonalityProfileRepository": [],
    "TodoListRepository_wrapper": []
}
```

---

## Implementation Notes

### 1. Signature Changes
All methods gain the parameter:
```python
is_admin: bool = False
```

### 2. Ownership Check Pattern
Change from:
```python
if owner_id:
    filters.append(Model.owner_id == owner_id)
```

To:
```python
if owner_id and not is_admin:
    filters.append(Model.owner_id == owner_id)
```

### 3. Complex Cases

**ProjectIntegrationRepository**: Uses JOIN with ProjectDB for ownership verification. Need to adjust the conditional block at lines 282-290 and 305-311:

```python
# Current (lines 282-290)
if owner_id:
    from .models import ProjectDB
    result = await self.session.execute(
        select(ProjectIntegrationDB)
        .where(and_(*filters))
        .join(ProjectDB, ProjectIntegrationDB.project_id == ProjectDB.id)
        .where(ProjectDB.owner_id == owner_id)
    )

# Modified
if owner_id and not is_admin:
    from .models import ProjectDB
    result = await self.session.execute(
        select(ProjectIntegrationDB)
        .where(and_(*filters))
        .join(ProjectDB, ProjectIntegrationDB.project_id == ProjectDB.id)
        .where(ProjectDB.owner_id == owner_id)
    )
```

### 4. Service → Repository Delegation

**KnowledgeGraphService** methods that delegate to repository methods must pass `is_admin` through:

```python
# Service method
async def get_node(
    self, node_id: str, owner_id: Optional[str] = None, is_admin: bool = False
) -> Optional[KnowledgeNode]:
    return await self.repo.get_node_by_id(node_id, owner_id, is_admin)  # Pass through
```

### 5. No Changes Needed

- **ConversationRepository**: Methods don't have ownership checks
- **PersonalityProfileRepository**: Methods are user-scoped, not ownership-based
- **TodoListRepository (wrapper)**: Inherits changes from UniversalListRepository
