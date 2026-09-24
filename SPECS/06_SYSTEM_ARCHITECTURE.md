# 06 — SYSTEM ARCHITECTURE

## Document status
- **Type:** Normative technical blueprint
- **Priority:** Highest
- **Audience:** Founder, tech lead, mobile lead, backend lead, design-system lead, QA lead, AI coding agents, reviewer agents
- **Purpose:** Define the end-to-end technical architecture of Pilgrims Mobile App so that mobile, backend, storage, maps, packs, content, telemetry, and operational behaviors can be implemented consistently without hidden assumptions or avoidable refactors.
- **Authority level:** This file is the system-level source of truth for component boundaries, runtime responsibilities, trust boundaries, and cross-system data flows. More specific files may refine details, but must not contradict this file.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `02-AI-AGENT-RULES-AND-WORKFLOW.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `05-ROADMAP-PROGRESS-AND-CHANGELOG.md`
- **Related files:** `07`, `08`, `09`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`–`26`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this architecture

This architecture exists to support a product with unusual constraints:
- the app must be useful in stressful, crowded, low-connectivity pilgrimage environments,
- essential help must work offline,
- religious guidance must be structured and governed,
- the mapping experience must be useful even when precise positioning is unavailable,
- group coordination must degrade gracefully,
- the codebase must remain maintainable for long-term AI-assisted development,
- the base app must stay lean and avoid bundling every heavy asset by default.

The architecture therefore prioritizes:
- local-first behavior for essential value,
- a tiny online surface,
- immutable content and pack delivery where possible,
- centralized contracts,
- strict module boundaries,
- additive change patterns,
- graceful degradation under failure.

---

# 2. Architectural goals

## 2.1 Product-facing goals
The system must enable the product to deliver:
- ritual guidance and RIC support that works offline,
- map orientation and saved anchors even without rich connectivity,
- group coordination with both modern and fallback paths,
- emergency and phrase help with near-zero friction,
- downloadable packs for richer offline value,
- ethical entitlement enforcement without hiding core correctness or safety.

## 2.2 Engineering goals
The system must be:
- modular,
- testable,
- observable,
- contract-driven,
- secure by default,
- resilient to partial failure,
- friendly to AI-agent execution and recovery.

## 2.3 Operational goals
The system must support:
- controlled rollout,
- fast hotfixes for content and flags,
- reliable asset distribution,
- measurable performance budgets,
- safe rollback paths,
- low-risk iteration.

---

# 3. Non-goals of the architecture

The architecture is **not** intended to support the following as default assumptions:
- a fully online-first product,
- permanent background location tracking,
- a giant backend surface for all product logic,
- direct client trust for entitlements,
- cloud sync for every user datum,
- a map stack that assumes precise indoor navigation is always available,
- heavy app-bundle packaging of all maps/audio/content,
- fragile one-off integrations without a defined boundary layer.

---

# 4. Architecture principles

## 4.1 Local-first for essential user value
Essential pilgrimage help should work from on-device data whenever possible.

## 4.2 Thin online surface
Only behaviors that truly require connectivity should depend on backend availability.

## 4.3 Contracts before implementation
All cross-boundary behaviors must be defined through canonical docs before large implementation work begins.

## 4.4 Immutable content where possible
Published content and downloadable packs should be versioned and treated as immutable artifacts rather than mutating in place.

## 4.5 Graceful degradation everywhere
Every important subsystem must define what happens when network, storage, positioning, realtime, or a provider fails.

## 4.6 Centralized trust boundaries
Entitlements, group permissions, and sensitive state transitions must be validated in trusted system layers rather than invented by the client.

## 4.7 Maintainability is architectural
Theme centralization, module boundaries, source-of-truth ownership, and reduced duplication are architecture concerns, not merely coding style.

## 4.8 Platform adaptation without architecture drift
iOS-specific or Android-specific experiences may differ, but the core domain architecture and product rules should remain coherent.

---

# 5. High-level system shape

