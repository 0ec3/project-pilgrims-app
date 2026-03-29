# Pilgrims Mobile App — Final Compact 30-File Spec System

This is the final compact documentation architecture for building the app with AI agents while keeping the spec system comprehensive, consistent, and maintainable.

## Design goals for this spec system

- Cover the full product, technical, UX, map, data, quality, and delivery scope.
- Stay compact enough for humans and AI agents to navigate reliably.
- Prevent AI-agent drift, hallucination, uncontrolled scope growth, and destructive refactors.
- Keep hard contracts separate from descriptive guidance.
- Make Flutter code, assets, themes, and modules easy to maintain over time.
- Centralize style rules so visual changes do not require touching many unrelated files.

## Rules for the whole spec set

- Every file must have a clear owner and purpose.
- Every file must state which other files it depends on.
- Every file must state when it must be updated.
- Contract files are normative. Feature and process files must not silently override them.
- Feature-family files must use a consistent template.
- Flutter implementation must follow centralized theme and token architecture; hardcoded colors, spacing, typography, shadows, blur, motion, and strings in feature widgets are forbidden unless explicitly documented as an exception.

---

# Final compact 30-file spec list

## 01-README-AND-MASTER-INDEX.md
**Purpose**
The root entry point for the entire documentation system.

**Must contain**
- Project overview
- Reading order for humans and AI agents
- Full file index with one-line purpose for each file
- Which files are normative vs informative
- Cross-file dependency map
- “If you are doing X, read these files first” matrix
- Documentation update matrix
- Repo structure summary

---

## 02-AI-AGENT-RULES-AND-WORKFLOW.md
**Purpose**
Operational rules for AI coding agents, reviewer agents, and debugging agents.

**Must contain**
- Required reading order before starting any task
- Rules for asking clarifying questions
- Rules for refusing to continue if critical context is missing
- No scope expansion without explicit approval
- No undocumented refactor rule
- No “change code only to satisfy tests” rule
- Required codebase inspection before editing
- Required schema and relation inspection before DB changes
- Required post-task documentation updates
- Task completion checklist
- Error-handling and recovery rules for confused agents

---

## 03-PRODUCT-CHARTER-AND-SCOPE.md
**Purpose**
Define the product identity, mission, boundaries, and release scope.

**Must contain**
- Product mission
- User promise
- Target users and personas summary
- Non-goals
- Ethical rules
- Religious correctness and safety principles
- Free vs paid philosophy
- Umrah-first/Hajj-season scope policy
- MVP scope
- V1 scope
- Post-V1 scope
- Explicit forbidden features unless approved
- Official-service handoff principle

---

## 04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md
**Purpose**
Single source for canonical terms, decision history, and controlled change process.

**Must contain**
- Glossary of product, ritual, technical, map, and business terms
- Canonical naming rules
- Forbidden synonyms or ambiguous terms
- Architecture decision records
- Product decision records
- Change approval workflow
- Breaking-change rules
- Deprecation policy

---

## 05-ROADMAP-PROGRESS-AND-CHANGELOG.md
**Purpose**
Track what is planned, what is built, what changed, and what is currently in progress.

**Must contain**
- Delivery phases
- Milestones and release plan
- Module-by-module progress tracker
- Current active work summary
- Known blockers
- Handoff context for new AI agents
- Changelog of product and technical changes
- Links to release evidence

---

## 06-SYSTEM-ARCHITECTURE.md
**Purpose**
Canonical overview of the full system architecture.

**Must contain**
- High-level architecture diagram
- Mobile app architecture context
- Backend/service boundaries
- Auth and identity flow
- Storage boundaries
- Edge/API boundaries
- Realtime boundaries
- Pack delivery flow
- Content publishing flow
- Map subsystem position in the architecture
- Third-party integration boundaries
- Failure domains and fallback rules

---

## 07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md
**Purpose**
Define how the Flutter codebase must be structured and maintained.

