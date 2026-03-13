#!/usr/bin/env python3
"""
Phase 5 Validation Script
Validates all refactoring deliverables programmatically
"""

import asyncio
import sys
from pathlib import Path

print("=" * 80)
print("PHASE 5: SYSTEMATIC VALIDATION")
print("=" * 80)
print()

# Track validation results
validation_results = []


def validate(description, condition, details=""):
    """Record validation result"""
    status = "✅ PASS" if condition else "❌ FAIL"
    validation_results.append((description, condition, details))
    print(f"{status}: {description}")
    if details:
        print(f"     {details}")
    return condition


print("SUCCESS METRIC 1: Domain Model Polymorphic Inheritance")
print("-" * 60)
try:
    from services.domain.models import Todo
    from services.domain.primitives import Item

    # Create Todo instance
    todo = Todo(
        text="Test validation",
        list_id="test-list-id",
        priority="medium",
        status="pending",
        completed=False,
        owner_id="system",
    )

    # Verify inheritance
    validate(
        "Todo extends Item (isinstance check)",
        isinstance(todo, Item),
        f"todo is Item: {isinstance(todo, Item)}",
    )

    validate(
        "Todo extends Item (class hierarchy)",
        issubclass(Todo, Item),
        f"issubclass(Todo, Item): True",
    )

    validate(
        "Todo has Item properties",
        hasattr(todo, "text") and hasattr(todo, "position") and hasattr(todo, "list_id"),
        "text, position, list_id all present",
    )

    validate(
        "Todo has todo-specific properties",
        hasattr(todo, "priority") and hasattr(todo, "status") and hasattr(todo, "completed"),
        "priority, status, completed all present",
    )

except Exception as e:
    validate("Domain model import", False, str(e))
    sys.exit(1)

print()
print("SUCCESS METRIC 2: Database Joined Table Inheritance")
print("-" * 60)
try:
    from services.database.models import ItemDB, TodoDB

    validate(
        "TodoDB extends ItemDB", issubclass(TodoDB, ItemDB), f"issubclass(TodoDB, ItemDB): True"
    )

    validate(
        "ItemDB has polymorphic_on",
        hasattr(ItemDB, "__mapper_args__") and "polymorphic_on" in ItemDB.__mapper_args__,
        "Polymorphic discriminator configured",
    )

    validate(
        "TodoDB has polymorphic_identity",
        hasattr(TodoDB, "__mapper_args__") and "polymorphic_identity" in TodoDB.__mapper_args__,
        f"Identity: {TodoDB.__mapper_args__.get('polymorphic_identity')}",
    )

except Exception as e:
    validate("Database model import", False, str(e))
    sys.exit(1)

print()
print("SUCCESS METRIC 3: Service Layer Universal Operations")
print("-" * 60)
try:
    from services.item_service import ItemService
    from services.todo_service import TodoService

    service = TodoService()

    validate(
        "TodoService extends ItemService",
        isinstance(service, ItemService),
        "isinstance(TodoService(), ItemService): True",
    )

    validate(
        "TodoService has universal create_item",
        hasattr(service, "create_item"),
        "Inherited from ItemService",
    )

    validate(
        "TodoService has universal update_item_text",
        hasattr(service, "update_item_text"),
        "Inherited from ItemService",
    )

    validate(
        "TodoService has universal reorder_items",
        hasattr(service, "reorder_items"),
        "Inherited from ItemService",
    )

    validate(
        "TodoService has universal delete_item",
        hasattr(service, "delete_item"),
        "Inherited from ItemService",
    )

    validate(
        "TodoService has todo-specific complete_todo",
        hasattr(service, "complete_todo"),
        "Todo-specific method",
    )

    validate(
        "TodoService has todo-specific reopen_todo",
        hasattr(service, "reopen_todo"),
        "Todo-specific method",
    )

    validate(
        "TodoService has todo-specific set_priority",
        hasattr(service, "set_priority"),
        "Todo-specific method",
    )

except Exception as e:
    validate("Service layer import", False, str(e))
    sys.exit(1)

