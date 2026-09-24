# 07 — FLUTTER APP ARCHITECTURE AND MODULE BOUNDARIES

## Document status
- **Type:** Normative technical architecture document
- **Priority:** Highest
- **Audience:** Flutter engineers, mobile tech lead, design-system engineers, QA, AI coding agents, reviewer agents
- **Purpose:** Define how the Flutter app must be organized, how modules are separated, how dependencies must flow, where shared code lives, how assets and localization are structured, and how UI styling is centralized so the codebase remains scalable, maintainable, and safe for AI-agent-driven development.
- **Authority level:** This file is the canonical source for Flutter project structure, module boundaries, and shared-code rules. Feature or implementation files must not contradict this file.
- **Primary dependencies:** `01_README_AND_MASTER_INDEX.md`, `02_AI_AGENT_RULES_AND_WORKFLOW.md`, `03_PRODUCT_CHARTER_AND_SCOPE.md`, `06_SYSTEM_ARCHITECTURE.md`
- **Related files:** `08`, `09`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`–`26`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This file defines how the Flutter codebase must be organized so the app remains understandable and maintainable as it grows.

This project has unusually high architectural risk because:
- the app includes many feature families with cross-cutting concerns,
- offline behavior is central rather than optional,
- maps and platform bridges are complex,
- design consistency is important,
- AI coding agents will be used heavily,
- AI agents are prone to scattering code, duplicating patterns, hardcoding styles, and losing track of module ownership.

This file exists to prevent those failures.

It defines:
- the Flutter repository structure,
- the package/module strategy,
- the dependency direction rules,
- the layering model,
- how shared and feature-specific code are separated,
- how themes/tokens/components are centralized,
- how assets and localization are organized,
- what AI agents may and may not do when editing Flutter code.

---

# 2. Architecture goals

## 2.1 Maintainability goal
A contributor should be able to find the correct place for a new widget, state holder, repository, or asset without guessing.

## 2.2 Refactor-resistance goal
The codebase should tolerate feature growth without frequent large-scale refactors caused by weak boundaries.

## 2.3 Design-consistency goal
The visual system must be centralized so palette, spacing, motion, Soft Surface depth/effect presets, typography, and component styling can be changed from controlled theme/token layers rather than scattered widget edits.

## 2.4 AI-agent safety goal
An AI coding agent should be able to inspect the repo, identify the correct module, and implement a change without introducing architectural confusion, duplicate code, or styling debt.

## 2.5 Offline-first goal
The Flutter architecture must make it straightforward to implement local-first behavior, cached state, and sync orchestration without bypassing repository boundaries.

## 2.6 Platform-adaptation goal
Platform-specific behavior must be implemented through explicit adaptation layers and bridges, not hidden inside random feature widgets.

---

# 3. Core principles

## 3.1 Feature-first at the product layer
Most user-facing app code should be organized by feature or feature family, not by generic technical layer folders scattered across the entire app.

## 3.2 Shared code only when truly shared
Code should move into shared/core/design-system packages only when it is reused, conceptually stable, and belongs there.

## 3.3 Stable dependency direction
Higher-level product modules may depend on shared/core abstractions, but not the other way around.

## 3.4 Centralized design system
Colors, typography, spacing, radius, blur, shadow, animation, and component surface behavior must be defined centrally.

## 3.5 Repository boundaries are mandatory
Feature UI and state layers must not reach directly into low-level storage or network clients.

## 3.6 Platform-specific code is isolated
Native or platform-conditional logic must live behind bridge interfaces or adaptation layers.

## 3.7 Prefer additive evolution
When the architecture changes, prefer additive and well-scoped changes over broad churn.

## 3.8 Generated code and source code must be distinguishable
Generated artifacts must not be treated as hand-edited source-of-truth files.

---

# 4. Project structure strategy

## 4.1 Recommended repository shape
The project should use a package-oriented monorepo structure so the app, design system, and shared domain/code can be maintained cleanly over time.

## 4.2 Recommended top-level repository layout
```text
repo/
  apps/
    pilgrims_mobile_app/
  packages/
    pilgrims_app_core/
    pilgrims_design_system/
    pilgrims_domain/
    pilgrims_data/
    pilgrims_platform/
    pilgrims_l10n/
    pilgrims_testkit/
  tools/
  docs/
  scripts/