**Must contain**
- Folder structure and package/module structure
- Feature-first vs layer-first rule
- Shared/core/common module rules
- Public interfaces between modules
- Dependency direction rules
- State management architecture
- Navigation architecture
- Repository pattern rules
- Platform channel boundaries
- Asset organization rules
- Localization file organization
- Forbidden dependency patterns
- Refactor guardrails
- Code ownership map

**Must explicitly require**
- No hardcoded design values in feature widgets
- No hardcoded business strings in feature widgets
- Centralized theme, tokens, and design constants
- Reusable component library instead of duplicate widget patterns

---

## 08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md
**Purpose**
Canonical design system for the whole app and the central source of visual rules.

**Must contain**
- Design principles
- Semantic color system
- Typography system
- Spacing scale
- Radius and shape scale
- Shadow and elevation rules
- Blur/material rules
- Motion and animation tokens
- Iconography rules
- Dark/light mode rules if applicable
- Glass vs solid surface rules
- Component catalog
- Component anatomy and states
- Accessibility contrast rules
- RTL visual rules
- Design token implementation strategy in Flutter

**Must explicitly define Flutter maintainability rules**
- Central theme files
- Central token files
- Central component styling rules
- Text styles defined once
- Animation durations and curves defined once
- Effect presets defined once
- Route/page transition definitions centralized
- No direct hex colors inside feature widgets
- No one-off padding/margin magic numbers unless tokenized

---

## 09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md
**Purpose**
Define platform-specific behavior, styling adaptation, and native bridge boundaries.

**Must contain**
- iOS-specific visual adaptation rules
- Liquid-glass usage rules
- Where glass is allowed and forbidden
- Readability and reduced-transparency fallbacks
- Android visual adaptation rules
- Platform parity vs platform-native behavior policy
- Native bridge modules
- BLE access rules
- Location access rules
- Map/native rendering bridge rules
- Notification bridge rules
- Purchase/store bridge rules
- Performance-sensitive native module rules

---

## 10-PERSONAS-IA-USER-JOURNEYS-AND-TASK-FLOWS.md
**Purpose**
Tie product decisions to real users and real usage flows.

**Must contain**
- Detailed personas
- Accessibility-related personas
- Elderly/low-literacy persona
- Group leader persona
- First-time pilgrim persona
- Stress/fatigue context scenarios
- Information architecture
- App navigation hierarchy
- Core user journeys
- Critical task flows
- Alternative flows
- Failure and recovery flows
- Offline-specific journeys

---

## 11-SCREENS-STATES-NAVIGATION-AND-UI-BLUEPRINTS.md
**Purpose**
Screen-level contracts for the app.

**Must contain**
For every screen:
- Screen purpose
- Entry points
- Data dependencies
- Inputs and outputs
- Empty/loading/error/offline states
- Navigation actions
- Bottom sheet/dialog rules
- Connected components
- Analytics events
- Accessibility notes
- Linked feature family
- Linked tests

---

## 12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md
**Purpose**
Govern all content presentation and inclusive UX rules.

**Must contain**
- Tone and copy principles
- Religious respect rules
- Error message style
- Safety messaging rules
- Premium/paywall messaging rules
- Supported languages
- Translation management rules
- RTL behavior rules
- Arabic transliteration/transcription policy
- Pluralization rules
- Accessibility requirements
- Dynamic text sizing rules
- Screen reader rules
- High-contrast and low-vision rules
- Simple mode language rules

---

## 13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md
**Purpose**
Canonical data model and database truth.

**Must contain**
- Entity catalog
- Table list
- Column definitions
- Relationship map
- Ownership rules
- Invariants and forbidden states
- Constraints and indexes
- Soft-delete rules
- Row-level security policy matrix
- Role and permission matrix
- Migration strategy
- Backfill rules
- Rollback rules
- Data integrity verification steps
- Seed data policy

---

## 14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md
**Purpose**
Canonical backend contracts.

**Must contain**
- REST endpoint list
- Request/response schemas
- Error envelope
- Idempotency rules
- Pagination rules
- Auth rules
- Versioning strategy
- Realtime channel/event schema
- Ordering and dedupe rules
- Retry rules
- Cache rules
- Third-party integration contract boundaries
- Webhook/event handling if used
- Contract testing rules