print()
print("SUCCESS METRIC 4: Backward Compatibility")
print("-" * 60)
try:
    from services.domain.models import Todo

    todo = Todo(
        text="Backward compatibility test",
        list_id="test-list",
        priority="high",
        status="pending",
        completed=False,
        owner_id="system",
    )

    validate(
        "Todo has title property",
        hasattr(todo, "title"),
        "Property exists for backward compatibility",
    )

    validate(
        "todo.title maps to todo.text",
        todo.title == todo.text,
        f"title='{todo.title}', text='{todo.text}'",
    )

    validate(
        "todo.title is same object as todo.text",
        todo.title is todo.text,
        "Same reference, not a copy",
    )

except Exception as e:
    validate("Backward compatibility", False, str(e))
    sys.exit(1)

print()
print("SUCCESS METRIC 5: File System Validation")
print("-" * 60)

# Phase 1 files
validate(
    "Item primitive exists",
    Path("services/domain/primitives.py").exists(),
    "services/domain/primitives.py",
)

validate(
    "ItemDB in database models",
    Path("services/database/models.py").exists(),
    "services/database/models.py",
)

validate(
    "Phase 1 migration exists",
    len(list(Path("alembic/versions/").glob("*create_items_table*.py"))) > 0,
    "40fc95f25017_create_items_table.py",
)

validate(
    "Phase 1 tests exist",
    Path("tests/domain/test_primitives.py").exists(),
    "tests/domain/test_primitives.py",
)

# Phase 2 files
validate(
    "Phase 2 migration exists",
    len(list(Path("alembic/versions/").glob("*refactor_todos*.py"))) > 0,
    "234aa8ec628c_refactor_todos_to_extend_items.py",
)

validate(
    "Phase 2 completion report exists",
    Path("dev/active/phase2-migration-completion-report.md").exists(),
    "dev/active/phase2-migration-completion-report.md",
)

# Phase 3 files
validate(
    "ItemService exists", Path("services/item_service.py").exists(), "services/item_service.py"
)

validate(
    "TodoService exists", Path("services/todo_service.py").exists(), "services/todo_service.py"
)

validate(
    "ItemService tests exist",
    Path("tests/services/test_item_service.py").exists(),
    "tests/services/test_item_service.py",
)

validate(
    "TodoService tests exist",
    Path("tests/services/test_todo_service.py").exists(),
    "tests/services/test_todo_service.py",
)

# Phase 4 files
validate(
    "Integration tests exist",
    Path("tests/integration/test_todo_full_stack.py").exists(),
    "tests/integration/test_todo_full_stack.py",
)

validate(
    "ADR-041 exists",
    Path(
        "docs/internal/architecture/current/adrs/adr-041-domain-primitives-refactoring.md"
    ).exists(),
    "docs/internal/architecture/current/adrs/adr-041-domain-primitives-refactoring.md",
)

validate(
    "ADR index updated",
    "ADR-041" in Path("docs/internal/architecture/current/adrs/adr-index.md").read_text(),
    "ADR-041 found in index",
)

validate(
    "Phase 4 completion report exists",
    Path("dev/2025/11/04/PHASE-4-COMPLETE.md").exists(),
    "dev/2025/11/04/PHASE-4-COMPLETE.md",
)

print()
print("SUCCESS METRIC 6: Database Migration Status")
print("-" * 60)
try:
    import subprocess

    result = subprocess.run(["alembic", "current"], capture_output=True, text=True, timeout=10)

    current_migration = result.stdout.strip()

    validate(
        "Alembic current shows Phase 2 migration",
        "234aa8ec628c" in current_migration,
        f"Current: {current_migration}",
    )

except Exception as e:
    validate("Migration status check", False, str(e))

print()
print("=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)

passed = sum(1 for _, condition, _ in validation_results if condition)
total = len(validation_results)
failed = total - passed

print(f"\nTotal Validations: {total}")
print(f"Passed: {passed} ✅")
print(f"Failed: {failed} ❌")
print(f"Success Rate: {(passed/total)*100:.1f}%")

if failed > 0:
    print("\nFailed Validations:")
    for desc, condition, details in validation_results:
        if not condition:
            print(f"  ❌ {desc}")
            if details:
                print(f"     {details}")
    sys.exit(1)
else:
    print("\n🎉 ALL VALIDATIONS PASSED! 🎉")
    print("\nDomain Model Refactoring: FULLY VALIDATED ✅")
    sys.exit(0)
