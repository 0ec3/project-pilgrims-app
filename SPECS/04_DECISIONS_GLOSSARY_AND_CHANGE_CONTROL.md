# 04 — DECISIONS, GLOSSARY, AND CHANGE CONTROL

## Document status
- **Type:** Normative governance document
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, design lead, content/religious governance contributors, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define canonical terminology, naming rules, decision-record standards, and controlled-change procedures so the product, codebase, and documentation system remain consistent over time.
- **Authority level:** If a term, naming pattern, or change process is unclear elsewhere, this file is the canonical source unless a more specific contract file explicitly defines a scoped exception.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `02-AI-AGENT-RULES-AND-WORKFLOW.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`
- **Related files:** All files, with strongest linkage to `05`, `07`, `08`, `13`, `14`, `16`, `18`–`26`, `28`, and `30`

---

# 1. Purpose of this file

This file exists to keep the project coherent as the documentation system, codebase, and AI-agent activity grow.

Without a canonical glossary and controlled decision system, projects like this often suffer from the following failures:
- the same concept gets multiple names,
- different files use the same word to mean different things,
- AI agents create duplicate entities because terminology is vague,
- features drift because decisions are made informally and then forgotten,
- architecture changes happen silently without shared understanding,
- code and documentation diverge because nobody knows which naming pattern is official,
- contributors argue repeatedly about decisions that were already made.

This file prevents those failures by defining:
- canonical product and technical terms,
- naming rules,
- ambiguous and forbidden terminology,
- decision-record format,
- change types and approval levels,
- deprecation and breaking-change rules,
- how truth changes must be documented.

---

# 2. Core governance principles

## 2.1 One concept, one canonical term
A concept should have one preferred name across product, design, engineering, analytics, docs, and AI-agent prompts wherever practical.

## 2.2 Clarity over clever naming
Names should optimize for clarity, stability, and maintainability, not cleverness or branding flair.

## 2.3 Decisions must be recoverable
If a decision matters later, it must be written down in a way that a new human or AI agent can understand without relying on memory.

## 2.4 Contracts beat casual language
If casual wording conflicts with a canonical contract term, the contract term wins.

## 2.5 Changes must be deliberate
The project must not drift through a chain of small undocumented “temporary” changes.

## 2.6 Naming is architecture
Poor naming causes duplicate models, bad APIs, confused analytics, scattered UI copy, and refactor debt. Therefore naming is a first-class design responsibility.

---

# 3. Canonical terminology rules

## 3.1 General rule
Every major entity, feature, state, and system concept should have:
- one canonical name,
- an optional short description,
- any allowed aliases for searchability only,
- any forbidden synonyms that must not be used in specs or code if they create confusion.

## 3.2 Scope of this glossary
This glossary covers:
- product terms,
- ritual/content terms,
- map and location terms,
- group coordination terms,
- personal tools terms,
- monetization terms,
- architecture and codebase terms,
- quality and release terms.

## 3.3 Glossary maintenance rule
When a new important concept is introduced, this file must be updated if the concept will appear in more than one module, file, API, analytics event family, or UI surface.

---

# 4. Product glossary

## 4.1 Pilgrims Mobile App
**Canonical meaning:** The mobile pilgrimage companion product defined by this documentation system.
**Allowed aliases:** the app, pilgrimage companion app
**Forbidden substitutes when precision matters:** travel app, navigation app, Islamic app

## 4.2 Pilgrim
**Canonical meaning:** The end user undertaking pilgrimage and using the app.
**Notes:** Prefer “pilgrim” over “customer” in product and UX contexts unless discussing billing.

## 4.3 Companion app
**Canonical meaning:** A supportive product that helps during the journey without claiming to replace official service systems.

## 4.4 Umrah-first
**Canonical meaning:** The strategic scope rule that the app’s initial product and default flows prioritize Umrah and must not silently reintroduce broader pilgrimage complexity.
**Forbidden distortion:** using “Umrah-first” to imply “Hajj already fully supported in the same flow.”

## 4.5 Simple Mode
**Canonical meaning:** A simplified operating mode intended to reduce cognitive load and make high-priority actions easier to access.
**Allowed aliases:** simplified mode
**Forbidden ambiguous substitutes:** beginner mode, elderly mode, lite mode, easy mode, unless explicitly defined as separate future concepts.

