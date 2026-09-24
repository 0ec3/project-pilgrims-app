# 03 — PRODUCT CHARTER AND SCOPE

## Document status
- **Type:** Normative product source-of-truth
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, design lead, QA, AI coding agents, reviewer agents, content/religious governance contributors
- **Purpose:** Define what the product is, who it serves, what value it must deliver, what is in scope, what is out of scope, and what product rules must govern all future implementation decisions.
- **Authority level:** If a proposed feature, screen, data model, API, or workflow conflicts with this file, this file wins unless an approved decision record changes it.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `02-AI-AGENT-RULES-AND-WORKFLOW.md`
- **Related files:** `04`, `05`, `10`, `11`, `18`–`26`, `28`, `29`

---

# 1. Purpose of this file

This file defines the product truth for Pilgrims Mobile App.

Its job is to answer these questions clearly:
- What is this app for?
- Who is it for?
- What problem does it solve best?
- What values and ethical rules must it respect?
- What is included in the initial product scope?
- What is deliberately excluded?
- What decisions must future contributors and AI agents not silently override?

This file exists because product ambiguity creates expensive technical mistakes. In this project, ambiguity is especially dangerous because AI coding agents may otherwise:
- invent features that sound useful but are not aligned with the product,
- reintroduce excluded scope,
- blur free vs paid boundaries,
- make the app more complex under the excuse of completeness,
- treat visual polish as more important than readability and calmness,
- overbuild in areas where handoff to official services is the better product decision.

---

# 2. Product identity

## 2.1 Product name
**Working product name:** Pilgrims Mobile App

The exact public brand may evolve later, but all product thinking in this documentation system should treat the app as a pilgrimage companion for Muslim pilgrims.

## 2.2 Product category
The product is a **pilgrimage companion mobile app**.

It is not primarily:
- a travel super-app,
- a social network,
- a ride-hailing app,
- a government-service replacement,
- a booking marketplace,
- a general Muslim lifestyle app,
- a generic navigation platform.

## 2.3 Product mission
Help Muslim pilgrims complete their journey with more confidence, correctness, calm, and coordination.

## 2.4 Product promise
The app should help pilgrims:
- know what to do,
- recover when uncertain,
- stay oriented,
- stay connected to their group,
- access essential help quickly,
- function even when connectivity is weak or absent.

## 2.5 Product personality
The app should feel:
- calm,
- trustworthy,
- respectful,
- practical,
- lightweight,
- reliable,
- quietly supportive rather than noisy or overwhelming.

---

# 3. Primary user value

## 3.1 Main user value statement
A pilgrim should be able to open the app and quickly get help with one of the following:
- “What should I do now?”
- “I made a mistake. What now?”
- “Where am I and how do I get where I need to go?”
- “Where is my family or group?”
- “I need help communicating or handling an urgent situation.”
- “I need to remember or organize something important for the journey.”

## 3.2 Core jobs to be done
The product is designed around these core jobs:
1. **Ritual guidance:** help users understand ritual steps and order.
2. **Mistake recovery:** help users respond when unsure, interrupted, or mistaken.
3. **Orientation and wayfinding:** help users re-orient and navigate in difficult environments.
4. **Group coordination:** help users stay in contact and regroup.
5. **Pilgrimage assistance:** help users communicate, access emergency information, and respond under stress.
6. **Personal organization:** help users prepare, remember, and save important information.

## 3.3 What matters most
When tradeoffs happen, the product should prioritize:
1. correctness,
2. clarity,
3. readability,
4. calmness under stress,
5. offline usefulness,
6. maintainability,
7. polish.

If a beautiful effect harms readability or confidence, readability wins.
If a clever architecture makes future agent work harder, maintainability wins.
If a premium idea risks limiting safety-critical help, the ethical boundary wins.

---

# 4. Target users

