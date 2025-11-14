# Phase 2: User Journey Mapping
**UX Investigation - Piper Morgan**
**Date**: November 13, 2025, 20:05 PT
**Investigator**: Claude Code (UXR)

---

## Executive Summary

This document maps 5 critical user journeys through Piper Morgan's ecosystem, identifying touchpoints, emotions, pain points, and opportunities at each step. The goal is to understand the **holistic user experience** across CLI, web, and Slack interactions, and identify where the experience feels fragmented vs. cohesive.

**Key Finding**: Users traverse **multiple context switches** (terminal → browser → Slack → back) without clear wayfinding or state synchronization. The product works well within each touchpoint but struggles at the **seams between touchpoints**.

---

## Journey Mapping Methodology

### Framework

Each journey is mapped with:
- **Steps**: Discrete actions user takes
- **Touchpoint**: Where the action happens (CLI, Web, Slack, etc.)
- **User Goal**: What they're trying to accomplish
- **Actions**: Specific UI interactions
- **Thoughts**: Internal monologue
- **Emotions**: Emotional state (😊 positive, 😐 neutral, 😤 frustrated)
- **Pain Points**: Friction encountered
- **Opportunities**: How we could improve this step

### Journey Diagrams

Each journey includes:
1. **Journey Map Table**: Step-by-step breakdown
2. **Emotional Journey Graph**: Emotional highs and lows
3. **Friction Analysis**: Critical pain points ranked
4. **Opportunity Scores**: Quick wins vs. long-term investments

---

## Journey 1: New User Onboarding (First-Time User Experience)

### Persona

**Alex - New Alpha Tester**
- Role: Product Manager at tech startup
- Tech Comfort: High (comfortable with CLI, GitHub, Docker)
- Motivation: Wants AI assistant for PM tasks
- Expectation: "Should be like GitHub Copilot but for PM work"

### Context

Alex received an email invitation to alpha test Piper Morgan. They clicked the GitHub repo link and are starting from scratch.

---

### Journey Map

| Step | Touchpoint | User Goal | Actions | Thoughts | Emotion | Pain Points | Opportunities |
|------|------------|-----------|---------|----------|---------|-------------|---------------|
| **1. Discover** | Email/GitHub | Understand what Piper is | Read README, scan repo | "Okay, AI assistant for PMs. Sounds useful." | 😊 Curious | README might be outdated | ✅ Clear value prop in README |
| **2. Prerequisites Check** | Terminal | Verify system requirements | Check Python version, Docker status | "Do I have Python 3.12? Let me check..." | 😐 Neutral | May not have Python 3.12 installed | 🔄 Clearer error messages for missing deps |
| **3. Clone Repo** | Terminal | Get code locally | `git clone`, `cd piper-morgan` | "Standard git workflow, familiar." | 😊 Confident | SSH key setup if not configured | ✅ Setup wizard helps with SSH |
| **4. Run Setup Wizard** | Terminal | Get Piper running | `python main.py setup` | "Okay, interactive setup. Nice." | 😊 Pleased | Wizard is ~10 minutes, feels long | 🔄 Progress indicators? |
| **4a. Python 3.12 Check** | Terminal | Verify Python version | Wizard checks automatically | "Good, it's checking for me." | 😊 Relieved | If missing: must install and restart | 🔄 Link to Python installer |
| **4b. Virtual Environment** | Terminal | Isolate dependencies | Wizard creates venv, installs packages | "This is taking a while... 2-3 minutes?" | 😐 Waiting | Dependency installation is slow | ℹ️ Expected, hard to avoid |
| **4c. SSH Key Setup** | Terminal | GitHub access | Wizard generates key, copies to clipboard | "Oh, it's helping me with SSH! Nice touch." | 😊 Delighted | Must switch to browser, paste in GitHub | 🔄 Open GitHub settings automatically? |
| **4d. Docker Check** | Terminal | Verify Docker running | Wizard checks Docker status | "Uh oh, Docker's not running..." | 😤 Frustrated | Must open Docker Desktop manually | 🚨 **CRITICAL**: Auto-start Docker? Or clearer guidance |
| **4e. Docker Services** | Terminal | Start databases | `docker-compose up -d`, wait 30-60s | "Okay, pulling images... this is really slow." | 😐 Impatient | First-time Docker pulls take 5-10 minutes | 🔄 Better progress feedback |
| **5. Create Account** | Terminal | Set up user credentials | Enter username, email, password (2x) | "Password twice, okay, security. Makes sense." | 😊 Confident | Typing password in terminal (no dots) | ℹ️ Uses getpass (hidden input) |
| **6. API Keys** | Terminal | Configure AI providers | Paste OpenAI key, optionally Anthropic/GitHub | "Wait, where's my OpenAI key again? Let me find it..." | 😤 Frustrated | **Must leave terminal to find API keys** | 🚨 **CRITICAL**: Support env vars (already does!), clearer instructions |
| **6a. Key Validation** | Terminal | Verify keys work | Wizard validates against provider APIs | "Validating... good, don't want to find out later it's wrong." | 😊 Reassured | Slow (API calls to OpenAI/Anthropic) | ℹ️ Necessary, could show "This may take 10s" |
| **7. Setup Complete** | Terminal | Confirm success | See success message, next steps | "Okay! Now what? It says 'python main.py'..." | 😊 Accomplished | **No clear indication of what happens next** | 🚨 **CRITICAL**: "Next: Open http://localhost:8001" |
| **8. Start Piper** | Terminal | Launch the app | `python main.py` (or `venv/bin/python main.py`) | "Is it running? I see logs scrolling..." | 😐 Uncertain | **No clear "Server started" message** | 🔄 Print "✅ Piper running at http://localhost:8001" |
| **9. Open Browser** | Browser | Access web interface | Navigate to `http://localhost:8001` | "Okay, opening browser... what will I see?" | 😊 Curious | **User must manually type URL** | 🔄 Auto-open browser? Or copy-paste URL shown |
| **10. First Impression** | Web | Understand interface | See home page, greeting, input box | "Simple chat interface. I know how this works." | 😊 Confident | **Not obvious I'm logged in** (no username shown) | 🚨 **GAP**: No logged-in indicator |
| **11. First Message** | Web | Test Piper | Type "Hello, can you help me with standup?" | "Let's see what it can do..." | 😊 Excited | None | ✅ Works well |
| **12. See Response** | Web | Get AI response | Bot message appears with markdown | "Okay, it's working! This is cool." | 😊 Delighted | None | ✅ Good experience |
| **13. Discover Features** | Web | Explore capabilities | Try example prompts, upload document | "What else can it do? Let me click examples..." | 😊 Engaged | **No navigation to other features** (standup, learning, settings) | 🚨 **CRITICAL**: No feature discovery mechanism |
| **14. Try Standup** | Browser (new tab?) | Generate standup report | **How do I get there?** Must type `/standup` URL manually | "Wait, how do I access standup? Is there a menu?" | 😤 Frustrated | 🚨 **CRITICAL PAIN POINT**: No navigation between features |
| **15. Lost** | Web | Figure out what's available | Searches documentation? Reads email again? | "What features exist? How do I find them?" | 😤 Confused | **Poor feature discoverability** | 🚨 **CRITICAL**: Need navigation menu |