## 4.6 Home
**Canonical meaning:** The app’s primary dashboard or landing surface after onboarding/login state resolution.
**Forbidden confusion:** Do not use interchangeably with tab root, launch screen, or onboarding entry screen.

## 4.7 Official-service handoff
**Canonical meaning:** A deliberate product pattern where the app routes the user toward an official or authority-managed service instead of trying to own the workflow.
**Examples:** permits, ministry-controlled flows, official registrations.

---

# 5. Ritual and content glossary

## 5.1 Ritual guidance
**Canonical meaning:** Structured product guidance that helps the user understand what step or action is relevant in the pilgrimage flow.

## 5.2 RIC
**Canonical meaning:** The product’s structured mistake-resolution or uncertainty-resolution capability.
**Current usage rule:** Until a later product decision changes it, “RIC” remains a valid internal product term, but every user-facing context must also ensure the meaning is understandable.
**Documentation rule:** If RIC is used in a file, define it at first mention.

## 5.3 Resolver
**Canonical meaning:** The user-facing or system-facing logic that helps resolve uncertainty, interruption, or mistakes in ritual flow.
**Relationship to RIC:** Resolver may be used as a descriptive label, but must not create a second disconnected concept. If both terms appear, the file must explain that they refer to the same feature family or tightly related concepts.

## 5.4 Remedy
**Canonical meaning:** The action or resolution guidance offered in response to a specific ritual mistake or issue.

## 5.5 Religious content
**Canonical meaning:** Structured content whose correctness and presentation are governed by the content and scholar-review workflow.

## 5.6 Scholar review
**Canonical meaning:** The formal review/approval process for sensitive religious content before publication or correction.

## 5.7 Draft / Review / Approved / Published
**Canonical meaning:** The standard content lifecycle states.
**Rule:** Do not invent alternate lifecycle states without updating the relevant content-governance files.

---

# 6. Map and wayfinding glossary

## 6.1 Map subsystem
**Canonical meaning:** The combined system for location understanding, routing, scene rendering, map data, and fallback guidance.
**Important rule:** Do not reduce this term to a visual map widget alone.

## 6.2 Wayfinding
**Canonical meaning:** Helping the user understand how to get from a current context to a desired destination through route logic, instructions, and visual/spatial guidance.

## 6.3 Positioning
**Canonical meaning:** Determining or estimating the user’s location or spatial context.
**Important rule:** Positioning is not the same thing as routing or map rendering.

## 6.4 Routing graph
**Canonical meaning:** The navigable structure of nodes, edges, levels, and constraints used for route calculation.

## 6.5 3D wayfinding
**Canonical meaning:** A user experience where wayfinding is supported by a 3D spatial representation, not merely a decorative tilted map.

## 6.6 Save My Gate
**Canonical meaning:** The user-facing feature that allows the user to save a gate or gate-like anchor for later recall and orientation.
**Rule:** This should remain a distinct user-facing concept even if implemented through underlying generic location objects.

## 6.7 Landmark
**Canonical meaning:** A meaningful visual or navigational reference point used in guidance.

## 6.8 POI
**Canonical meaning:** Point of interest. Use carefully in technical or data contexts.
**User-facing guidance:** Prefer user-friendly category names where appropriate instead of the term “POI.”

## 6.9 Indoor positioning
**Canonical meaning:** Positioning behavior specific to indoor or structurally constrained environments.

## 6.10 Fallback guidance
**Canonical meaning:** Guidance that remains useful when precise location, 3D rendering, or rich connectivity is unavailable.

---

# 7. Group coordination glossary

## 7.1 Group
**Canonical meaning:** A user-associated coordination unit for family, travel companions, or organized parties.

## 7.2 Group leader
**Canonical meaning:** A privileged group role with additional coordination permissions.
**Rule:** Do not invent new role names casually.

## 7.3 Member
**Canonical meaning:** A standard group participant.

## 7.4 Check-in
**Canonical meaning:** A user action or system event representing a status/location/coordination update within the group context.

## 7.5 Regroup pin
**Canonical meaning:** A coordination anchor used to help members regroup.
**Rule:** This must remain distinguishable from generic saved pins or generic check-ins in product language, even if implementation shares infrastructure.