```

## 4.3 Why a package-oriented monorepo is recommended
A package-oriented structure helps:
- make ownership clearer,
- prevent massive `lib/` sprawl,
- isolate shared concerns cleanly,
- make AI-agent navigation safer,
- support scaling without turning the main app package into a single giant dependency graph.

## 4.4 Workspaces rule
If a package-oriented monorepo is used, dependency management and tooling should be aligned with a workspace-friendly setup so package relationships remain explicit and reproducible.

---

# 5. Package responsibilities

This section defines the recommended package boundaries.

## 5.1 `apps/pilgrims_mobile_app`
The main Flutter application entry point.

### Responsibilities
- app bootstrapping,
- environment wiring,
- route registration,
- app-shell composition,
- feature integration,
- top-level dependency injection wiring,
- platform-specific app configuration.

### Must not become
- the dumping ground for every shared utility,
- the only place where themes/components live,
- the only place where domain logic exists.

## 5.2 `packages/pilgrims_design_system`
Canonical design system implementation package.

### Responsibilities
- design tokens,
- theme definitions,
- typography system,
- Pilgrims Soft Surface depth/effect presets,
- common component implementations,
- motion tokens,
- semantic colors,
- platform-adapted component styling,
- icon usage contracts where appropriate.

### Must not contain
- feature business logic,
- feature-specific data fetching,
- screen-specific product rules.

## 5.3 `packages/pilgrims_domain`
Pure domain layer package.

### Responsibilities
- domain entities,
- value objects,
- use-case interfaces or core business contracts,
- feature-agnostic domain policies,
- domain validation rules that are independent of transport or storage implementation.

### Must not contain
- Flutter UI code,
- HTTP clients,
- database drivers,
- provider-specific map SDK code,
- platform channel code.

## 5.4 `packages/pilgrims_data`
Data-layer package.

### Responsibilities
- repository implementations,
- local data sources,
- remote data sources,
- sync orchestration helpers,
- DTO mapping,
- cache handling,
- pack metadata persistence,
- error translation between data sources and domain/application layers.

### Must not contain
- feature UI widgets,
- direct screen logic,
- hardcoded component styling.

## 5.5 `packages/pilgrims_platform`
Platform bridge package.

### Responsibilities
- platform-channel wrappers,
- native service adapters,
- store bridge,
- notifications bridge,
- location/BLE bridge,
- map-native bridge abstractions,
- device capability queries.

### Must not contain
- product feature state machines,
- general UI composition,
- direct business entitlement decisions.

## 5.6 `packages/pilgrims_app_core`
App-level shared infrastructure package.

### Responsibilities
- app-wide constants that are not design tokens,
- environment/config models,
- logging abstractions,
- analytics interfaces,
- routing primitives,
- app lifecycle helpers,
- common result/error types,
- feature flag access interfaces,
- shared dependency registration helpers.

### Must not become
- a junk drawer for arbitrary shared code.

## 5.7 `packages/pilgrims_l10n`
Localization and textual resource package.

### Responsibilities
- ARB or equivalent localization resources,
- generated localization glue,
- locale configuration,
- shared text conventions where centralized.

### Must not contain
- product logic,
- feature state,
- styling.

## 5.8 `packages/pilgrims_testkit`
Test support package.

### Responsibilities
- test fixtures,
- fake repositories,
- golden-test helpers,
- widget harnesses,
- integration-test support helpers,
- deterministic clocks or environment stubs.

---

# 6. If a single-package app is chosen instead

A package-oriented monorepo is recommended, but if the team intentionally chooses a single app package at first, the internal structure must still mimic strong package boundaries.

## 6.1 Required internal top-level `lib/` structure
```text
lib/
  app/
  core/
  design_system/
  platform/
  features/
  l10n/