## 5.1 System overview
The system is built around five major runtime zones:
1. **Mobile app runtime (Flutter + selective native bridges)**
2. **Edge API and request-control layer**
3. **Primary data and identity platform**
4. **Static asset and pack delivery platform**
5. **Observability, quality, and operational control layer**

## 5.2 Intended platform stack
### Mobile app
- Flutter application shell
- Platform-native integrations for store APIs, notifications, location, BLE/positioning where applicable, and performance-sensitive map capabilities

### Edge/API layer
- Cloudflare Workers for low-latency HTTP endpoints, request validation, idempotency, ETag handling, rate limiting, and server-side trust enforcement

### Identity and primary data layer
- Supabase for authentication, PostgreSQL data, row-level security, and selected realtime capabilities

### Asset delivery layer
- Cloudflare R2 + CDN for immutable downloadable packs and optionally other static artifacts

### Error tracking and observability
- Centralized crash/error reporting and server/client observability tooling

---

# 6. Canonical component diagram

```text
[User]
  │
  ▼
[Flutter Mobile App]
  ├─ Presentation Layer
  ├─ Domain / Use-case Layer
  ├─ Data / Repository Layer
  ├─ Local Storage Layer
  ├─ Pack Manager
  ├─ Content Runtime
  ├─ Map Runtime
  ├─ Group Coordination Runtime
  ├─ Analytics / Error Queue
  └─ Platform Bridge Layer
          │
          ├──────────────▶ [Cloudflare Workers]
          │                   ├─ Flags / Manifest / Entitlements endpoints
          │                   ├─ Group / Check-in endpoints
          │                   ├─ Receipt validation / restore endpoints
          │                   ├─ Rate limiting / ETag / idempotency
          │                   └─ Service-role access to trusted backend systems
          │
          ├──────────────▶ [Supabase]
          │                   ├─ Auth
          │                   ├─ Postgres
          │                   ├─ RLS
          │                   └─ Realtime (selected flows only)
          │
          └──────────────▶ [R2 + CDN]
                              ├─ Maps packs
                              ├─ Audio packs
                              ├─ Content artifacts where applicable
                              └─ Immutable manifest-addressed assets
```

---

# 7. Component responsibilities

## 7.1 Mobile app runtime
The mobile app is the primary user experience and the primary runtime for essential product value.

### Responsibilities
- render the full UI,
- host the navigation model,
- execute local-first user flows,
- cache and interpret published content,
- execute ritual step and RIC logic from content-defined rules,
- store and retrieve local user data,
- manage packs and downloadable assets,
- render maps and wayfinding UI,
- manage local reminders and simple personal organization,
- collect telemetry and crash signals,
- gracefully handle connectivity and provider failure.

### Must not be responsible for
- inventing entitlements locally,
- becoming the source of truth for server-governed permissions,
- silently redefining API contracts,
- hardcoding content that should be content-governed,
- relying on always-on background tracking.

## 7.2 Cloudflare Workers layer
The Workers layer is the thin trusted API facade.

### Responsibilities
- expose the app’s small online API surface,
- validate requests,
- enforce idempotency where needed,
- provide ETag-based read optimization,
- apply rate limiting,
- mediate trusted server-side access to Supabase or storage where appropriate,
- standardize error envelopes,
- protect sensitive server credentials from the client,
- support observability and request correlation.

### Must not become
- a giant monolith for all product logic,
- the primary home of ritual content logic,
- a replacement for client offline capabilities,
- a place where UI decisions are invented ad hoc.

## 7.3 Supabase layer
Supabase is the primary identity and relational data platform.

### Responsibilities
- user authentication,
- JWT issuance,
- persistent relational data,
- row-level security,
- group membership and authorization enforcement,
- selected realtime coordination features,
- retention-governed server-side records.

### Must not become
- the default sink for every local user datum,
- a reason to turn local-first features into cloud-required features.

## 7.4 R2 + CDN layer
The asset delivery layer is responsible for large immutable artifacts.

