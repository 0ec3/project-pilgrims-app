# 10 — PERSONAS, IA, USER JOURNEYS, AND TASK FLOWS

## Document status
- **Type:** Normative product behavior and UX structure document
- **Priority:** Highest
- **Audience:** Founder, product lead, design lead, Flutter engineers, QA, AI coding agents, reviewer agents, content/religious governance contributors
- **Purpose:** Define canonical personas, information architecture, core journeys, task flows, recovery flows, offline behavior, accessibility-sensitive behavior, and navigation intent so product, design, implementation, and QA stay aligned.
- **Authority level:** This file is the canonical source of truth for how users move through the product and how the product is structured around their needs. File `11` owns screen-level contracts. Feature-family files own feature behavior. File `31` supersedes quality-first hardening decisions.
- **Last-updated-by:** AI-assisted quality-first hardening pass (validated 2026-06-11)
- **Primary dependencies:** `01`, `03`, `06`, `08`, `09`, `11`, `12`, `15`, `16`, `18`–`25`, `31`, `CONTRACTS/screen_feature_traceability.yaml`
- **Related files:** `13`, `14`, `17`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

Architecture alone does not define what the app must feel like in real use.

This file exists because the app serves pilgrims who may be stressed, tired, distracted, elderly, separated from their group, unfamiliar with smartphones, or operating with weak connectivity. It defines the UX backbone that prevents feature sprawl, dense navigation, and AI-agent drift.

It defines:
- personas,
- top-level IA,
- Home and Simple Mode behavior,
- canonical journeys,
- failure and recovery flows,
- accessibility-sensitive task rules,
- when this file must be updated.

---

# 2. UX strategy summary

## 2.1 Usage modes
The product must optimize for:
1. **Guided pilgrimage mode** — “What do I do now?”
2. **Recovery mode** — “I’m unsure / I made a mistake / I’m lost.”
3. **Coordination mode** — “Where is my group / how do we regroup?”
4. **Preparation mode** — “What should I save, download, or prepare?”
5. **Urgent assistance mode** — “I need help now.”

## 2.2 Product must avoid
The app must avoid:
- overwhelming first-time users with too many entry points,
- burying urgent features behind secondary menus,
- making online-only assumptions during critical flows,
- requiring users to understand system architecture,
- turning every feature into a dense power-user tool,
- hiding privacy/data controls,
- implying stale or failed trusted actions succeeded.

## 2.3 Navigation principle
The app should feel simple at the top level and richer only when the user intentionally enters a relevant feature family.

---

# 3. Primary personas

## 3.1 Persona A — First-time Umrah pilgrim
Needs step-by-step ritual guidance, mistake recovery, gate saving, offline reassurance, and low cognitive load.

High-priority product needs:
- clear start path,
- rituals/RIC,
- next-step guidance,
- Save My Gate,
- phrase/emergency shortcut,
- offline support.

## 3.2 Persona B — Elderly or low-confidence smartphone user
Needs Simple Mode, large touch targets, obvious navigation, emergency shortcuts, reduced clutter, and tolerant back/recovery behavior.

## 3.3 Persona C — Group member
Needs to join a group, read regroup instructions, send “I’m Safe,” follow regroup handoff, and understand stale/expired state without being tracked.

## 3.4 Persona D — Group leader or organizer
Needs to create a group, share a server-generated code, post regroup pins, understand recent member check-ins, and avoid repeated manual coordination while respecting privacy.

## 3.5 Persona E — Stress-response user
Needs immediate help, big text, saved gate recall, phrase/emergency support, group safe/regroup actions, and clear recovery without configuration friction.

## 3.6 Persona F — Quiet planner and note-keeper
Needs planner, reminders, packs, notes/bookmarks, and preparation surfaces that remain local-first and understandable.

## 3.7 Persona G — Privacy/account-management user
Needs to understand what is local-only, what is server-backed, how Supporter works, how restore behaves, and how to request deletion/export without hidden support-only paths.

---

# 4. Cross-persona stress factors

The app must handle:
- low connectivity,
- fatigue,
- crowded high-density environments,
- mixed language confidence,
- accessibility settings,
- low battery,
- group separation,
- privacy concern or account confusion,
- stale or failed trusted operations.

---

# 5. Canonical top-level information architecture

The app uses five conceptual top-level sections:

1. **Home**
2. **Rituals**
3. **Map**
4. **Group**
5. **Tools**

Settings may be reached from Tools, Home, Account Gate, or contextual entry points, but Settings is not a sixth primary tab unless files `10` and `11` are updated.

## 5.1 Section meanings
### Home
Dashboard and recovery surface. Entry point for most users.

### Rituals
Ritual steps, RIC, guidance, and next-step help.