```

## 6.2 Internal equivalents
- `app/` ≈ app shell and bootstrap
- `core/` ≈ shared non-UI infrastructure
- `design_system/` ≈ tokens/themes/components
- `platform/` ≈ bridge wrappers
- `features/` ≈ feature-family modules
- `l10n/` ≈ localization entry points

## 6.3 Rule
Even in a single-package structure, feature code must behave as if package boundaries exist.

---

# 7. Layering model inside the Flutter app

Each feature-family module should follow a consistent layered model.

## 7.1 Recommended feature module layers
```text
feature_x/
  presentation/
  application/
  domain/
  data/
```

## 7.2 Presentation layer
### Responsibilities
- screens,
- widgets,
- view composition,
- state rendering,
- navigation triggers,
- accessibility implementation,
- localized copy usage,
- consuming design-system components.

### Must not do
- direct HTTP calls,
- direct SQL/storage calls,
- direct map provider SDK calls unless that widget belongs to a dedicated adapter boundary,
- business rules that belong in application/domain layers,
- hardcoded repeated visual values.

## 7.3 Application layer
### Responsibilities
- view models/controllers/notifiers,
- orchestration of use cases,
- UI-facing state transitions,
- coordination between repositories and presentation,
- feature-local policies not belonging in shared domain.

### Must not do
- render widgets,
- directly know storage implementation details,
- directly style UI.

## 7.4 Domain layer
### Responsibilities
- feature entities,
- business rules,
- validation,
- use-case contracts,
- value objects,
- domain-level invariants.

### Must not do
- depend on Flutter UI types,
- know about provider SDKs,
- know about specific HTTP or database libraries.

## 7.5 Data layer
### Responsibilities
- repository implementations,
- DTO/entity mapping,
- storage/network adapters,
- cache and sync helpers,
- data-source composition.

### Must not do
- contain UI text or widget logic,
- invent domain semantics beyond mapping and source coordination.

---

# 8. Dependency direction rules

## 8.1 Allowed direction
The dependency flow should generally move in this direction:

```text
presentation -> application -> domain
presentation -> application -> repository interfaces
application -> domain
application -> repository interfaces
repository implementations -> local/remote/platform data sources
feature modules -> shared core/design system/platform abstractions
```

## 8.2 Forbidden direction
The following are forbidden unless explicitly approved:
- design system depending on feature modules,
- domain layer depending on Flutter widgets,
- one feature depending directly on another feature’s presentation layer,
- feature presentation depending directly on concrete data sources,
- feature modules depending directly on generated platform code without an adapter,
- shared core depending on product-specific feature implementations.

## 8.3 Cross-feature dependencies
When one feature needs behavior from another, prefer one of these:
- shared domain contract,
- shared core service,
- event/callback abstraction,
- route or deep-link invocation,
- composition at the app-shell layer.

Do not import another feature’s internal implementation just because it is convenient.

---

# 9. Feature-family module boundaries

The app should follow the same major feature families defined in the documentation system.

## 9.1 Canonical feature-family modules
- rituals_ric_content
- maps_wayfinding
- group_coordination
- planner_personal_tools
- phrasebook_emergency_safety
- offline_packs_content
- account_entitlements_settings
- onboarding_home_simple_mode
- content_governance_runtime

## 9.2 Why feature-family grouping is preferred
This keeps modules large enough to be coherent but small enough to remain bounded.

It also aligns better with:
- the product spec structure,
- AI-agent navigation,
- shared domain behavior,
- reduced cross-feature imports.

## 9.3 Module ownership rule
Each feature-family module should own:
- its screens,
- its application-layer state machinery,
- its feature-specific domain objects,
- its feature-specific repository interfaces if not shared,
- its tests,
- its localized text keys where needed,
- its analytics event definitions where coordinated by the analytics architecture.

---

# 10. App shell architecture

## 10.1 App shell responsibilities
The app shell is the composition root for the Flutter application.

### Responsibilities
- bootstrap app config,
- initialize dependency graph,
- initialize localization,
- initialize theming,
- initialize route map,
- initialize top-level observers,
- handle app lifecycle integration,
- host global overlays and top-level error boundaries where relevant.

## 10.2 App shell must not
- host feature business logic,
- become a giant switchboard of ad hoc feature state,
- contain repeated styling definitions that belong in the design system,
- duplicate route logic already defined centrally.

---

# 11. State management architecture

This file defines the architecture shape, not a hard ideological commitment to one state-management package. However, the project must choose one primary state-management approach and apply it consistently.

## 11.1 Required state management properties
The chosen approach must support:
- testable state containers,
- predictable dependency injection,
- separation between UI and business orchestration,
- async state handling,
- offline/cache-aware workflows,
- modular feature ownership,
- good debuggability.

## 11.2 Recommended state layering
- ephemeral UI state should stay close to widgets when local and trivial,
- feature state should live in application-layer controllers/view models/notifiers,
- shared long-lived state should be exposed through shared services or repository-backed models,
- no hidden mutable global state outside controlled top-level services.

## 11.3 State ownership rule
Every significant state object must have a clear owner.

Examples:
- screen-local state → screen/controller,
- feature workflow state → feature application layer,
- account/entitlement snapshot → app/core account service or repository-backed controller,
- pack inventory → offline packs module service.

## 11.4 State naming rule
State-holder names should reflect purpose, not implementation trend.

Examples:
- `RitualFlowController`
- `GroupHubViewModel`
- `PackInventoryService`

Not vague examples:
- `DataManager`
- `HelperState`
- `LogicProvider`

---

# 12. Dependency injection architecture

## 12.1 Requirement
Dependencies must be assembled centrally and exposed explicitly.

## 12.2 Composition root rule
The composition root must live in the app shell or a dedicated bootstrap layer, not scattered across random features.

## 12.3 DI design goals
DI should make it easy to:
- swap implementations in tests,
- keep repository contracts explicit,
- avoid hidden singleton sprawl,
- control lifecycle clearly.

## 12.4 DI anti-patterns
Forbidden:
- reaching into a global service locator from arbitrary deep widget code without discipline,
- registering hidden mutable singletons ad hoc,
- constructing repositories directly inside feature widgets,
- mixing multiple incompatible DI approaches chaotically.

---

# 13. Repository architecture

## 13.1 Repository role
Repositories are the application-facing source of truth abstraction for domain data and behavior.

## 13.2 Repository responsibilities
Repositories should:
- expose stable domain-focused APIs,
- coordinate local and remote sources,
- manage cache policy and sync logic,
- hide transport/storage implementation details,
- expose domain entities rather than raw transport DTOs wherever practical.

## 13.3 Repository boundaries
UI and application layers must depend on repository interfaces or stable repository contracts, not on raw database, HTTP, or provider SDK calls.

## 13.4 Repository ownership examples
- ritual content repository
- map anchor repository
- group repository
- entitlement repository
- pack catalog repository
- notes/bookmarks repository

## 13.5 Repository anti-patterns
Forbidden:
- monolithic “app repository” classes,
- repositories returning random UI models,
- repositories mixed with widget code,
- repositories bypassing local-first rules without explicit reason.

---

# 14. Data-source architecture inside Flutter

## 14.1 Local data sources
Examples:
- local SQL/NoSQL database adapters,
- secure storage adapters,
- local preferences/settings storage,
- pack metadata store,
- offline content snapshot store.

## 14.2 Remote data sources
Examples:
- API clients,
- realtime adapters,
- manifest fetchers,
- receipt-validation client wrappers.

## 14.3 Provider/native data sources
Examples:
- map provider adapter,
- BLE adapter,
- notification scheduler adapter,
- store bridge adapter.

## 14.4 Rule
Data sources should be implementation details beneath repositories or controlled services. Feature modules must not talk to them directly unless the module itself is the adapter boundary.

---

# 15. Navigation architecture

## 15.1 Central route ownership
Route definitions, route naming, and deep-link entry points must be centralized.

## 15.2 Feature navigation rule
Features may declare their route contracts, but app-shell integration should remain centralized.

## 15.3 Navigation anti-patterns
Forbidden:
- magic string routes invented per widget,
- inconsistent route argument patterns,
- direct navigation to another feature’s private internal screen structure,
- embedding route-building logic in many unrelated widgets.

## 15.4 Critical-flow rule
Priority flows such as ritual guidance, emergency tools, map wayfinding, and Simple Mode entry points must have predictable and stable routing paths.

---

# 16. Design-system architecture in Flutter

## 16.1 Design-system ownership
`packages/pilgrims_design_system` (or its approved single-package equivalent) owns the canonical Pilgrims Soft Surface implementation.

It owns:
- foundation tokens,
- semantic Light/Dark token mappings,
- component tokens,
- depth/effect presets,
- typography roles and fallbacks,
- shared component styling,
- platform-adaptation hooks.

## 16.2 Centralized theming rule
The app must construct complete Light and Dark themes centrally. The app shell owns appearance selection with exactly three user-facing modes:
- System,
- Light,
- Dark.

System is the recommended default. The selection is local-only, available to guests, non-entitled, network-independent, applied immediately, and persisted across restart.

## 16.3 Appearance state ownership
Appearance state belongs at the app-shell/design-system boundary, not inside feature modules.

Changing appearance must:
- not recreate navigation state,
- not reset active feature flows,
- not change Simple Mode semantics,
- not change entitlement, auth, offline, or protected-data truth.

## 16.4 Style application rule
Feature widgets consume semantic or component roles through Flutter theme access and approved `ThemeExtension`-style APIs. They must not consume raw Figma variable names, raw primitive palette names, or platform-specific effect constants directly.

## 16.5 Local override rule
A local visual override is allowed only when it expresses a documented semantic state that cannot be represented by the shared component contract. Repeated overrides must be promoted into the design system.

## 16.6 Forbidden styling behaviors
Forbidden:
- hardcoded repeated colors, spacing, radii, shadows, highlights, glows, or animation values in feature widgets,
- per-screen Light/Dark logic,
- feature-level `ThemeMode` ownership,
- checking platform/theme values only to fork visual identity,
- copying Figma-generated reference code directly into Flutter architecture,
- creating raw multi-shadow stacks in dense/repeated lists when a performance-safe effect tier exists.

# 17. Text and localization architecture

## 17.1 Localization rule
User-facing strings must be localized through the centralized localization system unless a string is explicitly non-localized by design.

## 17.2 No inline reusable copy
Repeated or meaningful user-facing copy must not be hardcoded repeatedly in widget files.

## 17.3 Translation ownership
Localization resources should be structured so feature ownership remains clear.

Recommended grouping:
- common/shared strings,
- feature-family strings,
- settings/account strings,
- error/offline/loading patterns.

## 17.4 RTL rule
Widgets and layouts must rely on direction-aware APIs and tokens rather than manual left/right hacks where possible.

---

# 18. Asset architecture

## 18.1 Asset categories
Assets must be organized by type and purpose.

Recommended categories:
- icons
- illustrations
- bundled audio
- bundled map fallback assets
- emergency visuals
- onboarding visuals
- lottie/animation assets if used
- typography/font assets

## 18.2 Downloaded vs bundled separation
Bundled assets and downloaded pack assets must be treated as different systems.

## 18.3 Asset folder rule
Asset directories should remain predictable and stable. Avoid feature-specific miscellaneous folders with overlapping asset meanings.

## 18.4 Asset naming rule
Asset names should reflect purpose and be searchable, not depend on transient design iteration names.

---

# 19. Platform bridge boundaries

## 19.1 Platform-sensitive capabilities
These capabilities must be isolated through dedicated bridge abstractions:
- purchases and restore flows,
- notifications,
- location permissions and location access,
- BLE/positioning,
- advanced map rendering capabilities,
- device capability and permission checks,
- file-system/storage capability checks where needed.

## 19.2 Bridge rule
Feature modules should depend on platform-agnostic interfaces wherever practical.

## 19.3 Bridge anti-patterns
Forbidden:
- platform channel code hidden inside feature widget files,
- direct platform API calls scattered across modules,
- bypassing bridge abstractions “just for one screen.”

---

# 20. Error and result handling architecture

## 20.1 Consistent result model
The app should use a consistent pattern for representing:
- success,
- empty,
- retryable failure,
- terminal failure,
- permission-related failure,
- offline/degraded state.

## 20.2 Translation rule
Low-level transport or storage errors should be translated into domain/application-friendly failures before reaching presentation.

## 20.3 Presentation rule
UI should render user-appropriate states rather than exposing raw exceptions.

---

# 21. Feature flag and configuration access

## 21.1 Access boundary
Feature flags and runtime configuration should be accessed through shared app-core/config services, not through ad hoc HTTP fetches from screens.

## 21.2 Caching rule
Feature code should consume resolved config state, not reimplement cache logic independently.

## 21.3 Anti-pattern
Do not sprinkle flag key strings across many feature widgets.

---

# 22. Pack manager boundary

## 22.1 Ownership
Pack discovery, download state, verification state, install state, and pack inventory should live behind a dedicated pack manager service or repository.

## 22.2 UI integration rule
Feature screens may render pack state, but must not implement download pipeline logic themselves.

## 22.3 Anti-pattern
Do not let each feature invent its own download/integrity logic.

---

# 23. Map runtime boundary inside Flutter

## 23.1 Rule
Most feature code must not talk directly to map SDKs.

## 23.2 Allowed map boundaries
- dedicated map adapter widgets,
- dedicated map services/controllers,
- domain-safe interfaces for anchors, routes, destinations, and positioning state.

## 23.3 Why this matters
This prevents:
- provider lock-in leaking through the app,
- rendering and business logic becoming tangled,
- difficult future migration or fallback behavior.

---

# 24. Suggested internal structure for each feature-family module

Example:

```text
features/maps_wayfinding/
  presentation/
    screens/
    widgets/
    controllers/
    states/
  application/
    use_cases/
    coordinators/
  domain/
    entities/
    value_objects/
    policies/
    repositories/
  data/
    repositories/
    datasources/
    models/
    mappers/
  analytics/
  tests/