### Responsibilities
- storing downloadable pack artifacts,
- globally distributing static assets efficiently,
- supporting resumable/ranged download patterns where needed,
- hosting versioned immutable artifacts,
- enabling checksum verification and content-addressed trust.

### Must not become
- a dynamic API substitute,
- the source of entitlement logic,
- an excuse to bloat the base app with bundled duplicates.

## 7.5 Observability and control layer
This layer ensures the system can be monitored, debugged, and operated safely.

### Responsibilities
- client crash reporting,
- server error monitoring,
- event and request correlation where appropriate,
- release evidence generation support,
- performance measurement,
- operational alerting and debugging support.

---

# 8. Mobile architecture at system level

The detailed Flutter structure lives in file `07`, but the system architecture defines the required mobile layers.

## 8.1 Presentation layer
Responsibilities:
- screens,
- view-state rendering,
- design-system component composition,
- accessibility and localization application,
- user interaction capture.

## 8.2 Domain/use-case layer
Responsibilities:
- application-level orchestration,
- feature workflows,
- policy application,
- state transitions,
- coordination between repositories and local logic.

## 8.3 Data/repository layer
Responsibilities:
- unify local and remote data sources,
- present stable interfaces to use cases,
- manage cache policy,
- manage sync and fetch decisions,
- isolate provider-specific details from feature modules.

## 8.4 Local storage layer
Responsibilities:
- local database,
- key-value settings/preferences,
- secure local sensitive storage,
- downloaded pack metadata,
- local event queue,
- offline-first source-of-truth for relevant entities.

## 8.5 Platform bridge layer
Responsibilities:
- native store APIs,
- notifications,
- device permissions,
- location and BLE access,
- map-provider/native rendering bridges,
- device-specific performance-sensitive services.

---

# 9. Source-of-truth strategy

This section is one of the most important architectural rules in the project.

## 9.1 Product and contract truth
### Canonical source
Documentation files `03`, `06`, `07`, `08`, `13`, `14`, `15`, `16`, and the relevant feature-family files.

### Rule
Implementation may realize the truth, but does not replace the canonical contract without doc updates.

## 9.2 Ritual and religious-content truth
### Canonical source
Published content artifacts plus the content-governance workflow.

### Rule
The app engine interprets ritual content and rules. It must not hardcode rulings or silently diverge from published content definitions.

## 9.3 Entitlement truth
### Canonical source
Server-validated entitlement state.

### Rule
The client may cache entitlements, but must never invent them locally as authoritative truth.

## 9.4 Group membership and authorization truth
### Canonical source
Server-side relational data + RLS-protected authorization model.

### Rule
Client UI may reflect group state, but permission decisions must be enforceable in trusted layers.

## 9.5 Offline operational truth on device
### Canonical source
For local-first features, the device-local store is the operational source of truth during runtime.

### Examples
- planner items,
- saved gates,
- local notes,
- local emergency profile,
- local pack inventory,
- local ritual progress state,
- local cached flags/content snapshots.

## 9.6 Downloadable asset truth
### Canonical source
Manifest-defined immutable pack metadata + verified local installation state.

---

# 10. Trust boundaries

## 10.1 Untrusted zone
The device client is user-controlled and therefore not fully trusted for:
- entitlement truth,
- server-side authorization,
- receipt validation,
- protected write access,
- hidden privileged operations.

## 10.2 Semi-trusted zone
Cached local content and local operational state are trusted for user experience continuity, but not for privileged server decisions.

## 10.3 Trusted server zone
Workers + Supabase trusted backend capabilities enforce:
- JWT validation,
- privileged data access,
- RLS-backed membership checks,
- receipt validation,
- server-governed entitlement state,
- rate limits and idempotency.

## 10.4 Immutable asset trust model
Downloaded assets are trusted only after:
- manifest resolution,
- checksum verification,
- successful installation bookkeeping.

---

# 11. Data and persistence strategy

The detailed canonical schema lives in file `13`, but the architecture defines persistence categories.

## 11.1 Local-only data
Should default to local-only unless an explicit sync requirement is approved.