## 4.1 Primary target users
The primary users are Muslim pilgrims, especially:
- first-time pilgrims,
- pilgrims traveling with family or guided groups,
- pilgrims who are easily stressed in crowded or unfamiliar environments,
- pilgrims who need dependable offline help,
- pilgrims who need practical guidance more than rich exploration.

## 4.2 High-priority user segments
The app must work especially well for:
- first-time Umrah pilgrims,
- elderly users,
- low-confidence smartphone users,
- users with weak connectivity,
- users who may be tired, anxious, sleep-deprived, or overwhelmed,
- group leaders coordinating multiple people,
- users switching between Arabic, English, and Indonesian or relying on simple phrase support.

## 4.3 Accessibility-sensitive users
The product must intentionally support:
- large text users,
- screen-reader users where applicable,
- low-vision users,
- users needing simpler information density,
- users who struggle with complex navigation or multi-step setup.

---

# 5. Product principles

These principles govern all product decisions.

## 5.1 Calm under pressure
The app must remain usable when the user is stressed, rushed, tired, confused, or in a noisy and crowded environment.

## 5.2 Correctness over cleverness
The product should not prioritize novelty or flashy interaction over getting the right answer, step, route, or fallback.

## 5.3 Offline-first for essential help
Essential user value must not depend on perfect connectivity.

## 5.4 Simplicity before breadth
A smaller set of dependable capabilities is better than a larger set of fragile or confusing ones.

## 5.5 Respectful religious handling
Religious guidance must be structured, reviewed, and handled carefully. The product must not behave casually around ritual correctness.

## 5.6 Safety and dignity
Emergency help, safety information, and urgent practical support should be easy to access and presented with dignity.

## 5.7 Group privacy and intentional sharing
The app should support coordination without defaulting to invasive tracking. Sharing should be intentional, minimal, and understandable.

## 5.8 Maintainability is a product requirement
A codebase that becomes chaotic will eventually degrade the user experience. Therefore code organization, design-system discipline, and contract clarity are product-level concerns, not merely engineering preferences.

---

# 6. Product scope anchor

## 6.1 Strategic scope statement
The product is initially scoped as an **Umrah-first pilgrimage companion** with focused support for ritual guidance, wayfinding, group coordination, assistance tools, offline packs, and light personal planning.

## 6.2 Why Umrah-first
This focus keeps the product practical, buildable, and coherent.

An Umrah-first approach:
- reduces feature sprawl,
- reduces ritual-path complexity,
- reduces UI complexity,
- makes onboarding simpler,
- creates a clearer path for high-quality offline support,
- improves implementation reliability for AI agents.

## 6.3 Hajj handling rule
Hajj-related complexity must not be treated as default scope unless explicitly included in a planned future release and documented across the relevant files.

No agent may silently add Hajj flow complexity back into default onboarding, ritual journeys, or user-path logic.

---

# 7. In-scope product pillars

These pillars define the intended product surface.

## 7.1 Pillar A — Ritual guidance and mistake recovery
The app should help the user:
- understand ritual sequence,
- see the current step,
- know what to do next,
- recover from common uncertainty or mistakes,
- save relevant reminders or remedy information when appropriate.

## 7.2 Pillar B — Maps, orientation, and wayfinding
The app should help the user:
- understand where they are,
- identify important destinations,
- save meaningful anchors such as gates,
- navigate visually and textually,
- benefit from 3D wayfinding where supported,
- still receive fallback guidance if 3D or precise positioning is not available.

## 7.3 Pillar C — Group coordination
The app should help users:
- join or manage a group,
- check in,
- regroup,
- view group coordination information,
- fall back to simpler/manual communication when live systems are unavailable.

## 7.4 Pillar D — Assistance and emergency support
The app should help users:
- communicate with basic phrase support,
- access emergency information,
- read safety alerts,
- use big-text or simplified support interfaces,
- reach assistance quickly in moments of stress.

## 7.5 Pillar E — Personal organization
The app should help users:
- plan key tasks,
- save reminders,
- store important journey items,
- write notes,
- bookmark meaningful content,
- use lightweight personal organization features without turning the app into a general productivity tool.