```

## 24.1 Rule
Exact names may vary slightly, but the separation of responsibility must remain clear.

---

# 25. Naming conventions inside the Flutter codebase

## 25.1 Widget names
Name widgets by role or purpose, not by temporary visual appearance.

Good examples:
- `EmergencyShortcutCard`
- `RitualStepPanel`
- `GroupMemberStatusTile`

Weak examples:
- `PrettyBox`
- `NewGlassThing`
- `CustomWidget2`

## 25.2 Controller/view model names
Should reflect owned state or workflow.

Good examples:
- `OnboardingFlowController`
- `PackCatalogViewModel`
- `SaveGateController`

## 25.3 Repository names
Should reflect domain meaning.

Good examples:
- `GroupRepository`
- `EntitlementRepository`
- `RitualContentRepository`

## 25.4 File naming
Use stable, searchable naming that matches the class or primary content.

---

# 26. Testing architecture inside the Flutter repo

## 26.1 Test locality rule
Tests should live close enough to feature ownership that module accountability is clear.

## 26.2 Recommended test buckets
- unit tests for domain/application logic,
- widget tests for state rendering and interaction,
- integration tests for feature flow boundaries,
- golden tests for selected high-risk UI surfaces,
- platform or device tests for native-bridge-heavy behaviors.

## 26.3 Test utility rule
Reusable test harnesses and fakes should live in shared testkit utilities, not be copy-pasted across feature folders.

---

# 27. Code generation boundaries

## 27.1 Allowed generation areas
Examples:
- localization generation,
- JSON/data model generation if used,
- route generation if chosen consistently,
- freezed/sealed model generation if chosen consistently.

## 27.2 Rule
Generated files must be:
- predictable,
- reproducible,
- clearly marked,
- excluded from hand-edit expectations.

## 27.3 Anti-pattern
Do not design architecture that depends on opaque generated magic few contributors understand.

---

# 28. Environment and flavor architecture

## 28.1 Environment support
The Flutter app must support at least:
- development,
- staging/test,
- production.

## 28.2 Configuration rule
Environment-specific values must be injected through controlled configuration layers, not hardcoded into feature files.

## 28.3 Flavor rule
Branding, endpoints, logging levels, and feature toggles that vary by environment must be managed centrally.

---

# 29. AI-agent-specific implementation guardrails

## 29.1 Before editing Flutter code, an AI agent must inspect
- app shell bootstrap,
- design-system package/module,
- relevant feature-family module,
- repository interface used by the feature,
- localization keys,
- route definitions,
- existing tests for the area.

## 29.2 AI agents must not
- create a new shared utility without checking if one already exists,
- hardcode repeated style values,
- bypass repository interfaces,
- couple two feature modules tightly without approval,
- add random helper files in arbitrary folders,
- create duplicated component variants because the design system was not inspected first.

## 29.3 When confused
The agent must prefer:
- searching existing shared abstractions,
- reading the relevant architecture/design-system files,
- asking for clarification when the boundary is truly unclear.

---

# 30. Recommended bootstrap sequence for implementation

## 30.1 First build the architectural spine
Before broad feature implementation, establish:
- app shell,
- dependency injection wiring,
- design-system package/module,
- localization setup,
- repository abstractions,
- pack manager abstraction,
- config/flags access layer,
- platform bridge scaffolding.

## 30.2 Then build critical feature families
Recommended order:
1. onboarding_home_simple_mode
2. rituals_ric_content
3. phrasebook_emergency_safety
4. maps_wayfinding baseline
5. planner_personal_tools baseline
6. account_entitlements_settings baseline
7. offline_packs_content
8. group_coordination
9. advanced maps refinement

## 30.3 Why this order
It reduces risk by:
- getting the shell and design system right first,
- ensuring core local-first value exists early,
- preventing map and group complexity from destabilizing the architecture too early.

---

# 31. Recommended example app-package layout

If using the recommended package-oriented monorepo, the main app package may look like this:

```text
apps/pilgrims_mobile_app/
  lib/
    main.dart
    bootstrap/
    app/
      app.dart
      router/
      guards/
      observers/
    features/
      rituals_ric_content/
      maps_wayfinding/
      group_coordination/
      planner_personal_tools/
      phrasebook_emergency_safety/
      offline_packs_content/
      account_entitlements_settings/
      onboarding_home_simple_mode/
    composition/
    platform_entry/
  test/
  integration_test/
  assets/