Examples:
- emergency cards and medical profile,
- saved gate anchors,
- notes/bookmarks,
- planner drafts,
- local ritual session state,
- dismissed banners,
- user visual preferences,
- local pack install state.

## 11.2 Server-governed relational data
Examples:
- user account record,
- group records,
- group membership,
- group check-ins,
- server-side itinerary objects if enabled,
- premium/entitlement state,
- server-side receipt status.

## 11.3 Cached remote data
Examples:
- flags,
- pack manifest,
- entitlement snapshot,
- selected content metadata.

## 11.4 Downloaded artifact storage
Examples:
- map packs,
- audio packs,
- optional high-resolution assets,
- versioned content artifacts if delivered as packs.

## 11.5 Sensitive local storage
Any especially sensitive local data should use stronger local protection measures and explicit retention rules.

---

# 12. Offline-first architecture

This system is not merely “offline tolerant.” It is deliberately offline-first for essential value.

## 12.1 Offline essentials
The architecture must support the following without requiring active connectivity:
- opening Home with last-known local state,
- ritual guidance and RIC execution,
- phrasebook and emergency tools,
- micro-basemap orientation,
- saved gate recall,
- planner/reminders already stored on device,
- local notes/bookmarks,
- previously downloaded packs.

## 12.2 Online-required behaviors
The following require connectivity or a trusted backend interaction:
- joining a server-backed group,
- sending a server-backed check-in,
- validating or restoring purchases,
- refreshing flags/manifest when cache is stale,
- fetching latest entitlement truth,
- realtime live-board features if enabled.

## 12.3 Offline behavior rule
If the network is absent:
- the app should continue to provide local-first value,
- stale cached data should be labeled or handled safely,
- user-critical flows should degrade clearly rather than fail silently,
- the app must not fabricate backend success.

## 12.4 Sync behavior rule
The client should synchronize intentionally and safely:
- queue or retry where appropriate,
- avoid duplicate harmful writes,
- respect idempotency contracts,
- reconcile local and remote state using defined policy rather than guesswork.

---

# 13. Flags and control-plane architecture

## 13.1 Purpose
A lightweight control plane is required for:
- season behavior,
- safety/advisory banners,
- simple feature toggles,
- copy and configuration updates that should not require a full app release.

## 13.2 Architecture rule
Flags are a lightweight remote-configuration surface, not a mechanism to ship broken or hidden architecture.

## 13.3 Control-plane boundaries
Allowed examples:
- season selection,
- banner/advisory visibility,
- small behavior toggles,
- copy tuning,
- recommendation ordering.

Not allowed examples:
- replacing stable product contracts ad hoc,
- introducing entire unplanned features,
- compensating for broken architecture.

## 13.4 Fetch model
Flags should be:
- fetched via a small public endpoint,
- cacheable via ETag,
- usable from last-good cache when offline,
- safe to parse or ignore if malformed.

---

# 14. Pack and asset delivery architecture

## 14.1 Goal
Keep the base app small while allowing richer offline experiences.

## 14.2 Pack types
The architecture should support at least:
- map packs,
- audio packs,
- optionally content/data packs if later justified.

## 14.3 Manifest-first discovery
All downloadable packs must be discovered through the manifest/control path, not through hardcoded URLs inside the client.

## 14.4 Integrity model
A pack is not considered installed until:
- it is fully downloaded,
- verified against expected checksum/integrity data,
- recorded in local pack state.

## 14.5 Storage model
Packs must be:
- purgeable,
- resumable where possible,
- independently versionable,
- separable from bundled assets,
- recoverable after partial failure.

## 14.6 Platform strategy rule
The app architecture must not depend on only one platform-specific asset-loading mechanism.

### iOS note
Apple now treats On-Demand Resources as legacy technology and recommends Background Assets as the modern direction. Therefore the iOS architecture should be written to support a modern asset-delivery approach rather than hard-baking legacy ODR assumptions into every layer.

### Android note
Android asset delivery should also be treated as one platform implementation path beneath the pack manager abstraction, not as the app’s core contract.

