# **NewApp – Multi-Party, Multi-Agent Conversational Modeling Platform**

**Product Requirements Document – Draft v0.3**

---

## **1\. Product Summary**

NewApp is a multi-user conversational platform where:

* A “conversation” is a **structured model**, not just a linear chat log.

* Multiple users each have their own **on-my-side AI agent**.

* A **facilitator AI agent** helps the group move toward shared outcomes.

* Users can **type, annotate, react, edit, and view** the conversation in multiple ways.

* The same underlying model supports multiple “views” (tasks, questions, agreements, scenes, itinerary, etc.), and can spin out into other tools (wiki, GitHub, Jira, calendar).

The goal is to enable each person to **rapidly, independently, and asynchronously contribute**, while the system (and agents) help them **unify and reconcile** the various contributions into coherent artifacts and decisions.

---

## **2\. Core Concepts**

### **2.1 Conversation as Model**

* The conversation is a **graph** of `Element_node`s and `Element_link`s, representing:

  * Messages, edits, annotations

  * Questions, answers

  * Tasks, decisions, rules

  * Domain-specific entities (characters, scenes, locations, itinerary items, etc.)

* This graph is the **single source of truth**.

* All UX is “one model, many views” over this graph.

### **2.2 Many Views from One Model**

Examples of views:

* **Timeline/Chat View** – “normal” chronological chat.

* **Thread / Outline View** – hierarchical tree view of discussion.

* **Tasks View** – tasks (open/closed) extracted from conversation.

* **Questions View** – open questions and their answers.

* **Agreements / Disagreements View** – commitments, conflicts, divergences.

* **Domain-specific Views**:

  * Movie-making: characters, settings, scenes, beats.

  * Travel: itinerary timeline, constraints, budget.

  * Healthcare: care plan, visit summary, follow-ups.

Each view is a projection of the underlying graph; switching views never changes the underlying model, only the presentation.

### **2.3 Agents**

* **Personal Agent (per user, per conversation)**

  * Configured by the user (model, style, goals, skills).

  * Provides private “whispers”: suggestions, reminders, questions.

  * Sees only allowed parts of the graph (per user configuration).

  * Can propose text or artifacts that the user can accept/edit/publish.

* **Facilitator Agent (per conversation)**

  * Configured for the conversation’s purpose (business plan, care plan, travel itinerary, movie structure, etc.).

  * Reads the whole conversation model (unless restricted by domain).

  * Produces summaries, highlights conflicts, suggests next steps, structures artifacts.

---

## **3\. Key User Gestures (MVP)**

1. **Type/write at any time**

   * Input goes to the **current insertion point**:

     * Default: bottom of main timeline view.

     * Or: as a **reply/annotation** to currently selected text/node.

   * User can explicitly choose whether the new text is:

     * A top-level message

     * A threaded reply

     * An annotation or label (e.g., “task”, “question”, “rule”, “character”).

2. **Propose/make edits to text**

   * User can select an existing node and:

     * Propose an edit (creates an “edit proposal” node linked to the original).

     * Optionally apply the edit (if they have edit rights).

   * Edits are recorded as separate nodes with version/diff info.

3. **Change view of the conversation**

   * User can switch between:

     * Timeline view

     * Thread view

     * Tasks view

     * Questions view

     * Agreements view

     * Domain-specific views (movie, travel, etc., when applicable).

4. **Ask questions about the conversation / request summary**

   * At any time, user can:

     * Ask “meta” questions: “What are the open issues?”, “What did we decide about X?”

     * Request summaries at different levels: “Summarize the last 10 minutes”, “Summarize the discussion about character Y.”

   * These queries go to personal agent or facilitator, depending on intent.

5. **Agent interactions (implicit/explicit)**

   * User can:

     * View personal agent suggestions.

     * Accept / edit / reject suggestions.

     * Promote agent suggestions to shared conversation or artifacts.

     * Ask the agent to “explain why this is relevant.”

---

## **4\. What is Sent to the LLM**

We explicitly define the context for LLM calls.

### **4.1 General Structure**

For each LLM call (personal or facilitator), the input context is:

* **A. Conversation Context**

  * A **relevant slice** of the conversation model (graph) represented as text \+ structured metadata.

  * This includes:

    * Selected node(s) plus ancestors/descendants.

    * Recent related nodes (by thread, semantics, or time).

    * Tags/labels (task, question, rule, character, scene, etc.).

    * Links that are relevant for the requested operation.