### Map
Wayfinding, Save My Gate, anchors, route guidance, 2D/3D/text modes.

### Group
Group creation, join, check-ins, live board, regroup, shared coordination.

### Tools
Planner, reminders, wallet, notes, bookmarks, phrasebook, emergency, packs, settings entry points where appropriate.

---

# 6. Home architecture

## 6.1 Home purpose
Home is the calm recovery surface for the product.

## 6.2 Home must answer quickly
- What should I do next?
- Where do I go for rituals?
- Where do I go for maps or saved gate?
- How do I reach or create/join my group?
- Where is emergency help or phrase support?
- What important offline/pack/account state needs my attention?

## 6.3 Home content priorities
Recommended order:
1. current journey guidance / quick start,
2. urgent shortcuts,
3. saved gate / recent map action,
4. active group summary or create/join prompt where relevant,
5. planner/reminder summary,
6. preparation/offline pack summary,
7. Settings/Privacy & Data only as low-noise access, not a takeover.

## 6.4 Home must avoid
- becoming a cluttered dashboard with every feature shown equally,
- requiring horizontal exploration to discover core flows,
- showing stale online data as live truth,
- asking for account/permissions before task-linked value is clear.

---

# 7. Canonical user journey inventory

Primary journeys:
- first launch and setup,
- start Umrah guidance,
- resolve uncertainty/mistake with RIC,
- Save My Gate,
- route to destination/regroup/saved anchor,
- create group,
- join group,
- send “I’m Safe” check-in,
- follow regroup pin,
- emergency/assistance shortcut,
- browse/install offline packs,
- add planner item/reminder,
- create note/bookmark,
- manage Supporter/restore,
- Privacy & Data deletion/export/retention flow.

---

# 8. Journey A — First launch and first-time setup

## Goal
Get a new user into a usable state quickly without overwhelming them.

## Primary path
1. Launch screen resolves quickly.
2. User selects language or confirms default locale.
3. User sees concise onboarding focused on value, not feature dump.
4. User is offered simple setup where appropriate.
5. User lands on Home with clear next actions.

## Key product rules
- Do not force account creation before the user can understand the app’s value.
- Do not ask for all permissions up front.
- Do not lead with monetization.
- Keep onboarding short and task-oriented.

## Failure handling
Offline launch still lands in a usable offline-capable Home state.

---

# 9. Journey B — Start Umrah guidance

## Goal
Help the user begin guided Umrah with minimal confusion.

## Primary path
1. User enters Rituals.
2. User confirms relevant context if needed.
3. App creates or resumes local ritual session.
4. App shows current step, next step, and progress.
5. User continues through guidance.

## Key product rules
- Umrah-first default.
- Do not confront default Umrah users with unnecessary Hajj complexity.
- Ritual content is governed, not widget copy.
- Offline use must remain meaningful.

---

# 10. Journey C — Resolve uncertainty or mistake with RIC

## Goal
Help the user recover from uncertainty, interruption, or a mistake.

## Primary path
1. User opens RIC.
2. App asks focused questions or uses ritual context.
3. App evaluates governed local rule content.
4. App returns clear status and recommended next action.
5. User can save or note remedy where relevant.

## Failure handling
If the app cannot confidently resolve, direct the user to a safer fallback explanation rather than pretending certainty.

---

# 11. Journey D — Save My Gate

## Goal
Allow the user to save a memorable anchor for later recovery.

## Primary path
1. User opens save-anchor flow.
2. App proposes or lets user enter/confirm gate/anchor.
3. User saves with optional note/photo.
4. Saved anchor becomes accessible from Home and Map.

## Key product rules
- Must work offline.
- Must remain useful without full map packs.
- Must support manual text-based save if precision is weak.

---

# 12. Journey E — Route to destination / wayfinding

## Goal
Help the user navigate to a destination, regroup pin, or saved anchor.

## Primary path
1. User opens Map or route action.
2. User chooses destination.
3. App assesses position confidence.
4. App computes route if possible.
5. App presents route visually and textually.

## Key product rules
- Low-confidence location must be shown honestly.
- 2D remains a clarity-first option.
- 3D is supportive, not mandatory.
- Text fallback must exist.

---

# 13. Journey F — Create a group

## Goal
Allow a leader to create a trusted coordination group safely.

## Trigger
User chooses Create Group from Group Root, Simple Mode Group shortcut, or a leader-oriented contextual prompt.

## Preconditions
Authenticated online session required.

## Primary path
1. User opens Group.
2. User taps Create Group.
3. If needed, app routes through Account Gate and returns to creation flow.
4. User enters simple group name/context.
5. App calls trusted backend creation endpoint with idempotency.
6. Server creates group, assigns requester as leader, and generates 6-character uppercase alphanumeric code.
7. App shows share-code card and safe system share/SMS handoff.