---

### Emotional Journey Graph

```
Emotion
😊 High  |     *         *              *  *      *
         |    * *   *   * *            * ** *
😐 Mid   | *     * * * *   *        * *      *
         |                  *      *            *
😤 Low   |                   **  **              ***
         |________________________________________________
         1  2  3  4  5  6  7  8  9  10 11 12 13 14 15

Key Emotional Moments:
- Peak 1: SSH key helper (delighted)
- Trough 1: Docker not running (frustrated)
- Trough 2: Finding API keys (frustrated)
- Peak 2: First successful message (delighted)
- Trough 3: Can't find other features (confused/frustrated)
```

---

### Critical Pain Points (Ranked by Severity)

| Rank | Pain Point | Impact | Frequency | Touchpoint Transition | Fix Difficulty |
|------|------------|--------|-----------|----------------------|----------------|
| 🥇 **1** | No navigation menu / feature discovery | HIGH | Every session | Web ↔ Web | Medium |
| 🥈 **2** | Docker not running (manual fix required) | HIGH | First-time only | Terminal | Medium |
| 🥉 **3** | No logged-in indicator | MEDIUM | Every session | N/A | Easy |
| 4 | Must find API keys externally | MEDIUM | First-time only | Terminal ↔ External | Easy (docs) |
| 5 | Slow Docker image pulls (5-10min) | MEDIUM | First-time only | Terminal | Hard (inherent) |
| 6 | No clear "server started" message | MEDIUM | Every startup | Terminal | Easy |
| 7 | Manual browser URL entry | LOW | Every startup | Terminal → Browser | Easy |

---

### Opportunities (Quick Wins vs. Long-term)

#### 🟢 Quick Wins (< 1 day)
1. **Add navigation menu** to web interface (header with links to all features)
2. **Show logged-in username** in header
3. **Print server URL** clearly when starting: "✅ Piper running at http://localhost:8001"
4. **Add "Welcome back, [username]"** to home page

#### 🟡 Medium Effort (1-3 days)
1. **Auto-open browser** after `python main.py` starts
2. **Better Docker guidance** in setup wizard (check if Docker Desktop is running, provide instructions)
3. **Progress indicators** during long operations (Docker pulls, dependency installs)
4. **Onboarding checklist** on first login: "Get started: 1. Try standup, 2. Customize personality, 3. Enable learning"

#### 🔴 Long-term (1+ weeks)
1. **Interactive tutorial** on first use (guided tour of features)
2. **Feature discovery nudges** ("Did you know Piper can generate standups?")
3. **Auto-start Docker** if possible (platform-specific)

---

### Jobs to Be Done (JTBD)

**Functional Jobs**:
- Get Piper installed and running ✅ (works, but slow)
- Verify it works with a test message ✅ (good experience)
- Understand what Piper can do ❌ (poor discoverability)