## 7.6 Pillar F — Offline support and content delivery
The app should support:
- downloadable content packs,
- offline maps or lightweight fallback data,
- offline ritual help,
- offline phrase/emergency tools,
- resilient sync and recovery behavior.

## 7.7 Pillar G — Ethical monetization and settings
The app may offer supporter or premium convenience features, but core correctness and safety value must remain ethically accessible.

---

# 8. Initial feature scope

This section defines the intended initial product feature scope at a high level.

## 8.1 Included feature areas
The following feature areas are in the compact spec system and are considered active product scope:
- Rituals guidance
- RIC / mistake-resolution support
- Maps and wayfinding
- Save My Gate
- Group Hub, check-ins, regroup, and coordination
- Planner, reminders, wallet, notes, and bookmarks
- Phrasebook
- Emergency tools
- Safety alerts
- Offline packs and audio/content distribution
- Account, subscriptions, entitlements, and settings
- Onboarding, Home, and Simple Mode
- Content governance and scholar review workflow

## 8.2 Included cross-cutting concerns
The following are also explicitly in scope:
- one shared cross-platform visual identity called **Pilgrims Soft Surface**, grounded in the approved current Figma direction and governed textually by file `08`,
- mandatory Light Mode and Dark Mode, plus a System appearance option that follows OS appearance,
- platform-appropriate iOS and Android behavior without forking the product identity,
- centralized theme, semantic-token, depth/effect, and component architecture,
- localization and RTL,
- accessibility,
- offline-first behavior,
- performance and observability,
- real-world verification and release evidence.

The approved Figma source is a visual reference, not a product/IA authority. Product scope, canonical feature names, navigation, screen IDs, entitlement behavior, religious meaning, and localization remain governed by their owning specs.

# 9. Explicitly out of scope for the initial product

The following are out of scope unless later approved and documented.

## 9.1 Government or official process ownership
The app is not responsible for:
- permits,
- official pilgrimage registration,
- ministry-managed approvals,
- visa processing,
- official booking workflows,
- government identity verification workflows,
- replacing official service portals.

The product may hand users off to official services where appropriate.

## 9.2 General travel marketplace features
Out of scope:
- hotel marketplace,
- flight marketplace,
- package comparison marketplace,
- tour marketplace,
- ride-booking marketplace,
- restaurant marketplace.

## 9.3 General social network features
Out of scope:
- public social posting,
- public discovery feed,
- follower systems,
- pilgrim-to-pilgrim social graph,
- chat network unrelated to core group coordination.

## 9.4 Invasive background tracking
Out of scope by default:
- continuous passive family tracking,
- invisible background location sharing,
- persistent background surveillance behavior.

## 9.5 Overbuilt productivity suite
Out of scope:
- full calendar replacement,
- team-style task management,
- complex document management,
- generic file cloud drive behavior,
- broad journaling platform behavior beyond the pilgrimage context.

## 9.6 Religious overreach
Out of scope:
- unreviewed fatwa-style advice,
- broad comparative theology product features,
- casual AI-generated religious rulings without documented governance.

## 9.7 Full emergency dispatch responsibility
The app may assist with communication and access to information, but it is not an emergency dispatch service.

---

# 10. Ethical boundaries

## 10.1 No paywall on core correctness
Core ritual correctness, core guidance needed to avoid major confusion, and baseline help for doing the pilgrimage properly must not be unfairly locked behind monetization.

## 10.2 No paywall on essential safety
Users must not be blocked from accessing essential emergency information or fundamental safety help due to a subscription gate.

## 10.3 Monetize convenience, enhancement, and richer experience
Paid tiers may focus on convenience, richer offline assets, premium organization, extended group coordination, advanced audio/content, and other enhancements that do not violate the ethical boundaries above.

## 10.4 No ads that degrade trust
Advertising models that reduce trust, clutter emergency flows, or make the product feel noisy and exploitative are incompatible with the product direction.