## Key product rules
- Server generates canonical code.
- App must not import contacts.
- App must not auto-send invitations.
- App must not create social graph data.
- Offline creation must fail honestly; do not queue hidden creation.

## Edge cases
- offline,
- auth expired,
- rate limited,
- duplicate/idempotent retry,
- server unavailable.

## Success outcome
Leader has an active group context and a safe code-sharing path.

---

# 14. Journey G — Join a group

## Goal
Allow a user to join a group safely and clearly.

## Primary path
1. User opens Group.
2. User taps Join Group.
3. If needed, app routes through Account Gate and returns to join.
4. User enters/pastes 6-character code.
5. App validates code via trusted backend.
6. App confirms joined state and shows group summary.

## Key product rules
- Join requires trusted online confirmation.
- Client validates obvious bad format, server remains authoritative.
- User understands they are now in a group context.

---

# 15. Journey H — Send “I’m Safe” check-in

## Goal
Allow a group member to send a fast reassuring status update.

## Primary path
1. User opens quick check-in.
2. App suggests text pin or allows manual text.
3. User confirms.
4. App posts trusted check-in if online.
5. Group state updates with freshness metadata.

## Key product rules
- Text-based coordination, not hidden tracking.
- Ordinary check-ins do not carry precise GPS.
- Offline failure offers manual share/SMS fallback without pretending group board updated.

---

# 16. Journey I — Follow a regroup pin

## Goal
Allow a user to regroup using a shared meeting reference.

## Primary path
1. User sees active regroup pin.
2. User opens details.
3. User launches map route or text guidance.
4. App guides using map, anchor, or text fallback.

## Key product rules
- Text-based guidance remains available.
- Expired/stale regroup state must be clear.
- Map handoff does not grant ongoing location sharing.

---

# 17. Journey J — Emergency / assistance shortcut

## Goal
Let the user reach urgent practical help immediately.

## Primary path
1. User opens emergency/assistance mode.
2. App shows big-text, high-clarity urgent actions.
3. User accesses phrase card, medical profile, saved gate, or “I’m Safe” related action.

## Key product rules
- Works offline.
- Does not require account, group, or entitlement for baseline access.
- Prioritizes clarity over visual polish.

---

# 18. Journey K — Browse and install offline packs

## Goal
Help the user prepare richer offline capability.

## Primary path
1. User opens pack catalog.
2. User sees recommended or available packs from manifest/current cached snapshot.
3. User chooses a pack.
4. App shows size, purpose, entitlement requirement, and install state.
5. User downloads.
6. App verifies manifest/artifact trust chain.
7. App installs only after verification succeeds.

## Key product rules
- Do not imply a pack is ready before verification completes.
- Checksum alone is not enough; signature/key/compatibility/storage checks also apply where required.
- Preserve last-known-good state on candidate failure.
- Support purge and retry.

## Edge cases
- offline with cached manifest only,
- low storage,
- checksum failure,
- artifact signature failure,
- manifest signature failure,
- revoked signing key,
- app compatibility failure,
- entitlement required but missing.

---

# 19. Journey L — Add planner item or reminder

Planner/reminders are local-first. Reminder success should not depend on network. If notification permission is denied, the planner item still exists.

---

# 20. Journey M — Create note or bookmark

Notes/bookmarks are local-first by default. Richer Supporter enhancements must not break baseline note/bookmark retrieval, and downgrade must preserve read access according to file `24`.

---

# 21. Journey N — Supporter / restore / entitlement

## Goal
Let users support the app and restore trusted entitlement state calmly.

## Key product rules
- No aggressive upgrade prompts.
- Never interrupt ritual-critical, emergency, medical, group recovery, or urgent map recovery flows.
- Server truth controls entitlement state.
- Stale entitlement state must be labeled honestly.
- `never_gate` capabilities remain available.

---

# 22. Journey O — Privacy & Data

## Goal
Help users understand and manage local-only data, server-backed data, deletion, export, and retention.

## Trigger
User opens Privacy & Data from Settings Root or account-related entry point.

## Preconditions
- Local explanations available without account.
- Deletion/export/status requests require authenticated online context.

## Primary path
1. User opens Privacy & Data.
2. App explains local-only data versus server-backed data.
3. User can review retention summary.
4. Signed-in user can request account deletion or data export.
5. User can view deletion status where a request exists.
6. App provides public deletion/help handoff where required.

## Key product rules
- Do not imply local-only data was uploaded.
- Do not hide deletion/export behind undocumented support-only channels.
- Do not promise immediate deletion for lawfully retained records.
- Offline state must explain that trusted server requests require network.

---

# 23. Failure and recovery journeys