* **B. Agent Context**

  * Agent’s configuration:

    * Role/goal (“help this user advocate for themselves”, “facilitate a travel plan”).

    * Tone/style (“supportive, concise, action-oriented”).

    * Skills enabled (“when you see a commitment, propose a task for this user”).

  * Any **agent-specific prompt templates**.

* **C. Conversation-to-This-Point Summary \+ Excerpts**

  * High-level summary of conversation-so-far (short-term memory), maintained incrementally.

  * Selected raw excerpts for high-precision reasoning:

    * Most recent items.

    * Directly linked nodes to the query.

    * Domain-relevant items (e.g., all mentions of “Tokyo hotel”).

* **D. Short-term & Long-term Memory**

  * Short-term memory:

    * Rolling conversation summaries for this conversation.

  * Long-term memory:

    * User-specific knowledge (preferences, roles, background).

    * Conversation-specific goals and constraints (e.g., “We prefer train over car”, “We are making a sci-fi movie with low budget”).

  * These are stored in separate structures and injected as compact structured text.

* **E. RAG (Retrieval-Augmented Generation)**

  * If context is too large:

    * Use a retrieval layer to fetch relevant nodes, artifacts, and prior summaries.

    * The retrieval layer is aware of graph structure (nodes \+ links), not just plain text.

---

## **5\. Functional Requirements (with User Stories & Acceptance Criteria)**

Below are some key areas with user stories and acceptance criteria (AC).

### **5.1 Core Gesture: Typing & Insertion Point**

**User Story F1:**  
 As a user, I want to type text at any time, and have it appear either at the bottom of the main conversation or in relation to a specific selected text, so I can easily contribute without breaking my flow.

**Acceptance Criteria (F1-AC):**

1. **Default insertion**

   * Given I am viewing the timeline view and no specific node is selected,

   * When I type into the main input and press send,

   * Then a new `Element_node` is created as a child of the last top-level node (or a new top-level if appropriate) and appears at the bottom of the timeline.

2. **Reply insertion**

   * Given I have selected an existing node A,

   * When I choose “Reply” and send my message,

   * Then the message becomes a child of node A (threaded reply) and is visually connected to it.

3. **Annotation insertion**

   * Given I have selected a text span or node A,

   * When I create an annotation and label it as, e.g., “task” or “question”,

   * Then a new `Element_node` is created with `kind='annotation'`, linked to node A, and marked with the specified label.

---

### **5.2 Core Gesture: Propose / Make Edits**

**User Story F2:**  
 As a user, I want to propose edits to existing text so that we can iteratively refine content without losing the history of what was originally said.

**Acceptance Criteria (F2-AC):**

1. **Create edit proposal**

   * Given I have permission to propose edits and have selected node A,

   * When I choose “Propose Edit”, edit the text, and click “Save proposal”,

   * Then a new `Element_node` is created with:

     * `kind='edit_proposal'`

     * `parent_id` referencing A or linked with `link_type='variant_of'`

     * text containing the proposed new content.

2. **View edit relationships**

   * Given node A has one or more edit proposals,

   * When I open node A in the inspector,

   * Then I see a list of associated edit proposals and their creators.

3. **Apply edit**

   * Given I have permission to apply edits on node A and there is edit proposal B,

   * When I click “Apply edit” on B,

   * Then either:

     * A new version of A is created and marked as current (versioned model), OR

     * Node A’s text is updated, and the previous text is stored in version history.

(MVP: we choose one consistent strategy; spec TBD in technical design.)

---

### **5.3 Core Gesture: Change View**

**User Story F3:**  
 As a user, I want to change the view of the conversation (timeline, threads, tasks, questions, etc.), so I can focus on the aspects that matter to me right now.

**Acceptance Criteria (F3-AC):**

1. **View switching**

   * Given I am in timeline view,

   * When I select “Tasks view” from the view switcher,

   * Then the main pane switches to show:

     * Only nodes and/or artifacts labeled as tasks.

     * Information like title, owner, status, due date.

2. **View invariance of model**

   * Given I switch between timeline, threads, and tasks views,

   * When I inspect a specific node via its permalink in each view,

   * Then I see it refers to the same underlying node id and data, regardless of view.

3. **Conversation continuity**

   * Given I am in tasks view,

   * When I type a message,

   * Then the message is still added to the underlying model and is visible in timeline view as well.

---

### **5.4 Core Gesture: Ask Questions / Request Summary**

**User Story F4:**  
 As a user, I want to ask questions or request summaries about the conversation at any time, so I can get oriented quickly and understand what’s going on.

**Acceptance Criteria (F4-AC):**