## 14.7 Architectural consequence
The canonical app contract is:
- manifest-defined packs,
- verified installation,
- pack-manager abstraction,
- local inventory state,
- fallback if a pack is absent.

The platform-specific delivery mechanism lives under that abstraction.

---

# 15. Authentication and identity architecture

## 15.1 Identity goals
The identity layer must support:
- authenticated users where needed,
- light-friction access for users who do not need a full account immediately,
- safe server-backed permissions for groups and entitlements,
- clear separation between local-only usage and server-backed features.

## 15.2 Authentication model
Primary supported model:
- Supabase-authenticated user identity for server-backed features

Optional product posture:
- limited local-only usage without a full account for offline-first personal features, where explicitly allowed by feature scope.

## 15.3 Identity boundary rule
Features that require trusted server-side permissions must not rely solely on anonymous local identity unless the backend contract explicitly supports that mode.

## 15.4 JWT rule
The mobile client may use JWT-based authenticated requests, but backend trust decisions must validate those tokens in trusted layers.

---

# 16. Authorization architecture

## 16.1 Authorization goals
The system must prevent unauthorized access to group or privileged server-backed functionality.

## 16.2 Enforcement model
Authorization is enforced by a combination of:
- trusted backend validation,
- server-side business checks,
- row-level security,
- scoped roles and permissions.

## 16.3 Client limitation rule
The client may hide or reveal UI surfaces based on cached state, but this is not security. Server-backed authorization must still be enforced independently.

---

# 17. Entitlements architecture

## 17.1 Business rule
Free vs paid access must be determined by trusted entitlement state, not client invention.

## 17.2 Architecture rule
The client may cache entitlements for performance and offline continuity, but the canonical grant state is server-backed.

## 17.3 Entitlement boundaries
Entitlements may govern convenience and richer capabilities, but architecture and contracts must preserve the product’s ethical boundary that correctness-critical and essential safety value are not unfairly paywalled.

## 17.4 Receipt validation
Purchase validation and restore flows must be mediated by trusted backend processes rather than trusting device-side purchase success alone.

---

# 18. Group coordination architecture

## 18.1 Design goal
Support coordination without making the entire experience depend on invasive live tracking.

## 18.2 Supported coordination modes
The architecture should support both:
- backend-backed coordination (join, check-ins, live board where enabled)
- manual or fallback coordination (text-based regrouping, SMS-friendly flows)

## 18.3 Key rule
The app must degrade gracefully from richer live coordination to simpler manual coordination without collapsing the entire feature.

## 18.4 Authorization rule
Group actions must be backed by trusted membership and role enforcement, not merely client-side assumptions.

---

# 19. Ritual and content runtime architecture

## 19.1 Design goal
Ritual logic must be governed, inspectable, and updateable without hardcoding every rule in app code.

## 19.2 Architecture rule
Ritual steps, rule definitions, remedy mappings, and other content-governed structures should live in versioned content artifacts interpreted by app logic.

## 19.3 Client runtime responsibilities
The app may:
- load structured ritual content,
- execute evaluation logic against that content,
- cache and interpret the latest approved local content,
- present user guidance and remedies.

## 19.4 Client runtime must not
- silently encode alternate rulings,
- diverge from content-governed contracts,
- assume a server must be present to answer essential ritual questions.

---

# 20. Map subsystem architecture

The detailed map contract lives in file `16`, but this system architecture defines the major system boundaries.

## 20.1 Architectural decomposition
The map subsystem consists of four distinct layers:
1. **Positioning layer**
2. **Routing and wayfinding layer**
3. **Scene/rendering layer**
4. **Offline fallback and anchor layer**

## 20.2 Why this separation exists
This separation prevents a common failure mode where the product team, engineering team, or AI agent treats “3D map” as if it fully defines the navigation system.

## 20.3 Positioning layer responsibilities
- estimate user position where possible,
- interpret permission state,
- expose confidence-aware position data,
- handle degraded or unavailable positioning.