**Emotional Jobs**:
- Feel confident I'm set up correctly ⚠️ (unclear logged-in state)
- Feel excited about capabilities ⚠️ (can't discover features)
- Not feel frustrated by tech setup ❌ (Docker, API keys)

**Social Jobs**:
- Seem technically competent to team ✅ (CLI setup is standard)
- Be an early adopter of cool tech ✅ (works)

---

## Journey 2: Daily PM Workflow (Standup → Issue Creation)

### Persona

**Morgan - Busy Product Manager**
- Role: PM at mid-size company
- Context: Morning routine, 10 minutes before standup meeting
- Motivation: "I need my standup summary NOW"
- Tech Comfort: Medium (prefers GUI over CLI)

### Context

Morgan has been using Piper for 2 weeks. It's 8:50 AM, standup is at 9:00 AM, and they need to quickly generate their standup summary.

---

### Journey Map

| Step | Touchpoint | User Goal | Actions | Thoughts | Emotion | Pain Points | Opportunities |
|------|------------|-----------|---------|----------|---------|-------------|---------------|
| **1. Start Day** | Desktop | Begin work routine | Boot computer, open apps | "Okay, standup in 10 minutes. Need Piper." | 😐 Neutral | N/A | N/A |
| **2. Start Piper** | Terminal | Launch Piper | Open terminal, `cd piper-morgan`, `python main.py` | "Where's my terminal window from yesterday?" | 😐 Neutral | **Must navigate to directory manually** | 🔄 Add to PATH or create alias |
| **2a. Wait for Startup** | Terminal | Wait for services | Watch logs scroll | "Is it starting? How long does this take?" | 😐 Impatient | **30-60 second startup time** | 🔄 Faster startup or persistent services |
| **3. Open Browser** | Browser | Access Piper web | Navigate to `http://localhost:8001` | "Okay, typing the URL..." | 😐 Routine | **Must type URL every time** | 🔄 Bookmark or auto-open |
| **4. Navigate to Standup** | Browser | Get to standup feature | **How?** Types `/standup` in URL bar | "No menu, so I just add /standup to the URL." | 😤 Annoyed | 🚨 **NO NAVIGATION MENU** | 🚨 **CRITICAL**: Add nav menu |
| **5. Generate Standup** | Web (Standup) | Create report | Click "Generate Standup" button | "Please be fast, I have 8 minutes..." | 😐 Anxious | None | ✅ Works well |
| **6. Wait for Generation** | Web (Standup) | Wait for AI | Watch "Loading..." text | "How long is this taking?" | 😤 Impatient | **No progress indicator** (just "Loading...") | 🔄 Show "Analyzing 47 GitHub events..." |
| **7. Review Report** | Web (Standup) | Read summary | Scan yesterday/today/blockers | "Good, this looks right. Time to copy it..." | 😊 Satisfied | None | ✅ Good output |
| **8. Copy Summary** | Web (Standup) | Get text for Slack | Select all text, Cmd+C | "Copying... wait, do I want the whole thing?" | 😐 Neutral | **No "Copy to Clipboard" button** | 🔄 Add copy button |
| **9. Paste to Slack** | Slack | Share in standup channel | Switch to Slack, paste in channel | "Done. 2 minutes to spare." | 😊 Relieved | **Context switch to Slack** | 💡 Could Piper post directly to Slack? |
| **10. Team Asks Question** | Slack | Respond to colleague | Type response about blocker | "Oh yeah, we need to file an issue for that bug." | 😐 Remembering | None | N/A |
| **11. Create Issue** | Browser (GitHub) | File bug report | Switch to GitHub, click New Issue | "What was the blocker again? Let me check Piper..." | 😤 Frustrated | **Piper standup not saved/accessible** | 🚨 **GAP**: No standup history |
| **12. Search for Info** | Browser (Piper?) | Find blocker details | Go back to Piper? Or check GitHub events? | "Where did Piper get that info from?" | 😤 Confused | **Can't reference Piper's analysis** | 🔄 Save standup history |
| **13. File Issue Manually** | GitHub | Create issue | Fill out title, description, labels | "Doing this manually since I can't reference Piper." | 😤 Annoyed | **No integration with Piper** | 💡 Could Piper draft the issue? |
| **14. Back to Standup** | Slack/Zoom | Join meeting | Click Zoom link, join call | "Made it with 30 seconds to spare!" | 😊 Relieved | None | ✅ Mission accomplished |

---

### Emotional Journey Graph

```
Emotion
😊 High  |                       *                   *
         |                      * *
😐 Mid   | *  *  *  *  *  *  *      *  *  *
         |                              *  *  *
😤 Low   |       *           **             *  *
         |________________________________________________
         1  2  3  4  5  6  7  8  9  10 11 12 13 14

Key Emotional Moments:
- Trough 1: No nav menu (frustrated)
- Trough 2: Waiting for generation (impatient)
- Peak 1: Good standup output (satisfied)
- Trough 3: Can't reference Piper later (frustrated)
```

---

### Critical Pain Points

| Rank | Pain Point | Impact | Frequency | Fix Difficulty |
|------|------------|--------|-----------|----------------|
| 🥇 **1** | No navigation menu (must type URLs) | HIGH | Every use | Medium |
| 🥈 **2** | No standup history / can't reference later | HIGH | Often | Medium |
| 🥉 **3** | Slow startup (30-60s) | MEDIUM | Every day | Hard |
| 4 | No progress indicator during generation | MEDIUM | Every use | Easy |
| 5 | No "Copy to Clipboard" button | LOW | Every use | Easy |
| 6 | Must manually switch to Slack | LOW | Every use | Medium (Slack integration) |

---

### Opportunities

#### 🟢 Quick Wins
1. **Navigation menu** with links to all features
2. **"Copy to Clipboard" button** on standup page
3. **Progress indicator** during generation ("Analyzing 47 events...")
4. **Standup history** page (list of past standups)

#### 🟡 Medium Effort
1. **Persistent services** (don't shut down Piper between uses)
2. **Auto-open browser** on startup
3. **Slack integration** (post standup directly)
4. **Browser bookmark** helper or auto-bookmark on first use

#### 🔴 Long-term
1. **Piper suggests filing issues** based on blockers
2. **Draft GitHub issues** from standup blockers
3. **Integration with standup meetings** (Zoom, calendar)

---

### Jobs to Be Done

**Functional Jobs**:
- Generate standup summary quickly ✅ (works, ~30s)
- Share summary with team ⚠️ (works, but manual copy-paste)
- Reference standup later ❌ (no history)
- Follow up on blockers ❌ (no integration)

**Emotional Jobs**:
- Feel prepared for standup ✅ (good output)
- Not feel rushed/anxious ⚠️ (startup + navigation friction)
- Feel organized ❌ (can't track blockers)

---

## Journey 3: Learning Discovery (First Pattern Suggestion)

### Persona

**Taylor - Efficiency-Minded PM**
- Role: Senior PM, cares about workflows
- Context: Been using Piper for 1 week
- Motivation: "I want Piper to learn my patterns"
- Expectation: "Like Gmail's smart compose"

### Context

Taylor has been using Piper regularly and just enabled the learning feature. They're curious to see Piper's first pattern suggestion.

---

### Journey Map

| Step | Touchpoint | User Goal | Actions | Thoughts | Emotion | Pain Points | Opportunities |
|------|------------|-----------|---------|----------|---------|-------------|---------------|
| **1. Hear About Learning** | Email/docs | Discover feature | Read alpha update email | "Oh, Piper can learn patterns now? Interesting!" | 😊 Curious | **Didn't know feature existed** | 🔄 Feature announcement in UI |
| **2. Find Learning Settings** | Web | Enable learning | **How?** No menu, must know URL | "Where is this feature? Let me check the email..." | 😤 Frustrated | 🚨 **NO NAVIGATION** | 🚨 **CRITICAL**: Nav menu |
| **3. Navigate to Learning** | Browser | Access dashboard | Type `/assets/learning-dashboard.html` | "Why such a weird URL? This doesn't feel integrated." | 😤 Annoyed | **Non-standard URL pattern** | 🔄 Clean URLs (/learning) |
| **4. First Impression** | Learning Dashboard | Understand interface | See toggle, metrics, privacy controls | "Whoa, this is a lot. Dark theme? Didn't expect that." | 😐 Surprised | **Theme inconsistency** (dark vs light) | 🚨 Theme mismatch issue |
| **5. Enable Learning** | Learning Dashboard | Turn on feature | Click "Enable Learning" button | "Okay, clicking enable... it's asking for confirmation?" | 😐 Neutral | **Confirmation dialog** (native confirm) | ℹ️ Good for destructive action |
| **6. Confirm** | Learning Dashboard | Confirm choice | Click OK in dialog | "Yes, I want to enable it. Confirming..." | 😐 Neutral | None | ✅ Good |
| **7. See Status Change** | Learning Dashboard | Verify enabled | Badge changes to "Enabled", button changes to "Disable" | "Okay, it's on. Now what?" | 😊 Confident | **No guidance on what happens next** | 🔄 "Piper will now learn patterns..." message |
| **8. Wait for Pattern** | N/A | Use Piper normally | Over next few days, use Piper for PM tasks | "I wonder when I'll see a pattern..." | 😐 Wondering | **No indication of progress** | 💡 "Piper has observed 23 interactions" |
| **9. Discovery Pattern** | Web (Chat) | First suggestion appears | **How?** In chat? Notification? Email? | "How will I know when there's a pattern?" | 😐 Uncertain | 🚨 **UNCLEAR DELIVERY MECHANISM** | 🚨 **GAP**: No notification system |
| **10. Check Dashboard** | Learning Dashboard | Look for patterns | Go to dashboard (manual check) | "Let me check if there are patterns yet..." | 😊 Curious | **Must manually check** (no notifications) | 🔄 Notification system |
| **11. See First Pattern** | Learning Dashboard | Review suggestion | See "workflow automation" pattern, 87% confidence | "Oh! It found a pattern. What is it suggesting?" | 😊 Excited | **Pattern description unclear** | 🔄 Better explanation of what pattern means |
| **12. Accept Pattern** | Learning Dashboard | Approve learning | Click accept button | "Okay, accepting... what does this do?" | 😐 Uncertain | **Unclear impact of acceptance** | 🔄 "Piper will now auto-suggest..." explanation |
| **13. See Effect** | Web (Chat) | Experience learned behavior | **When?** Next relevant interaction? | "Did accepting it do anything? How will I know?" | 😤 Confused | 🚨 **NO VISIBLE CHANGE** after acceptance | 🚨 **GAP**: No feedback loop |
| **14. Wonder** | N/A | Question value | Think about whether learning is working | "Is this actually helping? I can't tell." | 😤 Doubtful | **No measurable impact** | 💡 Show impact metrics |

---

### Emotional Journey Graph

```
Emotion
😊 High  |  *                       *       *
         |
😐 Mid   |   *     *  *  *  *  *  *   *  *  *
         |    *   *                       *
😤 Low   |     ***                         ***
         |________________________________________________
         1  2  3  4  5  6  7  8  9  10 11 12 13 14

Key Emotional Moments:
- Trough 1: Can't find feature (frustrated)
- Trough 2: Dark theme surprise (confused)
- Peak 1: First pattern discovered (excited)
- Trough 3: No visible effect (confused/doubtful)
```

---

### Critical Pain Points

| Rank | Pain Point | Impact | Frequency | Fix Difficulty |
|------|------------|--------|-----------|----------------|
| 🥇 **1** | No visibility into learning's effect | HIGH | Ongoing | Hard (product design) |
| 🥈 **2** | No notification when patterns found | HIGH | Per pattern | Medium |
| 🥉 **3** | Unclear pattern delivery mechanism | HIGH | First time | Medium |
| 4 | No navigation to learning dashboard | HIGH | Every access | Medium (nav menu) |
| 5 | Theme inconsistency (dark vs light) | MEDIUM | Every access | Medium (design system) |
| 6 | Non-standard URL (/assets/...) | LOW | Every access | Easy (routing) |
| 7 | Unclear pattern descriptions | MEDIUM | Per pattern | Medium (UX writing) |

---

### Opportunities

#### 🟢 Quick Wins
1. **Add notification** when new pattern discovered ("🎯 Piper learned a new pattern!")
2. **Better pattern explanations** ("This pattern helps with X by doing Y")
3. **Show impact** after acceptance ("Piper will now suggest this in context Z")

#### 🟡 Medium Effort
1. **In-app notifications** system (toast messages)
2. **Progress indicator** ("Piper has analyzed 47 interactions, needs 20 more for pattern")
3. **Before/after examples** of learned behavior
4. **Learning journal** ("Piper learned X on Nov 10, used 5 times since")

#### 🔴 Long-term
1. **Proactive suggestions** in context (not just dashboard)
2. **Impact metrics** ("Saved you 2.5 hours this week")
3. **Pattern recommendations** ("You might want to teach Piper...")

---

### Jobs to Be Done

**Functional Jobs**:
- Enable learning feature ⚠️ (works, but hard to find)
- See what Piper learned ⚠️ (works, but must manually check)
- Approve/reject patterns ✅ (works)
- Experience learned behavior ❌ (no visibility)

**Emotional Jobs**:
- Feel confident learning is working ❌ (no feedback)
- Understand value of learning ❌ (no impact shown)
- Feel in control of learning ✅ (can disable, configure privacy)

**Social Jobs**:
- Customize Piper to my workflow ⚠️ (unclear if it's working)

---

## Journey 4: Cross-Channel Usage (Web → CLI → Slack)

### Persona

**Jordan - Multi-Tool Power User**
- Role: Technical PM, uses many tools
- Context: Working across terminal, browser, Slack throughout day
- Motivation: "I want to use Piper wherever I am"
- Expectation: "Like Slack - available everywhere"

### Context

Jordan is working on multiple tasks and wants to interact with Piper from different contexts without losing continuity.

---

### Journey Map

| Step | Touchpoint | User Goal | Actions | Thoughts | Emotion | Pain Points | Opportunities |
|------|------------|-----------|---------|----------|---------|-------------|---------------|
| **1. Morning - Web** | Browser | Check yesterday's standup | Open Piper, navigate to /standup | "What did I say yesterday? Let me check..." | 😐 Neutral | **No standup history** | 🚨 **GAP**: No history/logs |
| **2. Switch to Terminal** | Terminal | File GitHub issue via CLI | Open terminal, try `python main.py issues create` | "Can I do this from CLI?" | 😊 Hopeful | **CLI commands exist!** (good) | ✅ CLI works |
| **3. CLI Issue Creation** | Terminal | Describe issue | Enter title, description in prompts | "This is pretty smooth, nice!" | 😊 Pleased | None | ✅ Good experience |
| **4. Get Slack DM** | Slack | Colleague asks question | Receive Slack message: "What's blocker on XYZ?" | "Hmm, can I ask Piper in Slack?" | 😊 Curious | **Slack integration exists!** | ✅ Slack bot works |
| **5. DM Piper in Slack** | Slack | Ask about issue | Send DM to Piper: "What's the status of issue #42?" | "Let's see if this works..." | 😐 Uncertain | **Does Piper remember context?** | ❓ Context unclear |
| **6. Get Response** | Slack | Read Piper's answer | Piper responds with issue details | "Okay, it worked! But feels disconnected..." | 😐 Satisfied but uncertain | **Doesn't reference earlier web convo** | 🚨 **GAP**: No cross-channel context |
| **7. Back to Web** | Browser | Continue earlier task | Switch back to browser, see chat | "Wait, did my Slack question show up here?" | 😤 Confused | **Slack DM not in web chat history** | 🚨 **CRITICAL**: Separate contexts |
| **8. Confusion** | Browser | Figure out context | Look for Slack conversation in web | "These feel like two different Pipers..." | 😤 Frustrated | 🚨 **NO UNIFIED CONVERSATION HISTORY** | 🚨 **CRITICAL FINDING** |
| **9. Try CLI Command** | Terminal | Check recent chats | Try `python main.py history` or similar | "Can I see my history from CLI?" | 😐 Hopeful | **No history command?** (need to verify) | 🔄 Add CLI history command |
| **10. Settings** | Web | Adjust personality | Navigate to personality settings (/assets/personality-preferences.html) | "I want Piper more concise in Slack..." | 😊 Proactive | **Can I set different personalities per channel?** | 💡 Channel-specific settings |
| **11. Realization** | Mental model | Understand limitation | "Oh, these are three separate interfaces, not one Piper." | 😤 Disappointed | 🚨 **MENTAL MODEL MISMATCH** | 💡 Unified experience vision |

---

### Emotional Journey Graph

```
Emotion
😊 High  |   *  *  *  *
         |
😐 Mid   | *          *     *     *
         |              *     *
😤 Low   |                         **  *
         |________________________________________________
         1  2  3  4  5  6  7  8  9  10 11

Key Emotional Moments:
- Peak 1-4: CLI and Slack both work! (pleased)
- Trough 1: Conversations don't sync (frustrated)
- Trough 2: Mental model breaks (disappointed)
```

---

### Critical Pain Points

| Rank | Pain Point | Impact | Frequency | Fix Difficulty |
|------|------------|--------|-----------|----------------|
| 🥇 **1** | No unified conversation history | CRITICAL | Constantly | Hard (architecture) |
| 🥈 **2** | Web, CLI, Slack feel like separate Pipers | HIGH | Daily | Hard (product vision) |
| 🥉 **3** | No cross-channel context | HIGH | Often | Hard (state sync) |
| 4 | Can't set channel-specific preferences | MEDIUM | Rarely | Medium |
| 5 | No standup history/logs | MEDIUM | Daily | Medium |

---

### Opportunities

#### 🟢 Quick Wins
1. **Standup history** page (save past standups)
2. **CLI history** command to view recent conversations
3. **Visual indicator** of which "Piper" you're talking to

#### 🟡 Medium Effort
1. **Conversation ID** system (link web/CLI/Slack by thread)
2. **"View in web"** links from Slack/CLI responses
3. **Channel badges** in web ("This came from Slack")

#### 🔴 Long-term (Architectural)
1. **Unified conversation store** (all channels in one timeline)
2. **Cross-channel context** (Piper remembers Slack in web)
3. **Channel-specific settings** (different personality per channel)
4. **Conversation sync** (Slack DM appears in web chat)

---

### Jobs to Be Done

**Functional Jobs**:
- Access Piper from multiple tools ✅ (works)
- Maintain context across channels ❌ (doesn't sync)
- See unified history ❌ (separate)

**Emotional Jobs**:
- Feel like I'm talking to one assistant ❌ (feels fragmented)
- Trust Piper remembers our conversation ❌ (doesn't)
- Feel efficient across tools ⚠️ (works but disconnected)

**Mental Model Jobs**:
- Understand Piper as one entity ❌ **BROKEN**
- Know where to find past conversations ❌ (scattered)

---

## Journey 5: Configuration & Customization

### Persona

**Casey - Customization-Focused User**
- Role: PM who likes personalized tools
- Context: Week 2 of using Piper
- Motivation: "I want Piper to feel like MY assistant"
- Expectation: "Like customizing my IDE or Slack"

### Context

Casey wants to adjust Piper's personality, privacy settings, and learning preferences to match their workflow.

---

### Journey Map

| Step | Touchpoint | User Goal | Actions | Thoughts | Emotion | Pain Points | Opportunities |
|------|------------|-----------|---------|----------|---------|-------------|---------------|
| **1. Decide to Customize** | Mental | Personalize Piper | Think "I want Piper more concise" | "Let me find settings..." | 😊 Motivated | None | N/A |
| **2. Look for Settings** | Web | Find configuration | Look for settings icon, menu, gear icon | "Where are settings? I don't see a menu..." | 😤 Frustrated | 🚨 **NO SETTINGS LINK/ICON** | 🚨 **CRITICAL**: No navigation |
| **3. Search Documentation** | External | Find how to access settings | Google "piper morgan settings" or check docs | "Really? I have to look this up?" | 😤 Annoyed | **Poor discoverability** | 🔄 In-app help |
| **4. Navigate to Personality** | Browser | Access personality settings | Type `/assets/personality-preferences.html` | "Again with the weird /assets/ URL..." | 😤 Irritated | **Non-intuitive URL** | 🔄 Clean URL routing |
| **5. See Interface** | Personality Prefs | Understand options | See sliders, radio buttons, dark theme | "Okay, dark theme AGAIN. Why isn't this consistent?" | 😤 Confused | **Theme mismatch** | 🚨 Theme consistency |
| **6. Adjust Warmth** | Personality Prefs | Set preference | Drag warmth slider to 0.5 | "Okay, this slider is nice. Live preview!" | 😊 Pleased | None | ✅ Good UX |
| **7. See Live Preview** | Personality Prefs | Preview changes | Watch example text update | "Oh cool, I can see the difference!" | 😊 Delighted | None | ✅ **GREAT** UX |
| **8. Save** | Personality Prefs | Persist changes | Click "Save Preferences" | "Saving... does this affect Slack too?" | 😐 Uncertain | **Unclear scope** (web only? all channels?) | 🔄 Clarify scope |
| **9. Test in Chat** | Web (Chat) | Verify change | Send message, see if response feels different | "Hmm, maybe? Hard to tell with one message..." | 😐 Uncertain | **Subtle changes hard to notice** | 🔄 "Try asking X to see difference" |
| **10. Navigate to Learning** | Browser | Adjust learning settings | **How to get there?** No breadcrumb, no nav | "Where's the learning dashboard again?" | 😤 Annoyed | 🚨 **NO NAVIGATION BETWEEN SETTINGS PAGES** | 🚨 **CRITICAL** |
| **11. Type URL** | Browser | Access learning dashboard | Type `/assets/learning-dashboard.html` | "I'm memorizing URLs now..." | 😤 Frustrated | **User shouldn't memorize URLs** | 🚨 Navigation |
| **12. Privacy Settings** | Learning Dashboard | Configure privacy | Toggle switches for data retention | "Good, I have control over privacy." | 😊 Reassured | None | ✅ Good |
| **13. Save Privacy** | Learning Dashboard | Persist choices | Click "Save Privacy Settings" (appears after change) | "Okay, saved. Will this sync to Slack?" | 😐 Uncertain | **Unclear if privacy applies everywhere** | 🔄 Clarify scope |
| **14. Want to Review All Settings** | Mental | See all configurations | Think "What other settings are there?" | "Is there a settings overview?" | 😐 Wondering | 🚨 **NO SETTINGS OVERVIEW/INDEX** | 🚨 **GAP** |
| **15. Give Up** | Mental | Accept limitations | "I'll just remember these URLs..." | 😤 Resigned | **Poor settings UX** | 💡 Unified settings experience |

---

### Emotional Journey Graph

```
Emotion
😊 High  |          *  *
         |
😐 Mid   |                  *     *     *
         |  *
😤 Low   |   *** *    *  *   *  *   *  ***
         |________________________________________________
         1  2  3  4  5  6  7  8  9  10 11 12 13 14 15

Key Emotional Moments:
- Trough 1-4: Can't find settings (frustrated)
- Peak 1-2: Live preview works great! (delighted)
- Trough 5-6: No navigation between settings (frustrated)
- Trough 7: Give up on unified experience (resigned)
```

---

### Critical Pain Points

| Rank | Pain Point | Impact | Frequency | Fix Difficulty |
|------|------------|--------|-----------|----------------|
| 🥇 **1** | No settings menu / navigation | CRITICAL | Every access | Medium |
| 🥈 **2** | No settings overview/index page | HIGH | Often | Medium |
| 🥉 **3** | Unclear settings scope (web only? all channels?) | HIGH | Per change | Easy (docs/UX writing) |
| 4 | Non-intuitive URLs (/assets/...) | MEDIUM | Every access | Easy (routing) |
| 5 | Theme inconsistency (dark vs light) | MEDIUM | Every access | Medium (design system) |
| 6 | Hard to verify personality changes | LOW | After changes | Hard (UX design) |

---

### Opportunities

#### 🟢 Quick Wins
1. **Settings icon** in header/nav (links to settings index)
2. **Settings index page** (list all configurable areas)
3. **Clarify scope** ("These settings apply to web chat only")
4. **Breadcrumbs** ("Settings > Personality")

#### 🟡 Medium Effort
1. **Unified settings page** (all in one place)
2. **Settings search** ("Find setting...")
3. **Cleaner URLs** (/settings/personality, /settings/learning)
4. **Before/after test** for personality changes

#### 🔴 Long-term
1. **Global vs. channel-specific settings** ("Apply to web" vs "Apply everywhere")
2. **Settings sync** across devices
3. **Recommended settings** based on usage
4. **Import/export settings** (backup/restore)

---

### Jobs to Be Done

**Functional Jobs**:
- Find all available settings ❌ (poor discoverability)
- Customize Piper's behavior ✅ (works once you find it)
- Control privacy/learning ✅ (good controls)

**Emotional Jobs**:
- Feel in control of Piper ⚠️ (controls exist but hard to find)
- Trust privacy settings ✅ (transparent controls)
- Feel settings apply everywhere ❌ (unclear scope)

**Mental Model Jobs**:
- Understand what's configurable ❌ (scattered)
- Know where to find specific setting ❌ (must memorize URLs)

---

## Cross-Journey Insights

### Recurring Themes Across All Journeys

#### 🚨 Critical Issues (Found in 4+ Journeys)

1. **No Navigation Menu** (5/5 journeys)
   - Impact: Users must memorize URLs or guess
   - Frequency: Every session
   - Fix: Add header navigation to all pages

2. **No Feature Discoverability** (4/5 journeys)
   - Impact: Users don't know what Piper can do
   - Frequency: Ongoing
   - Fix: Feature tour, in-app hints, help center

3. **Theme Inconsistency** (3/5 journeys)
   - Impact: Jarring experience switching between pages
   - Frequency: Every multi-page session
   - Fix: Implement unified design system (Phase 1.3 tokens)

4. **Unclear Scope of Actions** (3/5 journeys)
   - Impact: Users don't know if settings/actions apply to web-only or all channels
   - Frequency: Per configuration change
   - Fix: Clear labeling ("Applies to: Web chat" badge)

#### ⚠️ High-Impact Issues

1. **No Unified Context/History** (Journey 4)
   - Web, CLI, Slack feel like separate assistants
   - No conversation sync
   - Mental model breaks

2. **No Feedback Loops** (Journey 3)
   - Learning feature has no visibility into impact
   - Users can't tell if it's working
   - Value unclear

3. **Slow/Unclear Startup** (Journey 1, 2)
   - 30-60s startup time
   - No clear "ready" indicator
   - Must manually open browser

#### ✅ Strengths to Preserve

1. **Live Preview** (Journey 5)
   - Personality settings show real-time changes
   - Users love this
   - Keep and expand

2. **CLI Tools Work Well** (Journey 4)
   - CLI commands are smooth
   - Power users appreciate this
   - Maintain quality

3. **Privacy Controls** (Journey 3, 5)
   - Transparent privacy settings
   - Users feel in control
   - Good trust-building

---

## Opportunity Matrix

### Priority Scoring (Impact × Frequency × Fix Ease)

| Opportunity | Impact | Frequency | Ease | Score | Phase |
|-------------|--------|-----------|------|-------|-------|
| **Add navigation menu** | 10 | 10 | 7 | 700 | 🟢 Quick Win |
| **Settings index page** | 9 | 8 | 8 | 576 | 🟢 Quick Win |
| **Logged-in indicator** | 7 | 10 | 9 | 630 | 🟢 Quick Win |
| **Standup history** | 9 | 8 | 6 | 432 | 🟡 Medium |
| **Unified theme (design system)** | 8 | 9 | 5 | 360 | 🟡 Medium |
| **Notification system** | 8 | 6 | 4 | 192 | 🟡 Medium |
| **Unified conversation history** | 10 | 7 | 2 | 140 | 🔴 Long-term |
| **Cross-channel context sync** | 9 | 6 | 2 | 108 | 🔴 Long-term |

*Scoring: Impact (1-10), Frequency (1-10), Ease of implementation (1-10, higher = easier)*

---

## Mental Model Analysis

### Current User Mental Model (BROKEN)

Users expect:
- ✅ "Piper is one AI assistant"
- ✅ "Piper remembers our conversation"
- ✅ "Settings apply everywhere"
- ✅ "I can access Piper from anywhere"

Reality:
- ❌ Piper is 3 separate interfaces (web, CLI, Slack)
- ❌ Conversations don't sync across channels
- ❌ Unclear if settings apply to all channels
- ❌ Can access, but context doesn't follow

### Desired Mental Model (NORTH STAR)

**"Piper is my personal AI assistant, available wherever I work, remembering our full conversation history"**

Components:
1. **One Identity**: Piper is one entity, not three
2. **Unified Memory**: Conversations sync across all channels
3. **Context Awareness**: Piper knows what we discussed in Slack when in web
4. **Consistent Behavior**: Same personality/settings everywhere (unless overridden)
5. **Accessible Everywhere**: Web, CLI, Slack, (future: mobile, email)

---

## Journey-Based Recommendations

### Immediate (Week 1-2)

1. **Add Navigation Menu** (Journeys 1-5)
   - Header with links: Home | Standup | Learning | Settings
   - Present on all pages
   - Responsive (mobile-friendly)

2. **Settings Index Page** (Journey 5)
   - `/settings` main page
   - Links to: Personality, Learning, Privacy, Account
   - Breadcrumbs for navigation

3. **Logged-in Indicator** (Journey 1)
   - Show username in header
   - "Settings" / "Logout" dropdown

4. **Clean URLs** (Journeys 3, 5)
   - `/learning` instead of `/assets/learning-dashboard.html`
   - `/settings/personality` instead of `/assets/personality-preferences.html`

### Short-term (Month 1-2)

1. **Standup History** (Journey 2)
   - Save past standups
   - `/standup/history` page
   - Searchable by date

2. **Notification System** (Journey 3)
   - Toast notifications for: patterns discovered, errors, confirmations
   - Non-intrusive (dismissible)
   - Accessible (ARIA live regions)

3. **Unified Design System** (Journeys 3, 5)
   - Implement Phase 1.3 design tokens
   - Light theme default
   - Dark theme as user preference

4. **Learning Feedback Loop** (Journey 3)
   - Show impact of learning ("Used 5 times this week")
   - Progress indicators ("23/50 interactions analyzed")
   - Clear pattern descriptions

### Long-term (Quarter 1-2)

1. **Unified Conversation Store** (Journey 4)
   - All channels write to one conversation log
   - Web shows Slack messages
   - Thread/conversation IDs

2. **Cross-Channel Context** (Journey 4)
   - Piper remembers context across channels
   - "Earlier you mentioned in Slack..."

3. **Channel-Specific Settings** (Journeys 4, 5)
   - "Apply to: Web | Slack | All"
   - Override global settings per channel

---

## Summary: Journey Mapping Insights

### Key Findings

1. **Fragmentation is the Core Problem**
   - Users experience Piper as 3 separate products
   - No navigation, no history sync, no unified identity
   - Mental model breaks repeatedly

2. **Discoverability Crisis**
   - Features exist but users can't find them
   - No menu, no feature tour, no in-app help
   - Users resort to memorizing URLs

3. **Great Micro-Interactions, Poor Macro-Experience**
   - Individual features work well (live preview, CLI, privacy)
   - But: transitions between features are broken
   - Missing the "wholeness of experience"

4. **Technical Constraints Create UX Debt**
   - Vanilla JS makes state sync hard
   - No framework makes navigation hard
   - But: can be solved with thoughtful patterns

### Path to Wholeness

**Short-term (Stitching the Seams)**:
- Add navigation menu (connect the islands)
- Create settings index (make configuration discoverable)
- Implement clean URLs (remove technical leakage)
- Show logged-in state (build trust)

**Medium-term (Building Coherence)**:
- Unified design system (one visual language)
- Notification system (proactive communication)
- History/logging (build continuity)
- Learning feedback (close the loop)

**Long-term (True Unity)**:
- Unified conversation model (one memory)
- Cross-channel context (one assistant)
- Mobile/email expansion (true omnichannel)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-13 21:30 PT
**Next**: Phase 3 - Design System Foundations
**Total Journey Mapping Time**: 1.5 hours