## 10.5 No data-selling posture
The product should not depend on a business model based on exploiting pilgrim data.

---

# 11. Product recommendations adopted into the scope

This section captures key improvements discussed earlier that should influence the product direction.

## 11.1 Figma-first Pilgrims Soft Surface styling
The current approved visual direction is the project-owned **Pilgrims Soft Surface** language defined in file `08`.

The app should use:
- mostly opaque, calm surfaces,
- soft raised/inset depth and restrained ambient accent treatment,
- rounded, touch-friendly geometry,
- semantic surface roles instead of per-screen effect invention,
- one coherent visual identity across iOS and Android,
- mandatory Light and Dark appearances, with System as the recommended default.

Decorative depth must never outrank readability, route clarity, ritual correctness, emergency clarity, large-text usability, or accessible boundaries. Exact Dark Mode values must be intentionally calibrated rather than claimed as Figma-derived unless a dark Figma source is explicitly verified.

## 11.2 3D map utility, not just 3D appearance
The product’s mapping direction should aim for utility closer to an Al-Maqsad-like experience, not simply 3D visuals.

That means the product scope must assume a map subsystem that includes:
- route logic,
- position confidence,
- floor/landmark understanding,
- user-friendly fallback text guidance,
- meaningful offline behavior.

## 11.3 Simple Mode is strategic, not optional
A simplified operating mode is part of the product strategy, not a cosmetic extra.

This should influence:
- home screen priority,
- onboarding,
- phrasebook and emergency tools,
- text density,
- action hierarchy.

## 11.4 Official-service handoff is a product feature
In places where official or ministry-controlled ecosystems are the proper authority, the product should support clean handoff patterns rather than pretending to own those workflows.

## 11.5 Real-world validation is part of product quality
Release confidence must include real-world checks for:
- offline usefulness,
- map usefulness,
- stress readability,
- accessibility,
- degraded network behavior,
- group fallback behavior.

---

# 12. User experience goals

## 12.1 Immediate usefulness
A first-time user should quickly understand where to begin.

## 12.2 Low cognitive load
The app should avoid making users process too much at once.

## 12.3 Fast access to priority actions
High-priority actions should be reachable quickly and predictably.

## 12.4 Strong empty, offline, and fallback states
The app must still feel useful even when ideal data is missing.

## 12.5 Respectful language and tone
Copy should feel clear and respectful, never playful in the wrong context.

## 12.6 Clear upgrade boundaries
If premium features exist, the boundary should feel understandable and ethical rather than manipulative.

---

# 13. Product success criteria

The app is succeeding if users can reliably do the following:
- complete the core guided journey with less confusion,
- recover from common uncertainty or mistakes,
- save and use gate/location anchors,
- coordinate with their group without invasive tracking,
- access emergency and phrase support quickly,
- continue using essential functions offline,
- trust the app enough to rely on it during the journey,
- use the app without being overwhelmed.

The product is also succeeding if the team can:
- change the visual system centrally,
- extend the app without major refactor debt,
- maintain contract consistency,
- onboard new AI agents without major context loss.

---

# 14. Release layering

## 14.1 MVP release intent
The MVP should deliver the core pilgrimage companion value with high reliability, strong offline support for essentials, and low complexity.

## 14.2 V1 release intent
V1 may deepen map fidelity, richer group coordination, stronger content distribution, and more polished premium convenience layers if the foundations remain healthy.

## 14.3 Post-V1 expansion rule
Post-V1 expansion may consider broader pilgrimage scenarios or deeper service integrations, but only through documented product review and architecture validation.

---

# 15. Product guardrails for AI agents

The following rules must be treated as non-negotiable.

## 15.1 Do not quietly expand scope
No agent may introduce a new product direction without explicit approval.

## 15.2 Do not collapse ethical boundaries
No agent may move safety-critical or correctness-critical value behind monetization without explicit documented approval.

## 15.3 Do not sacrifice clarity for style
No agent may implement styling or animation that makes text, maps, or actions harder to use.

