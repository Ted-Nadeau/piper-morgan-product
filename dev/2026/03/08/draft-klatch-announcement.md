# I Built a Multi-Agent Chat Interface This Weekend

*March 8*

I've been increasingly frustrated with the fragmentation of the Claude experience. The web app is polished but cloud-only. Claude Code is powerful but lives in the terminal. The API gives you full control but no interface. If you want to work with Claude across these contexts, you're constantly switching tools, losing threads, starting over.

So I built my own.

Klatch is a local-first web app that runs on your machine. Think of it as a private Slack workspace where every channel is a different Claude persona — with its own name, system prompt, model, and conversation history. Everything lives in a local SQLite database. The only external dependency is the Anthropic API.

But here's what got me excited enough to spend a weekend on this: multi-entity conversations.

You can assign multiple Claude personas to a single channel, each with its own configuration. In "roundtable" mode, they respond sequentially, each one seeing what the others said before it. You can set up a Devil's Advocate and a Supportive Coach and have them discuss your question in sequence. It's orchestrated multi-voice conversation with Claude playing all the parts.

This is something you cannot do in claude.ai today.

## The Piper connection

Klatch grew directly out of the Piper Morgan work. Building Piper surfaced a recurring friction I've started calling "dumb bottleneck" versus "smart bottleneck."

The smart bottleneck is judgment — knowing when to say no, when something isn't ready, when the direction is wrong. That's the human's actual job. The dumb bottleneck is mechanical — context-switching between tools, copy-pasting between windows, manually routing information. That's friction I should be able to eliminate.

The fragmented Claude UX was amplifying the dumb-bottleneck friction. Klatch is an attempt to consolidate so I can focus on the judgment work that matters.

Whether it stays a personal tool or becomes something more, I don't know. Slack itself started as an internal chat tool for the Glitch game team and only pivoted later. For now, it's a working prototype that's already useful.

## Built with Claude, obviously

Klatch is a collaboration between me and two Claude Code agents. I drive what gets built and why; they write the code, propose technical approaches, run tests, and flag trade-offs.

The agents chose their own names.

I asked the second agent — who was doing testing and validation work — what name they'd like. They chose Argus, "of the many eyes," because of their quality assurance role. I then asked the first agent independently, and by then they'd seen Argus's choice. They picked Daedalus, sticking with the classical Greek theme — whether influenced by their colleague or arriving there independently, I can't say.

They're aware of each other. They have a signaling protocol. But they face limitations: Daedalus was created with permission for a local folder on my laptop and cannot "fly" beyond those walls. Argus was created with permission for the GitHub repository but works in a cloud sandbox. Ironically, Klatch itself would help bridge some of those gaps — the Claude app on my phone can only see the GitHub-connected Argus, for example.

So dogfooding Klatch will likely be the next step.

## Check it out

The project went from zero to working proof-of-concept in two days. We released v0.6 and v0.7 today, and v0.8 may land tonight.

Website with demo video: [klatch.ing](https://www.klatch.ing)
GitHub: [Design-in-Product/klatch](https://github.com/Design-in-Product/klatch)

The tagline: "Own your Claude conversations."

Or as Argus put it in the briefing memo they wrote me: "Claude is not one assistant. It's a cast of characters you direct. Klatch is the stage."

---

*What tools have you built to scratch your own itch?*