## 23.1 No network at launch
App opens using local data, Home remains meaningful, online sections degrade clearly.

## 23.2 No permission during map flow
Map remains useful through anchors, destination browsing, and manual/fallback guidance.

## 23.3 Missing pack during map flow
App offers fallback orientation or text guidance and may suggest pack download when online.

## 23.4 Low-confidence map position
App indicates uncertainty and avoids overclaiming precision.

## 23.5 Auth expired during group/account/purchase flow
Local-only features remain usable; protected action pauses safely; re-auth is clear and returns to initiating task where safe.

## 23.6 Entitlement refresh unavailable
App uses safe snapshot for continuity where appropriate and does not promise newly granted access.

## 23.7 Pack trust-chain failure
App blocks candidate activation, preserves last-known-good where available, explains failure calmly, and offers retry/recovery only where safe.

## 23.8 Deletion/export request unavailable
App explains that trusted server request did not happen and preserves local-only explanations.

---

# 24. Simple Mode behavior model

Simple Mode reduces cognitive load and exposes only the highest-value actions:
- Start / Resume Rituals,
- Save My Gate / Map,
- I’m Safe / Group,
- Phrasebook / Emergency,
- Settings where needed.

Simple Mode removes visible complexity but does not create a second product architecture.

---

# 25. Accessibility-sensitive task-flow rules

## 25.1 Large text users
Flows must remain usable when text is significantly larger.

## 25.2 Low-vision users
Critical tasks must not depend on subtle translucency, weak contrast, or tiny map controls.

## 25.3 Screen-reader users
Key flows such as onboarding, rituals, emergency, group creation/join, Privacy & Data, and pack installation must remain understandable with assistive technologies.

## 25.4 Motor/accessibility users
Primary tasks must avoid overly precise gestures or tiny control targets.

---

# 26. Information architecture anti-patterns

Forbidden unless explicitly approved:
- hiding emergency or urgent assistance deep inside secondary navigation,
- treating Tools as a dumping ground,
- exposing too many equal-priority actions on Home,
- building screen flows around implementation boundaries instead of user tasks,
- making online-only assumptions inside core pilgrimage flows,
- creating Simple Mode as a disconnected second app,
- hiding Privacy & Data controls,
- presenting failed trusted writes as success,
- presenting unsigned or unverified packs/content as ready.

---

# 27. When this file must be updated

Update this file when any of these change:
- personas,
- top-level IA,
- Home priorities,
- Simple Mode scope,
- major journey steps or success criteria,
- group creation/join/check-in/regroup behavior,
- Privacy & Data behavior,
- pack/content verification user journeys,
- recovery flow expectations,
- accessibility-sensitive flow requirements.

---

# 28. Summary

This file defines the behavioral and structural UX backbone of Pilgrims Mobile App.

It ensures the product remains:
- understandable,
- calm under stress,
- task-oriented,
- offline-capable,
- privacy-light,
- recoverable,
- and safe for long-term AI-assisted implementation without UX drift.

# 18. Hire a Guide IA and journeys

## 18.1 Additional user contexts
Guide Marketplace particularly serves:
- independent/backpacker Umrah pilgrims,
- first-time pilgrims without an agency Mutawef,
- small families/private groups seeking human ritual accompaniment,
- authenticated users applying to become eligible providers.

These extend existing personas; they do not replace the stress, accessibility, privacy, or offline assumptions already defined here.

## 18.2 Information architecture
Default entry is:

**Tools → Hire a Guide**

Home may expose a low-priority contextual shortcut when relevant, but Hire a Guide must remain below current ritual/recovery, Emergency, Save My Gate/orientation recovery, and urgent Group coordination.

The feature is not a sixth shell destination and is not part of the default Simple Mode urgent set.

## 18.3 Pilgrim journey
```text
Tools
-> Hire a Guide
-> browse/search/filter
-> Guide Profile
-> understand service + pricing + fact-specific current trust
-> Contact Guide
-> explicitly choose approved external channel
-> leave PILGRIMS for direct communication
```

If current trust cannot be established, contact handoff must not imply current eligibility.

## 18.4 Provider journey
```text
Authenticate
-> provider application
-> submit minimum required eligibility information
-> trusted review
-> verification status
-> profile/listing management
-> listing review
-> public discoverability only while eligibility remains current
```

Provider state is not a client role toggle.

## 18.5 Recovery/failure journeys
The journey must explicitly handle:
- network unavailable,
- cached/stale browse,
- provider no longer eligible,
- credential expired/revoked,
- application rejected,
- re-verification required,
- external contact app unavailable,
- feature legally/operationally disabled.

Guide Marketplace failure must never block essential local-first or urgent recovery flows.

---

End of file.