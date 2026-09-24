# 18 — FEATURE: RITUALS, RIC, AND RELIGIOUS CONTENT

## Document status
- **Type:** Normative feature-family specification
- **Priority:** Highest
- **Audience:** Founder, product lead, content lead, scholar-board contributors, Flutter engineers, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical feature contract for ritual guidance, ritual-session tracking, RIC (Ritual Integrity Checker) / resolver behavior, religious content structure, scholar-review dependency, UX surfaces, offline guarantees, monetization boundaries, analytics hooks, and release-readiness requirements.
- **Authority level:** This file is the canonical source of truth for the Rituals feature family. If implementation, UI, or tests diverge from this file, this file wins unless a higher-level normative contract or approved decision record explicitly changes it.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`, `09-PLATFORM-ADAPTATION-IOS-ANDROID-AND-NATIVE-BRIDGES.md`, `10-PERSONAS-IA-USER-JOURNEYS-AND-TASK-FLOWS.md`, `11-SCREENS-STATES-NAVIGATION-AND-UI-BLUEPRINTS.md`, `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`, `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`
- **Related files:** `14`, `17`, `21`, `23`, `24`, `26`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This file exists because ritual guidance and mistake-resolution are among the most sensitive and trust-critical parts of the product.

If this feature family is underspecified, the project is exposed to especially dangerous failure modes:
- AI agents hardcoding ritual logic that should live in governed content,
- UI flows sounding confident when the system lacks sufficient context,
- season scope drifting and Hajj complexity leaking into Umrah-first flows,
- monetization surfaces interrupting sacred or correctness-critical moments,
- translations simplifying or distorting governed religious meaning,
- inconsistent remedies or citations across screens,
- offline behavior regressing in the one area users most expect to work without the internet,
- test suites passing while real ritual flow behavior becomes confusing or unsafe.

This file prevents those failures by defining:
- what the Rituals feature family is responsible for,
- which ritual scope is supported,
- how ritual sessions and steps behave,
- how RIC and resolver logic behave,
- how religious content is modeled and governed,
- which UI surfaces must exist,
- what remains offline-capable,
- what is never paywalled,
- what must be tested and evidenced before release.

---

# 2. Feature purpose and user value

## 2.1 Feature family purpose
The Rituals feature family exists to help pilgrims:
- understand what they should do next,
- complete ritual steps with more confidence,
- recover from uncertainty or mistakes,
- keep practical progress state locally,
- access governed religious guidance in a calm and readable form,
- continue using the app even when connectivity is poor or absent.

## 2.2 Main user value statement
A pilgrim should be able to open the Rituals experience and quickly get help with one of these questions:
- What is my next step?
- What does this step mean in practical terms?
- I am unsure whether I completed something correctly. What now?
- I missed something or was interrupted. What is the remedy?
- Can I continue even though I am offline?

## 2.3 Feature-level promise
This feature family must feel:
- calm,
- respectful,
- trustworthy,
- offline-capable,
- structured rather than improvisational,
- focused on action and recovery instead of dense theory.

---

# 3. Scope and boundaries

## 3.1 In scope
This feature family includes:
- ritual-session start, resume, pause, and completion behavior,
- ritual step display and progression,
- ritual counters such as tawaf or sa’i counts where supported,
- madhhab-aware rule interpretation where content defines it,
- RIC / resolver behavior,
- remedy mapping and explanation,
- citation-aware governed religious content rendering,
- ritual bookmarks or saved guidance entry points where they originate in ritual flow,
- audio hooks for ritual guidance where content and entitlement allow,
- planner and wallet integration points triggered by ritual states or remedies,
- offline-capable ritual and RIC runtime.

## 3.2 Out of scope
This feature family does **not** include:
- official permit workflows,
- government or ministry process ownership,
- unreviewed AI-generated religious rulings,
- generalized theological comparison tooling,
- cloud sync for ritual session data by default,
- medical advice,
- background navigation or background tracking,
- turning ritual guidance into a chat-first conversational system without documented approval.

## 3.3 Boundary with file `26`
This file defines the feature-facing contract for religious content behavior.

Deeper governance mechanics such as:
- content publishing workflow,
- draft/review/approved/published operations,
- scholar approval roles,
- provenance storage,
- emergency correction process,
- rollback of published content,

belong to `26-CONTENT-MODEL-SCHOLAR-REVIEW-AND-PUBLISHING-WORKFLOW.md`.

---

# 4. Product rules that govern this feature family

## 4.1 Umrah-first rule
The product is Umrah-first by default.

Therefore:
- off-season ritual entry must prioritize Umrah,
- Hajj-only paths or windows must remain hidden unless season and scope explicitly permit them,
- Hajj-specific planning overlays must not leak into Umrah flows,
- default content, copy, and home entry points must remain Umrah-first outside Hajj season.

## 4.2 No paywall on correctness rule
Core ritual guidance, step clarity, and RIC mistake-resolution support must remain ethically available without a supporter paywall.

## 4.3 Offline-first ritual rule
Core ritual guidance and RIC must remain usable without network connectivity.

## 4.4 Calm-under-stress rule
This feature family must optimize for users who are tired, anxious, elderly, first-time, or uncertain.

## 4.5 Governed-content rule
Religious meaning and remedies must come from governed content, not ad hoc developer or AI-agent invention.

---

# 5. Canonical terminology for this feature family

## 5.1 Ritual guidance
Structured product guidance that helps the user understand what step or action is relevant in the pilgrimage flow.

## 5.2 RIC
The product’s structured mistake-resolution or uncertainty-resolution capability.

## 5.3 Resolver
A descriptive label for the same tightly related feature family that helps the user reason through “what if I…” uncertainty. It must not become a separate disconnected product concept.

## 5.4 Remedy
The recommended action offered in response to a ritual mistake, omission, or relevant issue.

## 5.5 Religious content
Structured content whose correctness and presentation are governed by content and scholar-review workflow.

## 5.6 Scholar review
Formal review/approval process for sensitive religious content before publication or correction.

## 5.7 Pillar / wajib / sunnah
These are content-governed classification terms. They may appear in data/content models and advanced explanations, but user-facing presentation must remain understandable and respectful.

---

# 6. Supported ritual scope

## 6.1 Initial ritual scope
The initial supported scope must prioritize:
- Umrah guidance,
- Umrah mistake-resolution support,
- off-season Umrah-first default behavior.

## 6.2 Hajj scope posture
The architecture may support Hajj-mode ritual structures, but they must be season-gated and product-gated.

## 6.3 Scope layering
### Baseline required scope
- Start Umrah
- Resume active Umrah session
- Complete step flow offline
- Use RIC offline
- Receive remedy guidance

### Conditional scope
- Hajj paths such as Tamattu, Qiran, and Ifrad
- Hajj-only window overlays or planning hooks
- Hajj-specific remedies and content packs

## 6.4 Forbidden scope drift
The feature must not silently introduce broader pilgrimage-path complexity into the default Umrah experience.

---

# 7. Feature architecture summary

## 7.1 Core sub-capabilities
This feature family consists of five tightly related sub-capabilities:
1. ritual content runtime
2. ritual-session engine
3. step progression and counters
4. RIC / resolver evaluation engine
5. governed religious content presentation

## 7.2 Architectural rule
These sub-capabilities must remain conceptually separate even when they appear in one user flow.

## 7.3 Why separation matters
Without this separation, contributors and AI agents tend to:
- bury rule logic inside widgets,
- mix content definitions with UI-specific copy,
- make the session engine depend on presentation details,
- confuse persisted session state with hypothetical resolver results,
- patch behavior in code instead of fixing source content.

---

# 8. Ritual step model

## 8.1 Step model purpose
A ritual step is the atomic unit of guided action used by ritual-session UI and the session engine.

## 8.2 Canonical step object responsibilities
A step definition must be able to express:
- stable step identity,
- ritual path membership,
- human-readable title and hint references,
- step classification,
- prerequisites/dependencies,
- UI behavior such as counters or emphasis,
- optional audio hooks,
- optional caution or note references,
- optional citation references.

## 8.3 Minimum step definition fields
Recommended minimum fields:
- `id`
- `mode`
- `path_id`
- `sequence_index`
- `classification`
- `title_key`
- `short_hint_key`
- `deps[]`
- `counter_config?`
- `advanced_detail_refs[]?`
- `citation_refs[]?`
- `audio_refs[]?`
- `visibility_rules?`

## 8.4 Classification values
Canonical step classifications should remain content-governed.

Recommended baseline classifications:
- `PILLAR`
- `WAJIB`
- `SUNNAH`
- `INFO`

If these need expansion later, update this file and file `26` together.

## 8.5 Dependency rule
Every dependency reference in a ritual path must point to a valid step within that path or a valid shared prerequisite object.

## 8.6 Referential-integrity rule
Broken or unknown step references are a content error and must fail validation before publication.

---

# 9. Ritual path model

## 9.1 Path model purpose
A ritual path represents a coherent supported route through a pilgrimage flow.

## 9.2 Initial path strategy
Recommended baseline paths:
- `UMRAH`
- `TAMATTU`
- `QIRAN`
- `IFRAD`

In the initial user experience, `UMRAH` is the primary active path.

## 9.3 Path-level fields
Recommended fields:
- `id`
- `mode`
- `display_name_key`
- `description_key?`
- `step_ids[]`
- `season_visibility_rules`
- `madhhab_support`
- `content_version`

## 9.4 Season visibility rule
When `season=umrah`, Hajj-specific path discovery must be hidden from default user entry points.

---

# 10. Religious content object structure

## 10.1 Purpose
The religious content model exists so that religious meaning, structured guidance, remedies, and citations remain governed and versionable instead of being improvised in application code.

## 10.2 Canonical content object families
This feature family depends on at least these governed content object families:
- ritual definitions
- path definitions
- step definitions
- rule sets by madhhab and mode
- remedy definitions
- citation references
- localized string bundles
- optional audio reference bundles
- optional season-specific window or advisory data for Hajj scope

## 10.3 Minimum governed content bundles
Recommended baseline bundle families:
- `rituals_umrah.*`
- `rituals_hajj.*`
- `madhhab_rules.*`
- `remedy_rules_umrah.*`
- `remedy_rules_hajj.*`
- `strings/rituals.*`
- `citations/rituals.*`
- optional `audio_manifest/rituals.*`

## 10.4 Content structure rule
The app must treat ritual logic as content-driven:
- steps are defined in content,
- dependencies are defined in content,
- rule mappings are defined in content,
- remedies are defined in content,
- citation associations are defined in content,
- UI copy references must point to localization resources rather than hardcoded widget strings.

## 10.5 Content-versioning rule
Published ritual content must carry explicit versioning so session engine behavior, content freshness, and test fixtures can remain aligned.

## 10.6 Content-runtime rule
The app should load the latest valid local ritual content bundle available and use it offline.

---

# 11. Scholar-review dependency

## 11.1 Scholar-review requirement
Religious content that influences:
- step correctness,
- remedy guidance,
- pillar/wajib interpretation,
- user-facing ritual warnings,
- citations or religious references,

must be governed by the scholar-review workflow defined in file `26`.

## 11.2 Developer and AI-agent rule
Developers and AI agents must not invent new ritual rules or new remedy meanings directly in code.

## 11.3 Emergency correction rule
If a high-severity ritual-content issue is identified, the correction path must follow the emergency correction workflow in file `26`, not an undocumented hotfix process.

## 11.4 Content provenance rule
Every governed ritual rule or remedy should be traceable to a reviewed content source even if the UI renders a simplified explanation.

---

# 12. Madhhab and rule-model behavior

## 12.1 Purpose
This feature family must support content-governed differences in ritual evaluation or remedy behavior without forcing the user through dense comparative theology.

## 12.2 Madhhab support rule
If madhhab-specific rule differences matter for evaluation or remedies, those differences must be expressed in rule content rather than widget code.

## 12.3 User-experience rule
The user experience should surface the result and recommended next action clearly.

It should not force the user into comparative jurisprudence unless they explicitly want more detail.

## 12.4 Unsupported-context rule
If the app lacks sufficient context to evaluate a scenario reliably, it must not overclaim certainty.

## 12.5 Persisted user-context rule
If the user selected a madhhab or ritual path for a session, the session should persist and reuse that context until the session ends or the user explicitly changes it.

---

# 13. Ritual session model

## 13.1 Canonical persistence rule
Ritual sessions are canonical device-local data.

## 13.2 Local session fields
This feature family must align with file `13`.

Minimum persisted fields for a ritual session:
- `id`
- `mode`
- `path`
- `madhhab`
- `current_step_id`
- `started_at`
- `updated_at`
- `completed_at?`
- `status`

## 13.3 Session-local only rule
Ritual progress remains local-first by default and is not synced to the server unless a future approved feature changes the contract.

## 13.4 Resume rule
Pause/resume must survive app kill and device relaunch.

## 13.5 Abandonment rule
A ritual session may enter an `ABANDONED` or equivalent non-active state only if the local model and feature behavior remain aligned with file `13`.

---

# 14. Step-state machine

## 14.1 Purpose
The step-state machine ensures progression, counters, and revisit behavior stay consistent.

## 14.2 Canonical step states
Recommended baseline step states:
- `LOCKED`
- `AVAILABLE`
- `IN_PROGRESS`
- `DONE`
- `REVISITABLE` (optional view-state when content and UX support revisiting)

## 14.3 Transition rule
Transitions must be driven by:
- path order,
- dependency satisfaction,
- user action,
- counter completion,
- explicit pause/resume behavior.

## 14.4 State safety rule
The UI must never imply that a step is completed unless the persisted session state supports that conclusion.

## 14.5 Validation rule
If content dependencies are invalid, the feature must fail safely rather than improvising a graph.

---

# 15. Counter behavior model

## 15.1 Purpose
Some steps require count-based guidance such as tawaf or sa’i progression.

## 15.2 Counter features
Counters should support:
- increment
- safe undo
- persisted progress after each meaningful change
- accessible feedback
- localized count rendering
- large-text usability

## 15.3 Haptic rule
Haptics may be used to reinforce counter increments or completion milestones, but they should rely on normal platform-level feedback rather than pretending the app controls precise custom haptic waveforms.

## 15.4 Counter integrity rule
Counter state must persist across app backgrounding and relaunch.

## 15.5 Undo rule
Undo must be available but safe.

Recommended behavior:
- one-step undo at a time
- explicit confirmation when the undo would materially change interpreted ritual progress

## 15.6 Accessibility rule
Counter interaction must remain usable with large text, screen readers, and reduced-motion preferences.

---

# 16. RIC / resolver behavior

## 16.1 Purpose
RIC exists to classify ritual status and recommend next actions or remedies using governed rule content.

## 16.2 Inputs to RIC
RIC may use:
- current ritual-session state,
- user answers in RIC entry flow,
- selected path and madhhab,
- content-governed rule sets,
- optional prior RIC findings where appropriate.

## 16.3 Outputs from RIC
RIC outputs must include:
- status classification,
- explanation summary,
- recommended next action,
- remedy list if relevant,
- citation or evidence references if relevant,
- confidence or context note when appropriate.

## 16.4 Canonical persisted statuses
This feature family must align with file `13` and use these persisted statuses unless updated there too:
- `VALID`
- `MISSING_PILLAR`
- `MISSING_WAJIB`
- `REMEDY_REQUIRED`

## 16.5 Non-persisted uncertainty handling
If the UI needs to represent incomplete context or unresolved uncertainty, it should do so as a presentation/result state rather than inventing a new persisted `ric_status` without updating file `13`.

## 16.6 Resolver behavior rule
Resolver behavior is part of the same feature family and must not drift into a separate conflicting engine.

### Resolver should support
- “What if I missed…” scenarios
- interruption/recovery questions
- hypothetical remedy preview
- calm next-step guidance

## 16.7 No-artificial-certainty rule
If the system lacks sufficient context, it must clearly say so instead of presenting a false final answer.

---

# 17. Mistake and remedy model

## 17.1 Purpose
The remedy model translates missing or invalid ritual conditions into user-actionable next steps.

## 17.2 Remedy object responsibilities
A remedy object should be able to express:
- remedy id
- trigger condition or case
- user-facing action summary
- explanatory detail
- category of remedy
- optional linked wallet evidence behavior
- optional citation refs
- mode/path applicability
- madhhab applicability where needed

## 17.3 Remedy categories
Recommended baseline categories:
- repeat step
- repeat segment
- dam/fidyah-related action
- clarification required
- no remedy required / reassurance case

## 17.4 Remedy display rule
The primary remedy display must focus on:
- what the user should do next,
- why it matters,
- where to get more detail if needed.

## 17.5 Wallet integration rule
If a remedy results in a practical record the user may want to keep, such as a receipt, the Rituals feature may hand off to Wallet via stable feature linkage.

## 17.6 Evidence-link rule
Wallet linkage must remain optional and supportive. It must not become required to complete ritual flow.

---

# 18. Citation and detail model

## 18.1 Purpose
Citations provide trustworthy grounding for governed religious guidance without overwhelming the user by default.

## 18.2 UI rule
Primary ritual and RIC screens should prioritize plain-language clarity.

Detailed citation material may live behind:
- expandable detail,
- “Why?” sections,
- advanced explanation panels,
- info drawers,
- dedicated detail screens if approved.

## 18.3 Copy rule
Citations must not force the primary user experience into legalistic or academic language.

## 18.4 Content-governance rule
Citation associations belong to governed content, not ad hoc UI-side hardcoding.

---

# 19. UI surfaces for this feature family

## 19.1 Canonical screen set
This feature family owns or strongly governs these screen contracts from file `11`:
- Rituals Root
- Start / Resume Ritual Screen
- Ritual Session Overview
- Ritual Step Detail
- RIC Entry
- RIC Result
- Ritual Bookmarks / Saved Guidance

## 19.2 Rituals Root
Purpose:
- show current ritual state,
- expose Start / Resume,
- provide clear entry to RIC,
- surface saved ritual references.

## 19.3 Start / Resume Ritual Screen
Purpose:
- start a new session or resume an existing local session,
- confirm or infer mode/path context safely,
- keep first-use friction low.

## 19.4 Ritual Session Overview
Purpose:
- show the user where they are,
- show what comes next,
- expose RIC and current status.

## 19.5 Ritual Step Detail
Purpose:
- explain one step clearly,
- provide action controls,
- support counters where relevant,
- support pause and completion state.

## 19.6 RIC Entry
Purpose:
- collect focused inputs for evaluation,
- avoid intimidating the user,
- use current session context where possible.

## 19.7 RIC Result
Purpose:
- present status,
- explain next action,
- show remedies and deeper detail access.

## 19.8 Ritual Bookmarks / Saved Guidance
Purpose:
- let the user return to important ritual content later.

---

# 20. Rituals Root UX contract

## 20.1 Required content blocks
- active-session card or start card
- progress summary if active session exists
- RIC quick entry
- saved guidance/bookmark entry
- optional audio surface if relevant and not distracting

## 20.2 Required states
- no session yet
- resumable session
- active session
- completed session summary
- offline local-content state
- content unavailable / corrupted fallback

## 20.3 Primary actions
- Start / Resume Ritual
- Open RIC
- Open current step

---

# 21. Ritual Step Detail UX contract

## 21.1 Required content blocks
- step title
- short practical explanation
- action emphasis
- counter surface if relevant
- pause / done actions
- optional advanced detail section
- optional audio control if relevant
- optional bookmark / add note action

## 21.2 Required states
- ready/content
- counter-active
- paused
- done/revisited
- offline fully available
- missing-content fallback

## 21.3 Readability rule
This screen must prioritize readability over decorative styling and must not use decorative-depth-heavy treatment on dense ritual content. Ritual guidance and RIC must remain calm, high-contrast, and low-decoration in both Light and Dark.

---

# 22. RIC Entry UX contract

## 22.1 Required content blocks
- short explanation of purpose
- focused questions or structured selectors
- current ritual context summary if available
- continue/evaluate action

## 22.2 Required states
- fresh start
- partial input
- missing context guidance
- evaluation in progress
- unsupported scenario fallback

## 22.3 Interaction rule
The flow must minimize cognitive load and avoid dumping too many branching questions at once.

---

# 23. RIC Result UX contract

## 23.1 Required content blocks
- status banner/card
- next action summary
- remedy list if relevant
- expandable explanation or citations
- optional wallet handoff for evidence capture
- return-to-ritual action

## 23.2 Required states
- `VALID`
- `MISSING_PILLAR`
- `MISSING_WAJIB`
- `REMEDY_REQUIRED`
- insufficient-context presentation state
- offline result

## 23.3 Presentation rule
The result must be calm and actionable. It must not sound judgmental or theatrically alarming.

---

# 24. Completion UX contract

## 24.1 Session-completion purpose
Completion should provide closure, reassurance, and optional supportive next actions.

## 24.2 Allowed completion elements
- subtle success haptic or completion feedback
- summary card
- share summary without sensitive data
- suggest related supportive actions such as notes, bookmarks, or post-journey pack cleanup

## 24.3 Forbidden completion behavior
- aggressive monetization surface
- misleading claim that completion implies every uncertainty is resolved if RIC has not been evaluated
- cluttered celebratory UI that disrupts calmness

---

# 25. Offline behavior

## 25.1 Offline tier
This feature family is Tier A fully offline-capable essential functionality.

## 25.2 Offline guarantees
The following must work meaningfully offline once the app has usable local content:
- ritual session start and resume
- ritual step reading
- counter progression
- RIC evaluation using local rule content
- remedy display
- saved ritual progress persistence

## 25.3 Offline content rule
The runtime must use last-valid local content if fresh network or content refresh is unavailable.

## 25.4 Missing-content fallback rule
If required ritual content is missing or invalid:
- prefer last known good content,
- surface a content-update or support message,
- do not pretend that missing content is present,
- degrade safely.

## 25.5 No-network rule
The absence of internet must not block the core ritual guidance or RIC flow.

---

# 26. Audio behavior and entitlement boundaries

## 26.1 Core correctness boundary
Text guidance and RIC must remain fully available without supporter entitlement.

## 26.2 Audio posture
Audio is a supportive enrichment layer, not a requirement for correctness.

## 26.3 Baseline audio rule
If streaming ritual audio is supported, it may be available when network permits. If not available, the feature must still remain fully usable through text.

## 26.4 Offline audio rule
Offline ritual audio requires:
- installed audio pack,
- entitlement permitting offline audio,
- platform/runtime support.

## 26.5 Entitlement key
Offline audio behavior should align with the `AUDIO_OFFLINE` entitlement boundary.

## 26.6 No-paywall-in-sacred-flow rule
Monetization or pack prompts must not interrupt ritual step completion or RIC evaluation.

## 26.7 Pace-control rule
If audio playback exists, pace controls may be offered as convenience, but not at the cost of clarity or accessibility.

---

# 27. Integration points with other feature families

## 27.1 Planner integration
Ritual state may create supportive planner suggestions.

Examples:
- hydration reminders
- shade reminders
- Hajj-only window-related suggestions when and only when Hajj scope is active

## 27.2 Wallet integration
Ritual remedies may link to wallet receipt capture for user records.

## 27.3 Notes/bookmarks integration
The user may bookmark ritual steps or add a note from ritual content surfaces.

## 27.4 Offline packs and audio integration
The feature may reference optional audio/content packs but must still function without them.

## 27.5 Home integration
Home may show current ritual status, resume entry, or recovery shortcut.

## 27.6 Map integration
The Rituals feature may suggest related orientation aids such as Save My Gate when contextually helpful, but it must not become dependent on map availability.

---

# 28. Local data and persistence alignment

## 28.1 Canonical local entities
This feature family must align with file `13` for:
- `ritual_sessions`
- `ric_findings`
- bookmark/note capture references where used

## 28.2 `ritual_sessions` rule
The feature must treat ritual sessions as canonical device-local progress state.

## 28.3 `ric_findings` rule
RIC findings are local operational records unless a future approved feature explicitly changes that contract.

## 28.4 Local reference rule
Cross-feature references should use stable ids or `source_kind` / `source_ref` patterns instead of brittle hard coupling.

---

# 29. API and backend boundaries

## 29.1 Tiny online surface rule
This feature family must not assume a large backend surface for core ritual logic.

## 29.2 Online uses allowed
Online behavior may be used for:
- flags/season refresh,
- content freshness checks if later approved,
- pack/manifest discovery for optional ritual audio/content packs,
- entitlement refresh when needed.

## 29.3 Forbidden backend dependency
The app must not require live API calls to evaluate a routine ritual session or RIC question.

## 29.4 Versioning rule
If any future API participates in ritual content distribution or content freshness metadata, that API must remain additive and must not undermine offline-first guarantees.

---

# 30. Copy, localization, RTL, and accessibility rules for this feature family

## 30.1 Tone rule
Ritual copy must be:
- respectful
- calm
- clear
- steady
- not overly casual
- not legalistic by default

## 30.2 User-facing terminology rule
Internal labels such as “RIC” may exist, but user-facing text must remain understandable without internal jargon.

## 30.3 Translation and transliteration rule
If ritual content surfaces Arabic, translated meaning, and transliteration, the UI must distinguish them clearly rather than mixing them casually.

## 30.4 Large-text rule
Ritual step and RIC screens must remain usable under significant text scaling.

## 30.5 RTL rule
Ritual flows must support RTL structurally, including step content, counters, navigation affordances, and mixed-direction content handling where needed.

## 30.6 Screen-reader rule
Key step titles, action buttons, counter changes, and RIC result changes must be exposed meaningfully to assistive technologies.

## 30.7 Haptic accessibility rule
Haptics may enhance interaction, but the experience must remain understandable even if haptics are unavailable or disabled.

---

# 31. State families and degraded states

## 31.1 Shared states
Important Rituals screens must support:
- loading
- content
- empty (where relevant)
- error
- offline
- stale-content notice if relevant
- unavailable/corrupted-content fallback

## 31.2 Ritual-specific degraded states
This feature family must explicitly handle:
- missing content bundle
- invalid step graph
- missing citation reference
- missing audio pack
- unsupported Hajj path while season is Umrah
- insufficient context for RIC certainty

## 31.3 Truthfulness rule
The feature must never pretend that:
- a missing step graph is valid,
- an unknown remedy is known,
- a stale or missing content bundle is current,
- an incomplete session has been fully evaluated.

---

# 32. Edge cases

## 32.1 App killed during session
The session must resume with preserved current step and counter state.

## 32.2 App killed during counter progression
Counter progress must survive and remain consistent.

## 32.3 User changes locale during active session
The content presentation should relocalize safely without corrupting underlying ritual-session state.

## 32.4 User changes madhhab mid-session
If allowed, the UX must explain implications clearly. If not allowed, the app must prevent silent rule drift.

## 32.5 Missing or corrupted content bundle
Use last good local content where possible; otherwise fail safely with support/update messaging.

## 32.6 Hajj content in Umrah season
Must remain hidden from default paths and must not leak through planner or ritual suggestions.

## 32.7 Offline audio absent
The user must continue using text guidance without interruption.

## 32.8 Insufficient context for resolver
Show uncertainty honestly and guide the user toward safer next steps or more detail.

## 32.9 Large-text layout pressure
Primary step and result actions must remain visible and tappable.

---

# 33. Error handling and guardrails

## 33.1 No monetization interruption rule
Never block ritual progress or RIC evaluation with upsells, supporter prompts, or pack gates.

## 33.2 Invalid content graph rule
If the step graph is invalid:
- do not improvise progression,
- disable unsafe evaluation paths where needed,
- surface safe fallback messaging,
- log observability evidence,
- treat the issue as release-blocking or content-blocking severity according to file `28`.

## 33.3 Missing-rule mapping rule
If a rule or remedy lookup fails, the UI must not fabricate a remedy.

## 33.4 Error copy rule
Errors must remain simple, respectful, and action-oriented.

## 33.5 Support-link rule
If the feature reaches a non-recoverable local content state, the app may point to About/support/update context, but must not trap the user in an ambiguous broken screen.

---

# 34. Analytics and observability hooks

## 34.1 Event goals
Analytics for this feature family should measure:
- session starts and completion,
- step progression quality,
- RIC usage and outcomes,
- offline success,
- degraded-state exposure,
- audio use when supported,
- remedy-to-wallet usage,
- drop-off points and confusion indicators.

## 34.2 Recommended analytics events
- `ritual_session_started`
- `ritual_session_resumed`
- `ritual_step_opened`
- `ritual_step_completed`
- `ritual_counter_changed`
- `ric_entry_opened`
- `ric_evaluated`
- `ric_result_viewed`
- `resolver_scenario_used`
- `ritual_audio_played`
- `ritual_audio_unavailable_shown`
- `ritual_remedy_wallet_handoff`
- `ritual_content_fallback_used`
- `ritual_invalid_content_guardrail_triggered`

## 34.3 PII-light rule
Do not log sensitive user note content, exported receipt contents, or raw governed content payloads beyond approved observability needs.

## 34.4 Observability rule
Content validation failures, graph failures, and repeated resolver uncertainty cases should surface in observability tooling because they indicate high-trust product risk.

---

# 35. Performance and implementation constraints

## 35.1 Ritual UI performance target
Rituals entry and main ritual screen presentation should feel near-instant on supported devices.

Recommended initial target:
- Rituals UI open to usable state within 500 ms on representative mid-tier devices when required local data already exists.

## 35.2 Counter responsiveness target
Counter interaction should feel immediate and not wait on heavy work.

## 35.3 Asset-weight rule
Ritual step content should avoid unnecessarily heavy media in the core path.

Recommended posture:
- prefer text, vector illustrations, and optional media rather than mandatory heavy assets.

## 35.4 Haptics implementation rule
Use platform-default haptic behavior through supported Flutter/platform APIs. Do not architect around precise custom haptic waveform control.

---

# 36. Security and privacy rules

## 36.1 Local-first privacy rule
Ritual session and RIC findings are local-first and should not be uploaded automatically.

## 36.2 No irrelevant permission rule
This feature family must not request irrelevant permissions such as microphone or background location.

## 36.3 Export rule
If ritual summaries or related records are exported, export must be explicit and user-initiated.

## 36.4 Sensitive-content logging rule
Do not log governed content payloads or user-specific recovery details recklessly.

---

# 37. Test cases

## 37.1 Unit tests
At minimum:
- ritual step graph validation
- step-state transitions
- counter increment and undo logic
- counter persistence
- RIC status derivation by supported rule sets
- remedy lookup logic
- season gating for Umrah/Hajj path exposure
- content fallback selection logic

## 37.2 Integration tests
At minimum:
- end-to-end ritual-session flow using local content fixtures
- RIC evaluation from realistic fixture inputs
- wallet handoff when remedy requires evidence capture
- planner suggestion hook on session start where relevant
- audio entitlement and installed-pack behavior

## 37.3 Device/E2E tests
At minimum:
- fresh install off-season -> Start Umrah -> complete flow offline -> RIC valid
- tawaf/sa’i counter to completion with haptics and undo
- session resume after app kill
- RIC missing-pillar case returns repeat guidance
- audio streaming available when online and offline audio available only with pack + entitlement
- large text and RTL ritual screens remain usable

## 37.4 Golden/state snapshot tests
Recommended:
- step counts and order per supported path
- resolver result snapshots for known scenarios
- localized ritual result screen variants

---

# 38. Release readiness checklist

A release candidate for this feature family is not ready unless all of the following are true:

- [ ] Ritual content bundles validate successfully against schema and referential-integrity rules.
- [ ] Supported Umrah flow works fully offline with local content.
- [ ] RIC statuses and remedy mappings match governed rule content.
- [ ] `VALID` cannot be produced when a required pillar is missing.
- [ ] Session pause/resume and counter persistence survive app kill.
- [ ] Ritual screens pass large-text, RTL, and screen-reader verification for critical flows.
- [ ] No paywall or supporter interruption appears in ritual-critical or RIC-critical flow.
- [ ] Audio entitlement boundaries behave correctly without making text guidance unusable.
- [ ] Wallet handoff for remedy evidence works and remains optional.
- [ ] Observability captures invalid-content guardrails and major degraded states.
- [ ] Real-device verification confirms the flow remains calm and readable under stress conditions.

---

# 39. Recommended implementation order

1. Implement content loader and content validation pipeline for ritual bundles.
2. Implement ritual session local model wiring.
3. Implement step graph construction and step-state engine.
4. Implement counters with persistence and safe undo.
5. Implement RIC evaluator using governed local rule content.
6. Implement RIC result UX and remedy presentation.
7. Implement wallet/planner integration hooks.
8. Implement optional audio integration and entitlement boundaries.
9. Complete localization, RTL, accessibility, and degraded-state verification.
10. Finalize analytics and release evidence.

---

# 40. Recommendations adopted into this feature contract

## 40.1 Recommendation — ritual logic stays in governed content
This file makes content-driven ritual logic a hard rule rather than a soft preference.

## 40.2 Recommendation — RIC and resolver remain one coherent feature family
The contract now prevents “RIC” and “resolver” from drifting into separate conflicting implementations.

## 40.3 Recommendation — no paywall in sacred correctness flows
Monetization boundaries are now explicitly enforced inside this feature-family spec.

## 40.4 Recommendation — offline correctness is first-class
The feature now treats offline ritual guidance and offline RIC as core product obligations.

## 40.5 Recommendation — governed content and scholar review are explicit dependencies
This prevents future contributors from treating ritual text like ordinary ungoverned app copy.

---

# 41. Anti-patterns forbidden by this feature family

The following are forbidden unless explicitly approved.

## 41.1 Hardcoding ritual logic in widgets or scattered business code
Forbidden.

## 41.2 Treating RIC as a chatty experimental assistant rather than a governed evaluator
Forbidden.

## 41.3 Introducing ritual statuses not aligned with file `13` without synchronized contract updates
Forbidden.

## 41.4 Showing supporter prompts inside ritual-critical or RIC-critical flow
Forbidden.

## 41.5 Presenting missing or uncertain ritual knowledge as certainty
Forbidden.

## 41.6 Letting Hajj-only content leak into off-season Umrah-first flows
Forbidden.

## 41.7 Replacing governed content with casual shortened copy that changes meaning
Forbidden.

## 41.8 Making audio or packs a requirement for core ritual usefulness
Forbidden.

## 41.9 Syncing ritual progress to the server by default without an approved contract change
Forbidden.

---

# 42. When this file must be updated

This file must be updated whenever any of the following changes:
- supported ritual scope
- step model or path model
- RIC status behavior
- remedy model
- governed content structure
- scholar-review dependency behavior
- ritual screen inventory or responsibilities
- offline guarantees
- audio entitlement boundaries
- wallet/planner integration hooks
- analytics events
- release-readiness criteria

If these change but this file is not updated, ritual correctness behavior, UI flow, testing, and content governance will drift quickly.

---

# 43. Summary

This file defines the canonical feature contract for Rituals, RIC, and governed religious content in Pilgrims Mobile App.

It establishes:
- the feature’s scope and value,
- the supported ritual-path posture,
- the ritual step and path models,
- the ritual-session and counter behavior,
- the RIC / resolver evaluation model,
- the remedy and citation structures,
- the scholar-review dependency,
- the required UI surfaces and degraded states,
- the offline guarantees,
- the entitlement boundaries,
- the testing and release-readiness requirements.

Its purpose is to ensure that this feature family remains:
- trustworthy,
- calm,
- governed,
- offline-capable,
- ethically monetized,
- and safe for long-term AI-assisted implementation without ritual-content drift.

