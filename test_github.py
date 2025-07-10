# test_github_flow_preservation.py
async def test_github_ticket_creation_still_works():
    # Existing flow should remain unchanged
    intent = await classifier.classify("Create a ticket for the login bug")

    assert intent.category == IntentCategory.EXECUTION
    assert intent.action in ["create_github_issue", "create_ticket"]

    workflow = await workflow_factory.create_from_intent(intent)
    assert workflow is not None