```

## 31.1 Rule
The app package should compose feature modules and shared packages; it should not re-own what shared packages already own.

---

# 32. Anti-patterns forbidden by this Flutter architecture

The following are forbidden unless explicitly approved.

## 32.1 Hardcoded repeated colors, text styles, spacing, shadows, blur, or animation values in feature widgets
Forbidden.

## 32.2 Feature widgets calling HTTP clients or local database adapters directly
Forbidden.

## 32.3 Random “utils” dumping grounds
Forbidden.

## 32.4 Deep cross-feature imports into another feature’s internal folders
Forbidden.

## 32.5 Route strings scattered across unrelated files
Forbidden.

## 32.6 Platform-channel code embedded in UI widgets
Forbidden.

## 32.7 Shared component duplication because the design system was not checked first
Forbidden.

## 32.8 Massive god classes such as `AppManager`, `DataManager`, or `HelperService`
Forbidden.

## 32.9 Feature-specific copy hardcoded inline across multiple widgets
Forbidden.

## 32.10 Building UI styling around visual trends instead of the centralized theme system
Forbidden.

---

# 33. When this file must be updated

This file must be updated when any of the following changes:
- package strategy,
- monorepo/single-package decision,
- feature-family boundaries,
- dependency direction rules,
- state management architecture,
- DI approach,
- repository/data-source layering rules,
- route ownership strategy,
- design-system implementation boundary,
- localization structure,
- asset structure,
- platform bridge strategy,
- testing structure,
- environment/flavor setup.

If any of these change but this file is not updated, AI-agent reliability and codebase maintainability will degrade quickly.

---

# 34. Summary

This file defines how the Flutter codebase must be structured.

It establishes:
- the recommended package-oriented repository shape,
- the responsibilities of each shared package,
- the layered structure of feature-family modules,
- the dependency direction rules,
- the app-shell and DI boundaries,
- the repository and data-source architecture,
- the centralized design-system boundary,
- the localization, asset, navigation, and platform-bridge rules,
- the anti-patterns that must be prevented.

This architecture is designed to keep the app:
- scalable,
- maintainable,
- visually consistent,
- offline-capable,
- and safe for long-term AI-assisted development.