## 15.4 Do not convert the app into a surveillance tool
No agent may add passive location-sharing or hidden background tracking as default behavior.

## 15.5 Do not turn the app into a marketplace or social product by accident
No agent may introduce marketplace or social-network patterns unless they are explicitly in scope.

## 15.6 Do not treat 3D map work as purely cosmetic
Map changes must preserve navigational utility and fallback behavior.

## 15.7 Do not undermine maintainability
No agent may implement the app in a way that spreads visual or business logic across many unrelated files when centralized patterns are required.

---

# 16. Product constraints

## 16.1 Connectivity constraints
The app must assume poor or unstable connectivity during real usage.

## 16.2 Stress constraints
The app must assume the user may be stressed, tired, disoriented, or rushed.

## 16.3 Device constraints
The app must support a practical range of devices and avoid treating high-end rendering as guaranteed.

## 16.4 Content-governance constraints
Religious content cannot be treated as ungoverned marketing copy.

## 16.5 Platform constraints
The app should respect platform realities instead of forcing one platform’s behavior onto another when it harms user experience or implementation quality.

---

# 17. Strategic product tradeoffs

This section records the intended bias when product decisions become difficult.

## 17.1 Clarity over density
Prefer clearer structure over packing too much information into one screen.

## 17.2 Reliability over breadth
Prefer a smaller dependable product surface over a bigger fragile one.

## 17.3 Guided usefulness over feature novelty
Prefer features that solve real field problems over features that merely sound advanced.

## 17.4 Maintainability over short-term shortcuts
Prefer centralized systems and clean boundaries over one-off implementation convenience.

## 17.5 Ethical trust over aggressive monetization
Trust and dignity matter more than extracting short-term revenue from anxious users.

---

# 18. Dependencies on other spec files

This file defines the product truth, but later files refine it.

## 18.1 Files that refine product behavior
- `10-PERSONAS-IA-USER-JOURNEYS-AND-TASK-FLOWS.md`
- `11-SCREENS-STATES-NAVIGATION-AND-UI-BLUEPRINTS.md`
- `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`
- `18` through `26` feature-family files

## 18.2 Files that implement technical consequences
- `06-SYSTEM-ARCHITECTURE.md`
- `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`
- `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`
- `09-PLATFORM-ADAPTATION-IOS-ANDROID-AND-NATIVE-BRIDGES.md`
- `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`
- `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`
- `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`
- `16-MAP-ARCHITECTURE-POSITIONING-ROUTING-3D-AND-OFFLINE-WAYFINDING.md`

## 18.3 Files that prove product quality
- `27-TESTING-STRATEGY-TEST-MATRIX-AND-DEVICE-LAB.md`
- `28-REAL-WORLD-VERIFICATION-RELEASE-GATES-AND-EVIDENCE.md`
- `29-SECURITY-PRIVACY-COMPLIANCE-AND-RISK-REGISTER.md`
- `30-DELIVERY-RUNBOOK-INCIDENTS-ROLLBACK-AND-OPERATIONS.md`

---

# 19. When this file must be updated

This file must be updated whenever any of the following changes:
- core mission,
- target users,
- strategic product positioning,
- ethical monetization boundary,
- Umrah-first vs broader pilgrimage scope,
- official-service handoff policy,
- major in-scope or out-of-scope feature decisions,
- product principles,
- release-layering intent.

If product scope changes but this file is not updated, the documentation system becomes unreliable.

---

# 20. Summary

This file defines the product truth for Pilgrims Mobile App.

It establishes:
- the mission,
- the user promise,
- the core user jobs,
- the target users,
- the product principles,
- the Umrah-first scope anchor,
- the in-scope pillars,
- the out-of-scope boundaries,
- the ethical rules,
- the key recommendations adopted into the new product direction,
- the guardrails that must protect future implementation from drift.

All feature, UX, architecture, monetization, content, and validation decisions must remain aligned with this file.