---

## 15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md
**Purpose**
Canonical offline and asset delivery behavior.

**Must contain**
- Offline-first rules
- Source-of-truth rules on device
- Sync strategy
- Queueing and reconciliation
- Pack types and boundaries
- Asset manifest structure
- Versioning and checksums
- Partial updates
- Corruption handling
- Cache invalidation rules
- Storage quotas and budgets
- Download/resume/retry rules
- Dependency rules between packs
- Fallback rules when offline assets are incomplete

---

## 16-MAP-ARCHITECTURE-POSITIONING-ROUTING-3D-AND-OFFLINE-WAYFINDING.md
**Purpose**
Canonical map and wayfinding system spec.

**Must contain**
- Overall map strategy
- Provider strategy and rationale
- 2D vs 3D behavior
- Indoor vs outdoor behavior
- Positioning methods and confidence rules
- BLE/beacon assumptions if used
- Routing graph model
- Multi-level wayfinding rules
- Landmark model
- Floor model
- POI/facility model
- Camera behavior
- 3D scene/layer rules
- Route text generation rules
- Save My Gate dependencies
- Group-location dependencies
- Offline map fallback rules
- Legal/attribution requirements
- Performance budgets specific to map rendering

---

## 17-ANALYTICS-OBSERVABILITY-AND-PERFORMANCE-BUDGETS.md
**Purpose**
Measure real behavior, detect failures, and prevent slow decay.

**Must contain**
- Analytics taxonomy
- Event naming rules
- Feature event map
- Funnel definitions
- Privacy-safe analytics rules
- Logging strategy
- Crash reporting strategy
- Error taxonomy
- Alert thresholds
- Tracing/diagnostics if used
- App startup budget
- Screen render budgets
- Battery/memory budgets
- Network budgets
- Map FPS/performance targets
- Asset size budgets

---

## 18-FEATURE-RITUALS-RIC-AND-RELIGIOUS-CONTENT.md
**Purpose**
Feature-family spec for ritual guidance and mistake-resolution logic.

**Must contain**
- Feature purpose and value
- Supported ritual scope
- Ritual step model
- RIC/Resolver behavior
- Mistake/remedy model
- Religious content object structure
- Scholar review dependency
- UI surfaces
- State machine
- Offline behavior
- Entitlement boundaries
- Analytics events
- Edge cases
- Error handling
- Test cases
- Release readiness checklist

---

## 19-FEATURE-MAPS-SAVE-MY-GATE-AND-3D-WAYFINDING.md
**Purpose**
Feature-family spec for maps and user-facing wayfinding features.

**Must contain**
- Feature purpose and value
- Save My Gate behavior
- Gate marker model
- User pin behavior
- Route request behavior
- Destination categories
- Facility discovery behavior
- 3D user experience rules
- Indoor guidance behavior
- Regroup/navigation link points
- Offline fallback behavior
- Failure states and fallback text directions
- Analytics events
- Accessibility notes
- Test cases
- Release readiness checklist

---

## 20-FEATURE-GROUP-HUB-CHECKINS-REGROUP-AND-SHARED-COORDINATION.md
**Purpose**
Feature-family spec for group coordination.

**Must contain**
- Group model summary
- Group roles
- Membership flows
- Join/invite rules
- Check-in model
- Live board behavior
- Regroup pin behavior
- Shared itinerary behavior if included
- Location/privacy rules
- SMS/manual fallback rules
- Offline behavior
- Presence and freshness rules
- Entitlement boundaries
- Analytics events
- Edge cases
- Test cases
- Release readiness checklist

---

## 21-FEATURE-PLANNER-REMINDERS-WALLET-NOTES-AND-BOOKMARKS.md
**Purpose**
Feature-family spec for personal planning and memory tools.

