Knowledge Hierarchies and Dependency Hell
Christian Crumlish
Christian Crumlish
Kind Director of Product, 18F alum, Product Management for UX People author, Piper Morgan (AI product assistant) maker, Design in Product curator, Layers of Meta bandleader


July 5, 2025
June 4–5, 2025

You know that moment when a simple feature request reveals a fundamental truth about your domain? That happened when I tried to upload my book to Piper Morgan.

“Just ingest a PDF,” I thought. “How hard could it be?”(Narrator: It was exactly as hard as it needed to be to teach important lessons.)

The knowledge hierarchy epiphany
While fighting with file uploads, I had to decide: Where does this knowledge go? That’s when I proposed a four-tier structure:

pm_fundamentals — Core PM knowledge (books, methodologies)
business_context — Company and industry specifics
product_context — Product details and history
task_context — Specific task patterns

This isn’t arbitrary. It mirrors the contextual layers PMs need to zoom between all the time. You can’t understand why your company does standups differently until you know what standups are supposed to accomplish. You can’t design product features without understanding the business model.

When we were building productivity software at CloudOn, we had no idea at first that we were going to pivot from virtualization (what Citrix does) to a native gesture-first interface, and we couldn’t really ever have figured out how to build that UI without first experiencing all the joys and sorrows of streaming video.

The hierarchy cascades. Each level assumes knowledge from the level above. Just like real life.

Enter dependency Hell
Of course, the moment I had this elegant architecture, Python decided to teach me humility.

First, the import errors:

pImportError: No module named 'services.knowledge_graph'
But I had a knowledge_graph directory! Turns out, Python cares deeply about whether you use hyphens or underscores. And whether your __init__.py file exists. And whether it's spelled correctly (not __init__ .py with a space, thanks Cursor Agent).

Then ChromaDB joined the party:

AttributeError: np.float_ was removed in NumPy 2.0
Cool. My vector database was incompatible with modern NumPy. Because of course it was. Over the next few weeks I would come to curse this “numpy mismatch.” Every time things weren’t working and I was trying to clean up an environment or a build eventually I’d have to downgrade NumPy. Eventually I asked how to pin the version but until I asked I was going to keep walking into that wall. And there are others like that.

The two-laptop tango
Did I mention I’m developing on two laptops? Personal (faoilean) and work (kindbook). Because apparently I enjoy pain.

This revealed gaps in our git workflow:

kindbook: “Everything works!”
faoilean: “What are these 47 missing dependencies?”
Me: “They’re the same code!”
Git: “Are they though?”

Premature initialization: it happens to everybody sometimes
The worst bug was subtle. The DocumentIngester was initializing before environment variables loaded:

# This runs when the module loads
ingester = DocumentIngester()  # ANTHROPIC_API_KEY not found!

# This runs when the server starts
load_dotenv()  # Too late!
Solution? Lazy initialization:

def get_ingester():
    return DocumentIngester()  # Created after env vars load
It’s not elegant. But it works. (My new motto.)

What I actually learned
Each frustration taught something:

Python’s import system is unforgiving — Respect the naming conventions or suffer
Version compatibility matters deeply — The AI ecosystem moves fast and breaks things
Lazy initialization prevents startup pain — Don’t create objects until you need them
Multi-laptop development keeps you honest — If it works on both, it’ll work anywhere

The payoff
After two days of fighting (and help from my AI assistants who kept apologizing for the confusion), we successfully:

Ingested Product Management for UX People into 85 searchable chunks
Tagged it with the pm_fundamentals domain
Verified search returns relevant, contextual results
Connected knowledge to our learning scaffolding

Now when someone asks Piper about PM/UX collaboration, it can reference actual content from my book. Not generic advice — specific passages about role definition and design partnerships. Or, it will be able too... once we, uh, teach it how to do that too.

The infrastructure reflection
This session reinforced something that often gets fast in this era of breaking things and vibing: Sometimes you need to slow down and think architecturally.

Every “quick fix” we considered would have made things worse:

Hardcoding paths? Breaks on the other laptop
Skipping initialization? Crashes on startup
Ignoring version warnings? ChromaDB won’t even load

But taking time to understand the problems — why imports failed, how initialization order matters, what dependency management means — that investment paid off immediately.

A love letter to boring solutions
The final architecture isn’t snazzy:

Standard Python package structure (boring!)
Lazy initialization pattern (ancient!)
Pinned dependency versions (conservative!)
Systematic debugging (methodical!)

But it works. On both laptops. Every time. And there can be beauty in boring old architecture that just works!

Next up in Building Piper Morgan: How we connected Piper’s understanding to actual workflows, and why sometimes the best architecture includes training wheels.

(Got war stories about debugging imports or multi-machine development? Share them below. Misery loves company, and I’m collecting tales of dependency hell for therapeutic purposes.)
