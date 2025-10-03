# The Plugin Architecture Nobody Asked For

*October 3*

Yesterday we built a plugin system for four plugins. If that sounds like over-engineering, let me explain why it's not completely ridiculous.

## The setup

GREAT-3A—our third major epic in the plugin architecture sequence—started with what seemed like a clear mission: extract our four integrations (Slack, GitHub, Notion, Calendar) into plugins. The gameplan assumed we'd need to pull apart embedded code and restructure everything around a new plugin interface.

Then we actually looked at the code.

Main.py, which the documentation claimed was a bloated 1,107 lines, turned out to be 141 lines of clean microservice orchestration. The integration routers we thought were scattered across the codebase were exactly where they should be, in `services/integrations/`. We didn't need extraction. We needed *wrapping*.

This is where methodology becomes infrastructure.

## When four things reveal a pattern

Our config pattern analysis told the real story. We had four integrations. Three different approaches to configuration:

- **Slack**: Clean service injection with a dedicated `SlackConfigService`
- **GitHub**: Had a config service but the router wasn't using it
- **Notion**: No config service at all—just reading environment variables directly
- **Calendar**: Same as Notion, grabbing credentials straight from the environment

Pattern compliance? **25%** (one of four doing it right).

[ADD PERSONAL ANECDOTE: Have you ever discovered your team has been solving the same problem three different ways? That moment when you realize nobody talked to each other about the approach?]

The question wasn't "should we build a plugin system?" The question was: "We're about to standardize these four things anyway—what's the marginal cost of making it *systematic*?"

## The config compliance sprint

Here's where the time-boxed methodology meets reality. We tackled config standardization one integration at a time, with our test suite becoming both validator and teacher.

**Phase 1B: Notion** (30 minutes estimated, 23 minutes actual)
Created `NotionConfigService` following the Slack pattern exactly. Not "inspired by" or "similar to"—we literally used Slack as a template. One integration at a time. Compliance: 50%.

**Phase 1C: GitHub** (30 minutes estimated, 15 minutes actual)
The existing `GitHubConfigService` was already complete. We just needed to wire it to the router. Update the constructor signature, add the parameter, done. Compliance: 75%.

**Phase 1D: Calendar** (60-90 minutes estimated, 24 minutes actual)
Created `CalendarConfigService`, updated the adapter, verified the integration. Our test suite immediately validated everything. Compliance: **100%**.

From 25% to 100% in a single day. Zero regressions. 38 config compliance tests passing.

## The plugin wrapper pattern

Once the config services were standardized, the plugin wrappers became almost trivial. Each one implements the same `PiperPlugin` interface with six required methods:

```python
class NotionPlugin(PiperPlugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="notion",
            version="1.0.0",
            description="Notion workspace integration",
            capabilities=["routes", "mcp"]
        )

    def get_router(self) -> Optional[APIRouter]:
        # Returns FastAPI router with status endpoint

    def is_configured(self) -> bool:
        return self.config_service.is_configured()

    async def initialize(self) -> None:
        # Startup logic

    async def shutdown(self) -> None:
        # Cleanup logic

    def get_status(self) -> Dict[str, Any]:
        # Health reporting
```

The wrappers don't replace the integration routers—they *coordinate* them. The router does the work, the plugin wrapper provides lifecycle management and registration.

Auto-registration happens via module import:
```python
# At module level
_notion_plugin = NotionPlugin()
get_plugin_registry().register(_notion_plugin)
```

Import the module, the plugin registers itself. No explicit registration calls scattered through startup code.

## Why this isn't over-engineering

Let me address the obvious question: why build plugin infrastructure for exactly four plugins?

Because we were doing the work anyway.

The config standardization? That was fixing refactoring artifacts from earlier domain-driven design work. We needed to do it regardless of plugins. The interface definition? That clarified the contract all integrations needed to follow. The registry? That replaced ad-hoc router mounting with systematic lifecycle management.

The marginal cost of making it a proper plugin system was essentially:
- Define the interface (265 lines)
- Create the registry (266 lines)
- Write four thin wrappers (417 lines total)
- Build the test suite (126 lines)

About 1,000 lines of infrastructure code. In return:

**The fifth integration becomes trivial.** Not "easier"—trivial. Implement six methods, import the module, done. The test suite validates interface compliance automatically. The registry handles lifecycle. The router mounts itself.

**Zero breaking changes.** All existing functionality preserved. 72/72 tests passing. Config compliance at 100%.

**Documentation through structure.** The plugin interface *is* the documentation. Every plugin implements the same contract, follows the same patterns, reports status the same way.

This is what "Time Lord Philosophy" means in practice—taking the time to do it right because you're doing it anyway, and that investment makes everything afterward easier.

## The multi-agent coordination moment

[CONSIDER: Include brief aside about Code and Cursor agents finishing simultaneously multiple times, or save for future "working with AI" piece?]

Worth noting: this wasn't solo work. Two AI coding agents (Code and Cursor) were working in parallel across different phases, consistently finishing within minutes of each other. Not because we had perfect task estimates, but because the methodology created clear boundaries. When Phase 1C finishes, Phase 1D can start—regardless of which agent is handling which.

The Lead Developer's post-session satisfaction assessment called it "energizing" rather than exhausting. Low cognitive load from systematic approach, watching the methodology manifest in practice, clear progression feeling productive.

That's the feedback loop: methodology reduces overhead, which creates space for noticing patterns, which improves methodology.

## What this means for you

You probably don't need a plugin system. Not today.

But if you find yourself with three or four things that do similar work in different ways, and you're about to standardize them anyway—that's the moment. The marginal cost of systematization when you're already touching every integration is surprisingly low.

The questions to ask:
- Are we doing this work regardless? (Config standardization, interface clarification, lifecycle management)
- What's the marginal cost of making it systematic?
- Does this create infrastructure for future work or just wrap current work?

For us, the answers were: yes, minimal, and creates infrastructure.

Your mileage will vary. But don't assume "plugin system" automatically means over-engineering. Sometimes it just means finishing what you started.

---

*Next on Building Piper Morgan: GREAT-3B continues the plugin architecture work with advanced features—now that the foundation is solid, what becomes possible?*

*Have you ever systematized something "too early" and later been glad you did? Or gone the other way and regretted not building infrastructure sooner?*