**Must contain**
- Planner flows
- Reminder behavior
- Local vs server reminder rules
- Wallet item model
- Notes model
- Bookmark model
- Attachment/media rules if any
- Search/filter behavior
- Offline behavior
- Sync behavior
- Entitlement boundaries
- Analytics events
- Edge cases
- Test cases
- Release readiness checklist

---

## 22-FEATURE-PHRASEBOOK-EMERGENCY-SAFETY-AND-ASSISTIVE-TOOLS.md
**Purpose**
Feature-family spec for assistance during stress, confusion, and emergencies.

**Must contain**
- Phrasebook data model
- Emergency card model
- Safety alert model
- Emergency mode/home shortcut behavior
- Big-text presentation rules
- Audio/text fallback rules
- Local/offline behavior
- Source and freshness policy for safety advisories
- Entitlement boundaries
- Group escalation links
- Analytics events
- Accessibility notes
- Edge cases
- Test cases
- Release readiness checklist

---

## 23-FEATURE-OFFLINE-PACKS-AUDIO-AND-CONTENT-DISTRIBUTION.md
**Purpose**
Feature-family spec for downloadable content and offline media.

**Must contain**
- Pack catalog UX
- Pack detail behavior
- Download manager UX
- Queue behavior
- Audio pack behavior
- Content dependency map
- Language-specific pack rules
- Storage and eviction UX
- Retry and corruption UX
- Entitlement boundaries
- Analytics events
- Edge cases
- Test cases
- Release readiness checklist

---

## 24-FEATURE-ACCOUNT-SUBSCRIPTIONS-ENTITLEMENTS-AND-SETTINGS.md
**Purpose**
Feature-family spec for identity, purchases, and app preferences.

**Must contain**
- Account states
- Sign-in/sign-out flows
- Guest behavior if supported
- Subscription products
- Entitlement keys
- Restore purchase behavior
- Family sharing/platform wording rules
- Store-specific edge cases
- Settings categories
- Notification preferences
- Map/data/download preferences
- Privacy preferences
- Analytics events
- Error handling
- Test cases
- Release readiness checklist

---

## 25-FEATURE-ONBOARDING-HOME-AND-SIMPLE-MODE.md
**Purpose**
Feature-family spec for first-run experience and simplified operation.

**Must contain**
- Onboarding goals
- Permission timing rules
- Home/dashboard logic
- Personalization inputs
- Entry points to critical features
- Simple mode rules
- Elder mode considerations if used
- Quick-action layout
- Offline-first home behavior
- Analytics events
- Accessibility notes
- Edge cases
- Test cases
- Release readiness checklist

---

## 26-CONTENT-MODEL-SCHOLAR-REVIEW-AND-PUBLISHING-WORKFLOW.md
**Purpose**
Govern all structured content and religious correctness workflow.

**Must contain**
- Content types
- Draft/review/publish lifecycle
- Scholar review workflow
- Approval roles
- Emergency correction workflow
- Versioning and history
- Content provenance/source attribution model
- Translation workflow
- Rollback rules
- Publish validation checklist
- Content QA rules

---

## 27-TESTING-STRATEGY-TEST-MATRIX-AND-DEVICE-LAB.md
**Purpose**
Canonical quality plan for automated and manual testing.

**Must contain**
- Testing philosophy
- Test pyramid/scope
- Unit/widget/integration/E2E definitions
- Feature-by-feature test matrix
- Offline test matrix
- Device matrix
- OS/version support matrix
- RTL and localization tests
- Accessibility tests
- Store/purchase tests
- Map and native bridge tests
- Mock/stub rules
- Fixture rules
- CI expectations
- Test evidence requirements

---

## 28-REAL-WORLD-VERIFICATION-RELEASE-GATES-AND-EVIDENCE.md
**Purpose**
Prevent fake success and require real proof before release.

**Must contain**
- Manual verification checklist
- On-device checks
- Real-network checks
- Offline/airplane-mode checks
- Navigation checks
- Subscription/restore checks
- Map route correctness checks
- Emergency mode checks
- Accessibility checks
- Required screenshots/videos/logs
- Go/no-go gates
- Known-issue policy
- Sign-off responsibilities

---