1. **Request summary**

   * Given there is an ongoing conversation,

   * When I type “Summarize the last 20 messages” or click a “Summarize” button,

   * Then the facilitator (or my agent, depending on context) generates a summary using:

     * relevant conversation context

     * agent context

     * memory, RAG if needed

   * And that summary appears as a new `Element_node` of kind `summary`.

2. **Ask question about conversation**

   * Given the conversation model contains tasks, questions, and decisions,

   * When I ask “What are the open questions about location scouting?”

   * Then the system queries the conversation model (and optionally uses LLM to interpret the query) and returns a response listing relevant nodes/artifacts.

3. **Meta-questions to personal agent**

   * Given I have a personal agent configured,

   * When I ask in my private agent channel “What should I focus on next?”,

   * Then the agent uses:

     * my tasks and commitments

     * recent conversation context

   * And returns a personalized answer visible only to me.

---

### **5.5 LLM Interaction (Context Construction)**

**User Story F5 (Personal Agent):**  
 As a user, I want my personal agent’s suggestions to be grounded in my context and the relevant parts of the conversation, so that its advice feels accurate and helpful.

**Acceptance Criteria (F5-AC):**

1. **Context assembly**

   * Given I request personal agent help related to node A,

   * When the system calls the personal agent LLM,

   * Then the prompt includes:

     * A compact summary of the conversation so far (short-term memory).

     * The text of node A plus relevant related nodes.

     * My agent context (role, goals, tone).

     * Relevant user preferences from long-term memory.

2. **Token limit handling**

   * Given the conversation is large,

   * When context would exceed configured token limits,

   * Then the system uses RAG \+ summaries to include only the most relevant nodes, not the entire raw history.

3. **Exclusion of private content**

   * Given other users have private agents with private content,

   * When the system calls my personal agent,

   * Then it does not include other users’ private agent messages in the LLM input.

---

### **5.6 Multi-User, Multi-Agent Collaborative Use Case (Example)**

**User Story F6 (Movie-making):**  
 As two or more creators making a movie, we want to collaboratively build characters, scenes, and settings, while each having our own agent and a shared facilitator that helps us keep the story consistent and complete.

**Acceptance Criteria (F6-AC):**

1. **Create story elements**

   * Given we have a conversation with “Movie” mode enabled,

   * When we create character/scene/location nodes,

   * Then they are typed elements (`character`, `scene`, `location`) and are visible in the “Story view”.

2. **Link characters to scenes**

   * Given a scene node S and character node C,

   * When we annotate “C appears in S” or use a UI to add C to S,

   * Then a `link_type='involves_character'` edge is created between them.

3. **Facilitator checks consistency**

   * Given there are scenes with no resolved ending or missing characters,

   * When we request “Check for missing/contradictory story elements”,

   * Then the facilitator uses the model context to:

     * highlight missing scenes or unresolved arcs

     * propose next scenes or edits as suggestions.

---

## **6\. Non-Functional Requirements (MVP-level)**

* **Latency**

  * Chat/post operations: 200–300ms typical (excluding LLM).

  * LLM responses: \< a few seconds, with UI indication of “thinking”.

* **Consistency & Integrity**

  * All node / link operations are persisted and recoverable.

  * No cycles in parent-child paths.

  * Hyperlinks (permalinks) remain stable.

* **Security & Privacy**

  * Per-user access control on conversations.

  * Personal agent content never shared unless explicitly promoted.

  * LLM calls partitioned by user & role (personal vs facilitator) with correct context isolation.

* **Extensibility**

  * Data model supports additional node types and link types.

  * View system can introduce new domain views (movie, travel, healthcare).

---

## **7\. Open Design Questions (Explicitly Called Out)**

These are known places where the spec still needs detail:

1. **Versioning Model**

   * Immutable nodes and explicit versions vs. mutable nodes with append-only history?

   * How do we expose “diffs” in the UI?

2. **Conflict Resolution & Governance**

   * How do we handle conflicting edits (e.g., two people applying different edits to the same node)?

   * Do we introduce “proposals” and “approvals” as a standard workflow?

3. **View Definition Mechanism**

   * Static (coded) views vs. user-defined views using a schema / DSL?

4. **LLM Orchestration Strategy**

   * Standard prompt schemas per operation?

   * How aggressively should we summarize vs. retrieve raw text?

5. **Integration Layer**

   * Which external tools are in MVP: Calendar, GitHub, Jira, Notion, Google Docs?

   * How deep is the sync (one-way export vs. two-way sync)?