## 7.6 Live board
**Canonical meaning:** The shared coordination surface showing current group-relevant updates or statuses.

## 7.7 Freshness
**Canonical meaning:** How recent or trustworthy a live/shared status item is.

---

# 8. Personal tools glossary

## 8.1 Planner
**Canonical meaning:** The feature area for lightweight pilgrimage planning and task organization.

## 8.2 Reminder
**Canonical meaning:** A time-based or context-based prompt for a relevant action.

## 8.3 Wallet
**Canonical meaning:** A storage surface for important pilgrimage-related items or references as defined by product scope.
**Forbidden confusion:** Do not let “wallet” drift into a payment wallet or crypto wallet concept.

## 8.4 Note
**Canonical meaning:** User-authored text or structured content saved for later reference.

## 8.5 Bookmark
**Canonical meaning:** A saved reference to app content for quick return.

---

# 9. Monetization and account glossary

## 9.1 Free
**Canonical meaning:** The baseline user entitlement state with ethically essential value available.

## 9.2 Premium / Supporter
**Canonical meaning:** Paid entitlement tiers that unlock convenience, enrichment, or enhanced experience without violating ethical boundaries.
**Rule:** Pick one canonical public naming direction when branding is finalized. Internal docs may use “premium/supporter” temporarily only if meaning remains clear.

## 9.3 Entitlement
**Canonical meaning:** A machine-checkable permission or access state used to gate features or content.

## 9.4 Restore purchase
**Canonical meaning:** The store-supported process for recovering valid paid access on a device/account.

## 9.5 Settings
**Canonical meaning:** The grouped surface for user preferences, controls, and app-level configuration.

## 9.6 Account
**Canonical meaning:** The user identity state and associated profile/authentication context.

---

# 10. Architecture and codebase glossary

## 10.1 Contract file
**Canonical meaning:** A normative file that defines truth AI agents must not guess around.

## 10.2 Feature-family file
**Canonical meaning:** A file that groups closely related product capabilities into one coordinated spec.

## 10.3 Module
**Canonical meaning:** A bounded area of code with a focused responsibility and explicit dependencies.

## 10.4 Design tokens
**Canonical meaning:** Centralized, reusable visual values such as semantic colors, typography scales, spacing, radius, motion, and effects.

## 10.5 Theme
**Canonical meaning:** The structured visual configuration that applies tokens and semantic styling rules throughout the app.

## 10.6 Shared component
**Canonical meaning:** A reusable UI building block used across features through the design-system boundary.

## 10.7 Platform bridge
**Canonical meaning:** The integration layer between Flutter and platform-native capabilities.

## 10.8 Source of truth
**Canonical meaning:** The canonical place where a rule or structure is defined.
**Rule:** Do not duplicate source of truth casually.

## 10.9 Invariant
**Canonical meaning:** A condition that must remain true across the system.

## 10.10 Additive change
**Canonical meaning:** A change that extends a system without immediately breaking existing consumers.

## 10.11 Breaking change
**Canonical meaning:** A change that invalidates previous assumptions, contracts, data, or integrations.

---

# 11. Quality and release glossary

## 11.1 Definition of done
**Canonical meaning:** The minimum bar that must be met before a task is considered complete.

## 11.2 Release gate
**Canonical meaning:** A mandatory condition or evidence checkpoint that must be satisfied before release.

## 11.3 Real-world verification
**Canonical meaning:** Validation beyond automated tests, including device behavior, offline checks, and practical user-flow confirmation.

## 11.4 Incident
**Canonical meaning:** An operational problem affecting users, release safety, or critical product correctness.

## 11.5 Rollback
**Canonical meaning:** A deliberate procedure to return to a previous safer state after a bad change or release.

---

# 12. Ambiguous or forbidden terminology

The following terms should be avoided or tightly controlled.

## 12.1 “Tracking”
Avoid this term in user-facing language unless absolutely necessary, because it can imply surveillance.
Prefer more precise terms such as:
- sharing location intentionally,
- check-in,
- regroup,
- saved anchor,
- live status.

## 12.2 “AI guide” for religious correctness
Do not casually market religious correctness features as autonomous AI wisdom. The governance model must remain explicit.

## 12.3 “Indoor GPS”
Avoid using this as a precise technical term because it is often inaccurate or misleading.
Use “indoor positioning” where appropriate.