## 20.4 Routing layer responsibilities
- calculate path or guidance recommendations,
- understand floors/levels/landmarks,
- support fallback text directions or anchor-based guidance,
- avoid provider lock-in from leaking upward.

## 20.5 Scene/rendering layer responsibilities
- display 2D and/or 3D representations,
- render route overlays and landmarks,
- adapt to device capability,
- preserve performance budgets and clarity.

## 20.6 Fallback layer responsibilities
- support micro-basemap use even without packs,
- support saved anchors such as gates,
- support manual “I am here” or text-guidance patterns,
- remain usable when precise positioning is absent.

## 20.7 Architectural rule
The rest of the app should depend on stable map-domain interfaces, not on direct provider-specific primitives everywhere.

---

# 21. Platform strategy

## 21.1 Shared product architecture, selective platform adaptation
The app uses one shared product architecture and one canonical visual identity, **Pilgrims Soft Surface**, across iOS and Android.

Platform differences are allowed for native navigation behavior, sheet/modal conventions, haptics, system bars, transitions, permission/settings handoffs, store APIs, notifications, location/BLE, asset delivery, and map/native capabilities. They must not create separate product identities.

## 21.2 Design adaptation
File `08` owns visual language, semantic tokens, component styling, and mandatory Light/Dark appearance. File `09` owns platform adaptation and native bridges.

The architecture must support:
- System / Light / Dark appearance,
- local persisted appearance preference,
- immediate theme switching without navigation-state reset,
- one shared semantic surface/depth model with platform-specific implementation details only where needed.

## 21.3 Platform-style boundary
Platform-specific behavior and system integration must be implemented through the design system and platform adaptation layer, not ad hoc in feature screens. Feature modules consume semantic/component roles and must not branch on raw platform or raw palette values merely to recreate visual styling.

## 21.4 Native bridge boundary
Native integrations remain isolated behind typed, mockable platform bridge interfaces. Visual-system changes must not weaken store, notifications, location, Bluetooth, map, asset-delivery, or system-capability boundaries.

# 22. Networking architecture

## 22.1 Request strategy
The app should prefer:
- small, cacheable, predictable endpoints,
- explicit retry rules,
- exponential backoff where appropriate,
- idempotent handling for replay-prone operations,
- defensive parsing,
- standard error envelopes.

## 22.2 Read-heavy endpoint strategy
Flags and manifest endpoints should support efficient cache validation using ETag/conditional requests.

## 22.3 Write strategy
Write operations likely to retry must support idempotency or safe duplicate handling according to contract.

## 22.4 Failure strategy
The client must not assume a transient write succeeded unless the trusted backend confirms it.

---

# 23. Caching architecture

## 23.1 Cache categories
The system uses several different caches:
- configuration cache,
- content snapshot cache,
- entitlement snapshot cache,
- local database state,
- pack inventory cache,
- rendered/provider map cache where applicable.

## 23.2 Cache safety rule
Cached data should speed up the app and support degraded operation, but not create silent truth conflicts.

## 23.3 Last-good-value rule
For small control-plane data such as flags, last-good cached values may be used when the network is unavailable, subject to safe fallback behavior.

## 23.4 Cache invalidation rule
Immutable or versioned artifacts should prefer replacement by new version rather than in-place mutation.

---

# 24. Observability architecture

## 24.1 Goals
The system must reveal:
- client crashes,
- backend failures,
- API contract problems,
- pack delivery failures,
- map performance problems,
- sync and retry anomalies,
- degraded feature adoption and quality signals.

## 24.2 Client observability
The mobile app should support:
- crash capture,
- non-PII error logging,
- queued analytics events,
- performance measurement hooks,
- offline-safe event buffering where appropriate.

## 24.3 Server observability
The backend should support:
- request IDs,
- endpoint metrics,
- error-rate visibility,
- rate-limit visibility,
- integrity failures,
- downstream dependency failures.

## 24.4 Privacy rule
Observability must remain PII-light and aligned with the privacy posture of the product.