## 29-SECURITY-PRIVACY-COMPLIANCE-AND-RISK-REGISTER.md
**Purpose**
Protect users, data, and the business.

**Must contain**
- Data classification
- Sensitive-data handling
- Secret management rules
- Encryption rules
- Token/session rules
- Deletion and retention policy
- Abuse prevention considerations
- Location/privacy constraints
- Compliance obligations relevant to the app
- Legal copy ownership
- Risk register
- Mitigation plan
- Incident severity matrix

---

## 30-DELIVERY-RUNBOOK-INCIDENTS-ROLLBACK-AND-OPERATIONS.md
**Purpose**
Operational runbook for shipping, support, incidents, and safe recovery.

**Must contain**
- Deployment workflow
- Environment strategy
- Release procedure
- Feature-flag strategy
- Rollback procedure
- Hotfix process
- Incident response workflow
- Escalation contacts/roles
- Operational dashboards/checks
- Support handoff rules
- Postmortem template
- Disaster recovery summary

---

# Cross-file relationship rules

## The most important dependency flow
- `03-PRODUCT-CHARTER-AND-SCOPE.md` defines what the app is.
- `06-SYSTEM-ARCHITECTURE.md` defines how the whole system is organized.
- `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md` defines how the Flutter codebase must be structured.
- `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md` defines how UI styling is centralized.
- `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md` defines the canonical data structure.
- `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md` defines service contracts.
- `16-MAP-ARCHITECTURE-POSITIONING-ROUTING-3D-AND-OFFLINE-WAYFINDING.md` defines the map subsystem.
- `18` through `25` define feature-family behavior.
- `27` and `28` define how correctness is proven.

## Update rules
- If data schema changes: update 13, 14, impacted feature files, 27, 28, and 05.
- If a UI pattern changes: update 08, 09 if platform-specific, impacted screen sections in 11, impacted feature files, and 30 if operational behavior changes.
- If a map behavior changes: update 16, 19, related screen entries in 11, analytics/performance in 17, tests in 27, and release evidence in 28.
- If entitlements change: update 03, 14, 24, impacted feature files, 27, 28, and 05.
- If onboarding or navigation changes: update 10, 11, 25, related feature files, 27, and 28.

---

# Flutter maintainability rules that must be enforced by the specs

These rules should be repeated in files 07 and 08 and referenced by feature files.

## Centralized styling
- All colors must come from semantic design tokens.
- All text styles must come from centralized typography definitions.
- All shadows, blur, opacity, and glass effects must come from centralized effect tokens.
- All animations must come from centralized motion tokens.
- All radii and spacing must come from centralized layout tokens.
- No feature widget may define its own ad-hoc style constants unless documented as a shared token candidate.

## Centralized text and copy
- Reusable UI copy must come from localization resources, not inline strings.
- Error, loading, offline, and empty-state messaging must use shared copy patterns.

## Centralized components
- Repeated visual patterns must be implemented as shared components.
- Shared components must reference tokens, not raw values.
- Platform variations must be handled inside the design system/component layer where possible.

## Centralized routing and transitions
- Page transitions, modal transitions, and route naming must be centralized.
- No feature module may invent route patterns inconsistent with the navigation architecture.

## Centralized assets
- Asset folder structure must be organized by type and purpose.
- Pack-delivered assets must be separated from bundled assets.
- Map assets, icons, illustrations, audio, and localization resources must each have a clear home.

## Centralized state boundaries
- Feature UI must not talk directly to low-level data sources.
- Repositories/use-cases/controllers must follow documented boundaries.

---

# Final guidance on file count

This 30-file system is the compact version that still covers everything important.

It is compact because:
- related governance concerns are merged,
- related UX concerns are merged,
- features are grouped into families,
- platform-specific behavior is grouped carefully,
- quality and release evidence are each preserved as dedicated files.

It is still safe because:
- hard contracts remain separate,
- map complexity has its own canonical file,
- Flutter structure and design-system structure are explicit,
- AI-agent operating rules remain first-class.

This is the recommended final documentation architecture for the project.

