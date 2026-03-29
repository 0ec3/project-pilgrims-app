# 09 — PLATFORM SPEC, IOS LIQUID GLASS, ANDROID ADAPTATION, AND NATIVE BRIDGES

## Document status
- **Type:** Normative platform adaptation and native-boundary document
- **Priority:** Highest
- **Audience:** Flutter engineers, iOS engineers, Android engineers, design lead, QA, AI coding agents, reviewer agents
- **Purpose:** Define how the shared product and design system must adapt to iOS and Android, how Liquid Glass should be applied on Apple platforms, how Android should remain platform-appropriate without forced imitation, and how native capabilities must be exposed through controlled bridge interfaces.
- **Authority level:** This file is the canonical source of truth for platform-specific UX adaptation, native-bridge boundaries, permission behavior, asset-delivery platform differences, store platform differences, and when platform divergence is allowed or required.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `06-SYSTEM-ARCHITECTURE.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `16-MAP-ARCHITECTURE-POSITIONING-ROUTING-3D-AND-OFFLINE-WAYFINDING.md`
- **Related files:** `10`, `11`, `12`, `14`, `17`, `18`–`25`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This file exists because platform differences in this project are not cosmetic details. They affect:
- visual system behavior,
- interaction patterns,
- motion,
- asset delivery,
- store entitlements,
- permissions,
- notifications,
- map rendering,
- BLE and positioning,
- testing and release behavior.

Without a dedicated platform spec, teams and AI agents often make one of two mistakes:
- they force the same behavior everywhere and create a product that feels wrong on one platform,
- or they let platform-specific improvisation spread until the app becomes two disconnected products.

This file prevents both mistakes.

It defines:
- what must remain shared,
- what may differ by platform,
- how iOS Liquid Glass should be applied,
- how Android should adapt without imitation,
- how native functionality must be isolated behind stable bridges,
- which platform-specific technical choices are implementation details versus product-level differences.

---

# 2. Platform philosophy

## 2.1 One product, two native expressions
The app should feel like one product with one product logic, one information architecture, one ethical boundary, and one feature set where possible.

## 2.2 Shared product core
These must remain aligned across iOS and Android unless a future decision explicitly changes them:
- product scope
- feature families
- data model semantics
- API contracts
- entitlement rules
- offline-first behavior
- map-domain behavior
- accessibility intent
- terminology

## 2.3 Platform-appropriate expression
These may adapt by platform:
- navigation chrome treatment
- material/surface expression
- motion feel
- control styling
- modal presentation style
- certain native permission or settings flows
- implementation of bridges to stores, notifications, asset delivery, maps, BLE, and platform services

## 2.4 Anti-imitation rule
Android must not become a visual clone of iOS. iOS must not be reduced to generic Material styling. The app should use shared semantics with platform-appropriate expression. Flutter’s adaptive guidance explicitly supports platform-specific adaptations rather than assuming all design choices are automatic. ([docs.flutter.dev](https://docs.flutter.dev/ui/adaptive-responsive/platform-adaptations))

---

# 3. Platform scope categories

Every cross-platform behavior should be classified into one of the following categories.

## 3.1 Category A — Shared invariant
Must behave the same conceptually on all platforms.

Examples:
- who can join a group
- what a supporter entitlement means
- what Save My Gate does
- what counts as a regroup pin
- what content is offline-capable

## 3.2 Category B — Shared semantics, different presentation
Same meaning, different native expression.

Examples:
- top bar treatment
- bottom navigation/tab chrome
- modal sheet presentation
- map overlay controls
- list row density or interaction feel

## 3.3 Category C — Platform-specific technical implementation
Same product behavior, different native plumbing.

Examples:
- store purchase bridges
- local notifications implementation
- BLE APIs
- asset delivery mechanisms
- map SDK/native integration

## 3.4 Category D — Platform-only behavior by necessity
Rare. Allowed only where platform APIs or store rules force it.

Examples:
- family-sharing nuance surfaced differently per store/platform
- iOS-specific material adaptation details
- Android-specific permission granularity or device settings affordances

---

# 4. Shared platform invariants

The following are non-negotiable across iOS and Android.

## 4.1 Product invariants
- Umrah-first scope
- core rituals and RIC behavior
- ethical monetization boundary
- offline-first essential value
- privacy-light posture
- no passive hidden tracking
- Simple Mode as a supported product capability

## 4.2 Data and contract invariants
- same canonical entity meanings
- same API contract shapes
- same pack lifecycle semantics
- same route graph semantics
- same entitlement gate meanings
- same group-role meanings

## 4.3 UX invariants
- critical flows remain reachable
- important actions remain obvious
- readability takes priority over style
- emergency and safety content remains strong-contrast and low-friction
- the app must still degrade clearly under offline or low-confidence map conditions

---

# 5. Platform adaptation categories in detail

## 5.1 Navigation chrome
Same navigation meaning, platform-adapted surface and motion.

## 5.2 Control surfaces
Buttons, chips, overlays, sheets, and bars may adapt shape/material/motion while preserving semantic roles.

## 5.3 Modal and sheet presentation
Must follow shared information hierarchy, but may use iOS-appropriate or Android-appropriate presentation patterns.

## 5.4 Map overlays
Map overlay controls may use stronger glass/material treatment on iOS and stronger elevated/material surfaces on Android, but route clarity and tap reliability remain the same requirement.

## 5.5 Permission prompts and settings handoff
Must respect native permission models and platform-specific settings affordances.

---

# 6. iOS adaptation strategy

## 6.1 iOS design goals
On iOS, the app should feel:
- refined,
- calm,
- modern,
- structurally aligned with Apple platform expectations,
- visually layered without reducing clarity.

## 6.2 iOS-specific design direction
Apple’s current guidance frames Liquid Glass as a system material to adopt thoughtfully, especially in standard components, bars, and controls, rather than as indiscriminate translucency over all content. ([developer.apple.com](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass))

## 6.3 Liquid Glass usage rule on iOS
Liquid-Glass-like treatment is allowed where it improves hierarchy and premium feel without harming readability.

### Preferred zones
- top bars / navigation chrome
- bottom bars / tab bars
- map overlay control clusters
- contextual floating action trays
- lightweight modal headers
- selected chip/filter surfaces

### Discouraged or forbidden zones
- long-form ritual text
- dense instructions
- safety-critical alerts
- emergency sheets/cards
- dense settings forms
- any surface where transparency lowers comprehension

## 6.4 iOS structural behavior
Where appropriate, iOS should favor:
- more fluid material transitions
- stronger sense of layered chrome
- modal presentation that feels native to iOS hierarchy
- motion that feels cohesive with system conventions

## 6.5 Accessibility rule on iOS
When system settings such as Reduce Transparency or higher contrast are active, glass/material surfaces must degrade to stronger solid surfaces while preserving hierarchy and affordance. Apple explicitly notes that Liquid Glass adapts with accessibility settings such as Reduce Transparency and Increase Contrast. ([developer.apple.com](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass))

---

# 7. Android adaptation strategy

## 7.1 Android design goals
On Android, the app should feel:
- calm,
- clear,
- premium,
- fast,
- natural within Android conventions.

## 7.2 Android expression rule
Android should use the shared semantic design system with platform-appropriate elevated/material surfaces rather than imitating Apple’s Liquid Glass literally.

## 7.3 Android structural behavior
Android may favor:
- stronger solid/elevated surfaces
- Android-appropriate navigation transitions
- Material-adjacent control behavior where it supports usability
- clearer emphasis on contrast and tactile feedback in critical controls

## 7.4 Android visual differentiation rule
The product identity remains shared, but Android is allowed to express it through:
- different surface treatment
- different transition feel
- Android-appropriate haptic or system-integration expectations

## 7.5 Accessibility rule on Android
The Android experience must preserve high contrast, large text support, reduced motion handling, and robust focus/touch target behavior independent of any visual adaptation differences.

---

# 8. Shared design system vs platform adaptation boundary

## 8.1 Shared design system owns
- semantic color roles
- text roles
- spacing roles
- shape/radius families
- motion token families
- component meanings
- content hierarchy
- accessibility requirements

## 8.2 Platform adaptation layer owns
- how those semantics are rendered per platform
- which material treatment variant is used
- bar and overlay presentation differences
- transition selection by platform
- native integration-specific visual affordances

## 8.3 Feature module rule
Feature modules must consume platform-adapted shared components or theme extensions, not hand-roll platform differences per screen.

---

# 9. Native bridge philosophy

## 9.1 Native code should be deliberate and bounded
Native bridges exist to expose platform capabilities that Flutter alone should not directly own or that require platform-specific performance and APIs.

## 9.2 Bridge goals
Native bridges must:
- expose stable APIs to Flutter
- isolate provider/platform details
- support testing and mocking
- keep product semantics in Dart/domain layers where possible
- reduce plugin sprawl and random direct platform channel usage

## 9.3 Bridge anti-goal
Do not put product business rules in native bridge code unless the rule is inherently platform-native and documented.

## 9.4 Preferred bridge style
Use typed, explicit bridge contracts. Flutter’s platform integration guidance and plugin/package guidance support typed platform-channel or generated-interface approaches instead of ad hoc channel strings scattered through the app. ([docs.flutter.dev](https://docs.flutter.dev/platform-integration/platform-channels))

---

# 10. Canonical native bridge catalog

The following bridge surfaces are considered canonical for this project.

## 10.1 `StoreBridge`
Purpose:
- initiate purchase
- retrieve platform purchase references
- restore transaction state when appropriate
- return normalized purchase data to trusted backend flows

### Rule
Bridge returns platform-native purchase references/status, but trusted entitlement truth still comes from backend validation.

## 10.2 `NotificationsBridge`
Purpose:
- request notification permissions
- schedule local reminders
- cancel/update local reminders
- inspect notification capability state where needed

### Rule
Reminder semantics remain shared; scheduling implementation is platform-specific.

## 10.3 `LocationBridge`
Purpose:
- request location permission
- retrieve coarse/fine location state as permitted
- surface service enabled/disabled state

### Rule
Location bridge does not define routing or navigation behavior; it only exposes platform location capability.

## 10.4 `BluetoothBridge`
Purpose:
- request BLE-related permissions
- scan or range beacons if supported
- surface BLE availability and permission state

### Rule
BLE support must be optional and confidence-aware.

## 10.5 `MapBridge`
Purpose:
- expose provider-native rendering and performance-sensitive map functionality
- surface camera operations if provider-specific optimizations are required
- host native map view wrappers when necessary

### Rule
Map domain truth stays in shared map architecture; bridge only provides platform/provider capabilities.

## 10.6 `AssetDeliveryBridge`
Purpose:
- expose any platform-specific asset-delivery services beneath the pack manager abstraction
- query download capability/state if needed
- surface lifecycle events when platform-managed delivery is used

### Rule
The Flutter pack manager should not care whether the platform uses app-managed downloads or system-backed asset delivery, only whether the pack is installed and verified.

## 10.7 `SystemCapabilitiesBridge`
Purpose:
- query reduced transparency / reduced motion / contrast preferences if needed
- query background task capability or other platform-specific capabilities
- query system adaptation flags used in platform rendering decisions

---

# 11. Bridge contract design rules

## 11.1 Shared Dart-facing API first
Each bridge must expose a stable Dart-facing interface owned by shared platform or app-core layers.

## 11.2 Typed payloads only
Bridge payloads must use typed models or generated typed interfaces, not loosely structured maps sprinkled across feature code.

## 11.3 One bridge, one responsibility family
Do not create giant “NativeBridge” or “SystemManager” interfaces that mix unrelated concerns.

## 11.4 No direct feature-widget channel access
Feature widgets and screens must not call platform channels directly.

## 11.5 Mockability rule
Every bridge must be mockable for tests.

---

# 12. Store and entitlement platform differences

## 12.1 Shared product meaning
The product-level meaning of `FREE` and `SUPPORTER` must remain shared across platforms.

## 12.2 Platform purchase differences
Purchase initiation, receipt shape, restoration details, and family-related behavior may differ between stores.

## 12.3 Bridge vs backend rule
- native bridge handles purchase initiation and local platform transaction access
- backend validates and normalizes purchase state
- Flutter receives normalized entitlement state

## 12.4 Family-sharing rule
Do not assume identical family-sharing behavior between Apple and Google. The platform UI may need different explanatory wording while the normalized entitlement contract stays consistent.

---

# 13. Asset-delivery platform differences

## 13.1 Shared product contract
The product contract remains:
- manifest discovery
- download/acquisition
- verification
- install state
- purgeability
- pack-manager ownership

## 13.2 iOS asset-delivery rule
Apple’s current direction introduces Background Assets and Apple-hosted background asset flows as the modern asset-distribution path. Therefore iOS architecture must not hardwire older On-Demand Resources assumptions into the app contract. ([developer.apple.com](https://developer.apple.com/documentation/BackgroundAssets))

## 13.3 Android asset-delivery rule
Android may use app-managed downloads or platform-assisted delivery beneath the same abstraction.

## 13.4 User-experience rule
Regardless of platform, the user should see the same semantic pack states:
- not installed
- downloading
- verifying
- installed
- failed
- purged

---

# 14. Notification and reminder platform differences

## 14.1 Shared product contract
Reminders are local and must work offline from local scheduled state.

## 14.2 Platform implementation differences
Permission flows, scheduling APIs, and edge-case delivery behavior differ by platform and must be handled in the bridge layer.

## 14.3 UX rule
The product should explain reminder availability in shared language while respecting platform-specific permission timing and settings affordances.

---

# 15. Location and BLE permission differences

## 15.1 Shared product contract
The map subsystem may use location or BLE to improve orientation, but the app must still provide useful fallback behavior if permissions are denied.

## 15.2 Platform variation rule
Permission prompts, rationale flows, and settings redirection may differ between iOS and Android.

## 15.3 UX rule
Do not create platform-inappropriate pre-prompt behavior. Permission education should remain short, respectful, and tied to real user value.

## 15.4 No-dependency rule
The product must not become unusable simply because location or BLE permission was denied.

---

# 16. Map rendering platform differences

## 16.1 Shared map semantics
Route graph, anchors, floors, regroup references, and confidence states remain shared.

## 16.2 Platform implementation differences
The rendering engine, native wrappers, and performance-sensitive hooks may differ by platform.

## 16.3 3D rule
3D behavior may be tuned per platform based on SDK capability, device performance, and rendering constraints, but route meaning and fallback behavior must remain aligned.

## 16.4 Feature rule
Feature modules must not care whether the map is implemented with one native view path or another.

---

# 17. Navigation, bars, and modal adaptation

## 17.1 Shared information architecture
The app uses one information architecture.

## 17.2 iOS chrome guidance
- tab and top chrome may lean into material/glass treatment
- modal and sheet hierarchy should feel native to iOS
- transitions should feel fluid and cohesive

## 17.3 Android chrome guidance
- bars and navigation should use stronger material/elevated surfaces
- transitions should feel Android-appropriate and efficient
- modal patterns should remain familiar to Android users

## 17.4 Shared semantics rule
A primary action is still primary, a destructive action is still destructive, and emergency surfaces remain high priority on both platforms.

---

# 18. Platform-specific accessibility rules

## 18.1 Shared accessibility contract
Both platforms must support:
- larger text
- high contrast
- reduced motion handling
- direction-aware layout
- screen-reader accessible semantics
- practical touch targets

## 18.2 iOS-specific accessibility adaptation
Respect platform accessibility states that materially affect material rendering, especially reduced transparency and increased contrast. Apple explicitly ties Liquid Glass behavior to these accessibility settings. ([developer.apple.com](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass))

## 18.3 Android-specific accessibility adaptation
Respect platform text scaling, contrast, talkback/navigation, and input-mode differences without requiring separate product logic.

---

# 19. Testing strategy by platform

## 19.1 Shared tests
- product behavior tests
- shared repository/domain tests
- API contract tests
- local persistence tests
- pack state machine tests

## 19.2 iOS-specific tests
- Liquid Glass / material fallback behavior with accessibility settings
- Background Assets or iOS asset-delivery integration behavior if used
- store purchase bridge behavior
- map native wrapper behavior on supported iOS versions
- notification scheduling and permission flows

## 19.3 Android-specific tests
- Android surface adaptation behavior
- asset-delivery/download integration behavior
- Play purchase bridge behavior
- notification permission/scheduling differences by OS version
- map native wrapper behavior across representative devices

## 19.4 Bridge tests
Every bridge must have:
- interface-level Dart tests where possible
- mock/fake tests
- platform-specific integration tests for critical paths

---

# 20. Release and support matrix guidance

## 20.1 Supported OS matrix
The exact minimum supported versions must be defined in release planning and testing documents, but this file requires that platform adaptation and native bridge strategy be validated against the intended support matrix before locking implementation choices.

## 20.2 Capability variability rule
Not every supported device will have equal:
- BLE reliability
- 3D rendering capability
- storage performance
- notification behavior
- battery tolerance

The app must degrade by capability rather than failing unpredictably.

---

# 21. Platform QA scenarios

## 21.1 iOS QA must include
- material/glass fallback under Reduce Transparency
- high-contrast and larger-text checks
- map overlays with glass chrome and route readability
- asset download/install behavior through the chosen iOS asset path
- restore purchase and entitlement refresh

## 21.2 Android QA must include
- elevated/material adaptation consistency
- larger-text and talkback checks
- low-end device performance checks
- download/install behavior through the chosen Android asset path
- purchase and restore behavior via Android flows

## 21.3 Shared QA must include
- no-permission location/BLE behavior
- pack install/purge/reinstall behavior
- emergency and safety readability
- Simple Mode cross-platform usability
- map fallback when 3D or precise positioning is unavailable

---

# 22. Recommendations adopted into this platform spec

## 22.1 Recommendation — controlled Liquid Glass on iOS only where structurally appropriate
The platform spec now explicitly limits glass-heavy treatment to bars, overlays, and selected chrome instead of dense content blocks.

## 22.2 Recommendation — Android adaptation without imitation
Android now explicitly uses shared semantics with platform-appropriate material/elevated expression rather than a forced iOS clone.

## 22.3 Recommendation — native bridges as typed interfaces, not scattered channels
All platform integrations are now defined through dedicated bridge families with explicit ownership.

## 22.4 Recommendation — asset delivery remains abstracted from the product contract
The file keeps Background Assets / app-managed downloads / Android delivery mechanisms beneath the same pack-manager abstraction.

## 22.5 Recommendation — platform differences are explicit categories
This prevents hidden divergence while still allowing necessary native behavior.

---

# 23. Anti-patterns forbidden by this platform spec

The following are forbidden unless explicitly approved.

## 23.1 Applying Liquid Glass indiscriminately to dense or critical content
Forbidden.

## 23.2 Forcing Android to visually mimic iOS materials everywhere
Forbidden.

## 23.3 Direct platform-channel usage inside feature widgets
Forbidden.

## 23.4 Giant all-purpose native bridges
Forbidden.

## 23.5 Letting platform-specific code define product business rules without documentation
Forbidden.

## 23.6 Requiring platform-only capabilities for baseline product usefulness
Forbidden.

## 23.7 Platform divergence that changes feature meaning without an approved decision
Forbidden.

## 23.8 Treating purchase success on device as equivalent to trusted entitlement success
Forbidden.

---

# 24. When this file must be updated

This file must be updated whenever any of the following changes:
- iOS adaptation rules
- Android adaptation rules
- Liquid Glass usage boundaries
- native bridge catalog
- store integration boundary
- asset-delivery platform implementation strategy
- map-native bridge strategy
- permission-flow strategy
- platform support matrix assumptions
- accessibility behaviors tied to system settings

If any of these evolve but this file is not updated, platform-specific behavior, QA, and Flutter implementation boundaries will drift quickly.

---

# 25. Summary

This file defines how Pilgrims Mobile App adapts to iOS and Android while preserving one product architecture.

It establishes:
- what remains shared across platforms
- what may adapt by platform
- how Liquid Glass is used on iOS
- how Android should express the product without imitation
- which native bridge families exist and what they own
- how platform-specific purchase, asset, notification, location, BLE, and map behaviors are isolated
- how platform QA and accessibility requirements should be enforced

Its purpose is to keep the app:
- native-feeling on both platforms
- visually coherent
- maintainable in Flutter
- and safe for long-term AI-assisted development without hidden platform drift.