---

# 25. Security and privacy architecture

## 25.1 Security goals
Protect users, permissions, purchases, and sensitive data without overcomplicating core flows.

## 25.2 Key architectural security controls
- HTTPS transport
- JWT validation in trusted layers
- server-side receipt validation
- row-level security for relational access
- minimized sensitive data exposure
- local encryption/protection for highly sensitive device-only data where appropriate
- no hidden background location collection
- rate limiting and abuse protection

## 25.3 Privacy posture
The system architecture must preserve the product’s privacy-light posture:
- no default background tracking,
- manual sharing by design,
- local-first storage for sensitive personal artifacts where possible,
- server data minimized to what is necessary.

---

# 26. Performance architecture

## 26.1 Performance goals
The system must support:
- fast startup,
- responsive local-first screens,
- lean base-app size,
- efficient pack delivery,
- smooth enough map rendering for the target devices,
- bounded battery/memory impact.

## 26.2 Performance strategy
Achieve this through:
- small online surface,
- local-first data access,
- pack-based heavy asset delivery,
- lazy loading where appropriate,
- stable caches,
- provider abstraction to contain expensive map logic,
- centralized theme and component systems to reduce rendering inconsistency and maintenance complexity.

## 26.3 Performance guardrail
Do not accept architecture that requires the user to download a huge initial bundle just to get baseline value.

---

# 27. Resilience and failure handling

## 27.1 Failure classes to expect
The architecture must assume:
- no network,
- flaky network,
- stale flags/manifest,
- pack corruption,
- partial download,
- provider outage,
- map render failure,
- low storage,
- auth expiry,
- realtime disconnect,
- data conflict,
- schema drift during development,
- client update lag.

## 27.2 General failure policy
Each subsystem must:
- fail safely,
- fail visibly when important,
- preserve essential local value,
- avoid data corruption,
- avoid pretending success occurred when it did not.

## 27.3 Hotfix strategy
Lightweight remote fixes should be possible for controlled surfaces such as flags, safety banners, and configuration-level content selection.

## 27.4 Rollback strategy
The system should support rollback through:
- additive contract evolution,
- controlled release rollout,
- immutable asset versioning,
- manifest rollback,
- backend rollback patterns,
- disabling risky toggles when safe to do so.

---

# 28. Deployment and environment architecture

## 28.1 Environment separation
The system should support clear environment separation for:
- local development,
- test/staging,
- pre-release validation,
- production.

## 28.2 Environment rule
Configuration, secrets, and pack/catalog references must be environment-aware and must not be hardcoded across arbitrary files.

## 28.3 Release control
The architecture should allow:
- phased rollout,
- feature-flag-assisted mitigation,
- pack-manifest rollback,
- backend rollback or hotfix paths,
- release evidence collection.

---

# 29. Cross-file architecture contracts

This file defines the system shape. The following files refine parts of it.

## 29.1 File `07` — Flutter app architecture
Refines:
- codebase structure,
- module boundaries,
- dependency direction,
- folder strategy,
- repository and state patterns.

## 29.2 File `08` — Design system
Refines:
- theme architecture,
- tokens,
- shared components,
- visual semantics.

## 29.3 File `09` — Platform adaptation
Refines:
- iOS/Android platform adaptation while preserving the shared Pilgrims Soft Surface identity,
- native interaction and system-behavior differences,
- typed native bridges.

## 29.4 File `13` — Data model
Refines:
- relational schema,
- invariants,
- RLS rules,
- migrations.

## 29.5 File `14` — API contracts
Refines:
- exact endpoint shapes,
- auth and idempotency rules,
- error envelopes,
- realtime event definitions.

## 29.6 File `15` — Offline/packs/sync
Refines:
- cache policy,
- sync and queue behavior,
- manifest and pack lifecycle,
- storage and integrity details.

## 29.7 File `16` — Map architecture
Refines:
- provider strategy,
- positioning model,
- routing graph,
- 3D scene behavior,
- map data schema,
- offline wayfinding contract.