## 12.4 “Lite”
Do not use “lite” as a substitute for Simple Mode unless a separate product concept is formally approved.

## 12.5 “Paywall” in internal specs
Allowed in internal product and monetization discussion, but when describing user-facing behavior prefer “entitlement boundary” or “upgrade boundary” where precision is needed.

## 12.6 “Just a 3D map”
Forbidden framing in documentation because it obscures the map subsystem’s functional complexity.

---

# 13. Naming conventions across the project

## 13.1 General naming goals
Names should be:
- clear,
- stable,
- scoped,
- searchable,
- consistent across docs and code where practical.

## 13.2 File naming convention
Documentation files should use:
- numeric ordering prefix,
- uppercase kebab-style words separated by hyphens,
- descriptive scope,
- no unnecessary abbreviations unless already canonical.

Example:
- `16-MAP-ARCHITECTURE-POSITIONING-ROUTING-3D-AND-OFFLINE-WAYFINDING.md`

## 13.3 Flutter/Dart naming convention guidance
Detailed code conventions may be refined in the Flutter architecture file, but the following rules apply at a high level:
- packages/modules should use stable descriptive names,
- widgets should be named by purpose, not visual coincidence,
- repositories/services should reflect domain meaning,
- avoid abbreviations unless widely understood and already canonical,
- public API names should align with canonical glossary terms where possible.

## 13.4 API naming convention guidance
- Resource naming should be explicit and domain-consistent.
- Event names should reflect user-meaningful actions or system events, not implementation trivia.
- Avoid multiple names for the same entity across endpoints.

## 13.5 Analytics naming convention guidance
- Event families should be predictable.
- Event names should use stable domain language.
- Avoid renaming analytics casually because historical analysis continuity matters.

---

# 14. Decision-record system

Important decisions must be captured in this file or a linked structured decision log section.

## 14.1 What counts as a decision worth recording
Record a decision when it materially affects:
- product scope,
- monetization boundary,
- architecture direction,
- map/provider strategy,
- content-governance policy,
- data model or invariant behavior,
- platform adaptation,
- feature boundary,
- release strategy,
- privacy/safety posture,
- AI-agent workflow rules.

## 14.2 Decision record template
Each decision entry should include:
- **Decision ID**
- **Date**
- **Status** (proposed / accepted / superseded / deprecated)
- **Owner**
- **Area** (product / design / engineering / content / operations / monetization)
- **Context**
- **Decision**
- **Alternatives considered**
- **Why this decision was chosen**
- **Consequences**
- **Files impacted**
- **Supersedes / superseded by** if relevant

## 14.3 Decision quality rule
A decision record must be understandable later by someone who was not present when the decision was made.

## 14.4 Sample current decisions already established
These should be entered as accepted decisions in the maintained decision log section.

### D-001 — Compact 30-file spec architecture
- **Status:** accepted
- **Area:** documentation governance
- **Decision:** Use a compact but controlled 30-file spec system rather than either over-fragmented docs or an over-compressed minimal doc set.

### D-002 — Umrah-first product scope
- **Status:** accepted
- **Area:** product scope
- **Decision:** Default product and early release scope are Umrah-first; Hajj complexity must not be silently reintroduced.

### D-003 — Centralized Flutter theme and token architecture
- **Status:** accepted
- **Area:** engineering/design system
- **Decision:** Repeated style values must be centralized rather than hardcoded across feature widgets.

### D-004 — Controlled iOS Liquid Glass adaptation
- **Status:** accepted
- **Area:** design/platform
- **Decision:** Use controlled iOS-specific glass/material adaptation where appropriate without compromising readability.

### D-005 — Map subsystem treated as a full system
- **Status:** accepted
- **Area:** maps/architecture
- **Decision:** Treat pilgrimage mapping as positioning + routing + 3D rendering + offline fallback, not just a visual map feature.

### D-006 — Simple Mode as strategic product capability
- **Status:** accepted
- **Area:** product/UX
- **Decision:** Simple Mode is a first-class product behavior, not an optional extra.

### D-007 — Official-service handoff boundary
- **Status:** accepted
- **Area:** product/operations
- **Decision:** Use official-service handoffs where authority-managed workflows are more appropriate than in-app ownership.