## 29.8 Feature-family files
Refine the user-facing and domain-specific behavior built on this architecture.

---

# 30. Architecture decisions already established

These decisions are already active and should be preserved unless explicitly superseded.

## 30.1 Compact controlled architecture
The project uses a compact but high-authority documentation structure rather than excessive fragmentation.

## 30.2 Local-first essentials
Essential pilgrimage value must remain available on device.

## 30.3 Tiny online surface
Only a small number of backend flows are required for core system operation.

## 30.4 Centralized theming and design tokens
Flutter UI architecture must centralize visual rules instead of scattering them.

## 30.5 Umrah-first product and control-plane behavior
The system architecture must support season-aware behavior without silently broadening scope.

## 30.6 Map subsystem as full system
The map layer is not a mere view. It is a multi-layer subsystem.

## 30.7 Official-service handoff posture
The system may hand users off cleanly to official flows rather than trying to own authority-managed workflows.

## 30.8 Real-world verification over fake-green confidence
The architecture must remain testable in real-world degraded conditions, not only in ideal CI conditions.

---

# 31. Recommendations incorporated into this architecture

This section records important improvements derived from earlier analysis and current platform research.

## 31.1 Recommendation — asset delivery abstraction over platform lock-in
The architecture now defines pack delivery through a pack-manager abstraction rather than baking every assumption into ODR/PAD terminology.

Reason:
- iOS asset-delivery guidance has shifted toward Background Assets,
- platform-specific delivery mechanisms should remain implementation details beneath the app’s manifest/integrity contract.

## 31.2 Recommendation — provider abstraction in maps
The architecture requires stable map-domain boundaries so the rest of the app does not depend directly on whichever provider ultimately renders 3D or 2D maps.

## 31.3 Recommendation — local-first source-of-truth discipline
The architecture makes explicit that essential runtime behavior should prefer local truth and safe cached state rather than fragile constant backend dependence.

## 31.4 Recommendation — maintainability as architectural control
Theme centralization, component reuse, and clear module boundaries are explicitly elevated into architecture so AI agents do not accidentally create UI debt.

## 31.5 Recommendation — graceful fallback as a first-class success metric
The architecture treats fallback behavior as part of success, not merely an error state.

---

# 32. Anti-patterns forbidden by this architecture

The following are forbidden unless explicitly approved through change control.

## 32.1 Hardcoding ritual rules in app logic
Forbidden.

## 32.2 Direct provider-specific map dependency spread across features
Forbidden.

## 32.3 Client-derived entitlement truth
Forbidden.

## 32.4 Requiring network for essential ritual/emergency functionality
Forbidden.

## 32.5 Scattering style tokens across feature code
Forbidden.

## 32.6 Treating realtime as mandatory for group usefulness
Forbidden.

## 32.7 Silent contract drift between app, backend, and docs
Forbidden.

## 32.8 Using flags to hide architectural problems instead of fixing them
Forbidden.

---

# 33. When this file must be updated

This file must be updated whenever any of the following changes:
- major infrastructure choice,
- backend surface strategy,
- authentication/authorization posture,
- asset delivery strategy,
- trusted-boundary model,
- local-first versus cloud-first assumptions,
- map subsystem decomposition,
- observability/security architecture,
- environment or rollout strategy,
- major resilience or fallback assumptions.

If any of those change but this file is not updated, downstream files will drift quickly.

---

# 34. Summary

This file defines the end-to-end system architecture of Pilgrims Mobile App.

It establishes:
- the major runtime zones,
- the component responsibilities,
- the trust boundaries,
- the source-of-truth strategy,
- the offline-first posture,
- the control-plane and pack-delivery architecture,
- the identity and entitlement architecture,
- the map subsystem decomposition,
- the resilience, security, observability, and performance posture,
- the cross-file architecture boundaries that future specs must refine.

This architecture is intentionally optimized for:
- calm, reliable pilgrimage assistance,
- offline usefulness,
- maintainability,
- and safe AI-agent implementation over time.