### D-008 — Real-world verification separate from automated tests
- **Status:** accepted
- **Area:** quality/release
- **Decision:** Passing automated tests alone is insufficient proof of release readiness.

---

# 15. Change-control framework

This section defines how project truth may change.

## 15.1 Change categories
Changes should be classified as one of the following.

### Category A — Editorial clarification
Examples:
- wording cleanup,
- typo fixes,
- non-semantic structure improvement.

**Approval level:** low
**Requirements:** must not change meaning.

### Category B — Non-breaking refinement
Examples:
- adding clarifying detail,
- strengthening a spec without altering core scope,
- additive examples,
- better update instructions.

**Approval level:** moderate
**Requirements:** must remain consistent with existing product and contract truth.

### Category C — Contract-affecting change
Examples:
- API shape changes,
- schema changes,
- entitlement changes,
- map behavior changes,
- feature state-machine changes.

**Approval level:** high
**Requirements:** linked doc updates and validation planning required.

### Category D — Strategic scope or ethics change
Examples:
- monetization boundary changes,
- product-scope changes,
- Hajj/Umrah scope shifts,
- privacy posture changes,
- official-service ownership changes.

**Approval level:** highest
**Requirements:** explicit decision record required.

## 15.2 Change proposal minimum contents
Any meaningful proposed change should identify:
- what is changing,
- why it is changing,
- which files are impacted,
- whether it is additive or breaking,
- risk level,
- what validation will be needed.

## 15.3 No silent truth changes
No contributor or AI agent may change product or contract truth only in code and leave docs behind.

---

# 16. Breaking-change rules

## 16.1 General rule
Breaking changes must be treated as explicit project events, not casual implementation details.

## 16.2 Breaking-change examples
- removing or renaming data fields consumers rely on,
- changing entitlement behavior,
- changing route/state semantics,
- renaming canonical analytics events without migration planning,
- changing map data assumptions,
- changing content lifecycle states.

## 16.3 Requirements for a breaking change
A breaking change requires:
- documented decision or approval,
- impacted file list,
- migration strategy if relevant,
- rollback strategy if relevant,
- explicit test and release evidence plan.

---

# 17. Deprecation rules

## 17.1 Deprecate before removing when practical
If a concept, field, event, endpoint, or UI pattern is being replaced, prefer a documented deprecation period when feasible.

## 17.2 Deprecation record must include
- what is deprecated,
- replacement if any,
- reason,
- timeline or trigger for removal,
- impacted files and consumers.

## 17.3 Avoid zombie terminology
Once a term is deprecated, new work must not keep reintroducing it.

---

# 18. When a new term must be added to this file

Add a new term here when any of the following is true:
- it appears in more than one spec file,
- it appears in both product and engineering contexts,
- it could plausibly be misunderstood by AI agents,
- it is part of an API, schema, analytics family, or reusable UX pattern,
- it replaces an older term and needs controlled adoption.

---

# 19. How AI agents must use this file

## 19.1 Before implementation
Agents must check whether the task introduces a new concept or renames an existing one.

## 19.2 During implementation
Agents must align variable names, API names, docs, and UI labels with canonical terminology where appropriate.

## 19.3 During refactor
Agents must avoid opportunistic renaming unless the rename is itself planned and documented.

## 19.4 During debugging
Agents must use glossary terms to describe the problem clearly and avoid introducing ad-hoc labels.

## 19.5 During documentation updates
Agents must update this file when a new cross-cutting concept becomes important.

---

# 20. When this file must be updated

This file must be updated when:
- a new cross-cutting concept is introduced,
- a concept is renamed,
- a term proves confusing in implementation,
- a meaningful decision is made or superseded,
- a new change-control rule is established,
- a deprecation or breaking-change policy changes,
- a file naming or canonical naming rule changes.

If important project language evolves but this file is not updated, the documentation system will eventually fragment.

---

# 21. Summary

This file is the language and governance stabilizer for the project.

It defines:
- the canonical terminology,
- naming expectations,
- ambiguous or forbidden phrasing,
- how important decisions are recorded,
- how changes are classified and approved,
- how breaking changes and deprecations are managed,
- how AI agents must use shared language consistently.

Its purpose is to keep the product, codebase, and documentation system coherent as complexity grows and many humans or AI agents contribute over time.

