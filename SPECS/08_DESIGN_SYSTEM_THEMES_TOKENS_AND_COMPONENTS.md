# 08 — DESIGN SYSTEM, THEMES, TOKENS, AND COMPONENTS

## Document status
- **Type:** Normative design-system and Flutter implementation architecture document
- **Priority:** Highest
- **Audience:** Design lead, Flutter engineers, design-system engineers, QA, AI coding agents, reviewer agents
- **Purpose:** Define the canonical visual system of the app, the token architecture, theme architecture, component contracts, platform adaptation rules, accessibility requirements, and Flutter implementation boundaries so the app remains visually consistent, maintainable, and safe for AI-assisted development.
- **Authority level:** This file is the canonical source of truth for visual semantics, theme structure, token categories, component styling, and how UI styling must be implemented in Flutter. Feature modules and screens must not silently override this system.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `06-SYSTEM-ARCHITECTURE.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`
- **Related files:** `09`, `10`, `11`, `12`, `16`, `17`, `18`–`25`, `27`, `28`

---

# 1. Purpose of this file

This file defines how the app should look, feel, scale, and stay maintainable over time.

The canonical current visual language is **Pilgrims Soft Surface**. It is a project-owned system grounded in the approved current Figma direction and translated into reusable semantic contracts rather than copied as screenshot-specific styling.

Pilgrims Soft Surface is characterized by:
- mostly opaque canvas and card surfaces,
- calm rounded geometry,
- soft raised and inset depth,
- restrained outer shadows and inner highlights,
- controlled cyan/turquoise/blue accent and ambient glow,
- strong readable text and icon contrast,
- dimensional layering that remains subtle under stress,
- one shared product identity across iOS and Android.

The visual identity is **not** defined by transparency or blur. Soft-relief or neumorphic-inspired depth techniques may be used descriptively, but “Neumorphism” is not the canonical product/design-system name.

The approved Figma target is visual evidence, not product-behavior authority. It must not override product scope, feature names, IA, screen IDs, entitlement truth, localization, accessibility, offline guarantees, or governed religious meaning owned by other normative specs.

This file defines:
- design principles,
- Light/Dark appearance architecture,
- foundation, semantic, component, and appearance token layers,
- typography and multilingual fallback rules,
- surface/depth/effect rules,
- component families and states,
- accessibility requirements,
- platform adaptation boundaries,
- performance-safe implementation guidance,
- Flutter implementation boundaries.

# 2. Design-system goals

## 2.1 Calmness goal
The design system must produce interfaces that feel calm and focused rather than crowded, trendy, or noisy.

## 2.2 Readability goal
The system must prioritize text clarity and scannability, especially for ritual guidance, safety messages, and route instructions.

## 2.3 Maintainability goal
The system must let the team change visual behavior centrally through tokens, themes, and shared components rather than editing many screens manually. Material 3 explicitly treats design tokens as reusable building blocks that connect design and code, which aligns with this requirement. ([m3.material.io](https://m3.material.io/foundations/design-tokens))

## 2.4 Platform-adaptation goal
The system must support platform-specific adaptation while preserving one product identity. Flutter’s adaptive guidance distinguishes shared app architecture from platform-specific design choices, which supports this direction. ([docs.flutter.dev](https://docs.flutter.dev/ui/adaptive-responsive))

## 2.5 Accessibility goal
The system must support larger text, contrast needs, motion sensitivity, input diversity, and direction-aware layouts. Flutter’s accessibility and adaptive-input guidance explicitly emphasizes these needs. ([docs.flutter.dev](https://docs.flutter.dev/ui/adaptive-responsive/best-practices))

## 2.6 AI-agent safety goal
The system must reduce the chance that AI agents invent new styling patterns, duplicate components, or hardcode visual constants in feature code.

---

# 3. Design principles

## 3.1 Content first
User content, guidance, and actions are more important than decorative surface treatment.

## 3.2 Calm before expressive
The app may be polished and dimensional, but never at the expense of focus, readability, or confidence.

## 3.3 Semantic styling over raw values
Widgets must use semantic and component roles, not raw Figma values, palette names, arbitrary spacing, or copied shadow stacks.

## 3.4 Reuse before reinvention
If a visual pattern repeats or represents stable product behavior, it belongs in shared tokens/components rather than local screen styling.

## 3.5 Legibility over decorative depth
Raised, inset, glow, border, highlight, blur, or transparency effects are optional presentation tools. Text, icon, route, ritual, emergency, and state clarity are mandatory.

## 3.6 One product, selective platform behavior
Pilgrims Soft Surface is shared across iOS and Android. Platform adaptation may change native behavior, interaction convention, system chrome, haptics, and presentation mechanics, but not fork the product into separate visual identities.

## 3.7 Stress-safe hierarchy
The design must remain obvious when the user is tired, rushed, anxious, elderly, distracted, or using accessibility settings.

## 3.8 Appearance parity
Light and Dark are equally required product appearances. Neither may be treated as a secondary skin with missing components, unreadable states, or degraded critical flows.

# 4. Visual identity direction

## 4.1 Canonical name
The project-owned canonical design-language name is **Pilgrims Soft Surface**.

Do not rename the system canonically to “Neumorphism.” That term may only describe specific soft-relief depth techniques where useful.

## 4.2 Figma grounding rule
The approved current Figma design is the visual reference for the present styling direction.

The current reference is treated as light-oriented calibration unless an explicit verified Dark Mode design is available. Therefore:
- Light theme may be calibrated directly from verified Figma variables and repeated design decisions,
- Dark theme is a required semantic counterpart of the same identity,
- exact Dark values must be intentionally designed and verified,
- no spec or implementation may claim fabricated Dark values are “from Figma.”

Figma-generated code, local layer colors, one-off shadows, or font artifacts must not be promoted blindly into canonical Flutter tokens.

## 4.3 Surface roles
The design system must define reusable semantic surface roles including:
- canvas/background,
- base surface,
- raised surface,
- inset/recessed surface,
- floating surface,
- interactive surface,
- selected/active surface,
- critical solid surface,
- modal/sheet surface,
- map overlay surface.

## 4.4 Depth and effect roles
The design system must define semantic effect roles including:
- subtle outer shadow,
- raised shadow,
- inset shadow,
- inner highlight,
- ambient accent glow,
- subtle border,
- strong boundary,
- focus ring,
- scrim,
- no decorative effect.

Representative semantic names may include:
- `effect.surface.subtle`,
- `effect.surface.raised`,
- `effect.surface.inset`,
- `effect.surface.floating`,
- `effect.surface.active`,
- `effect.surface.critical`,
- `effect.focus`,
- `effect.none`.

Feature code must not reconstruct these roles from raw shadow parameters.

## 4.5 Information-density strategy
High-density information must use calm modular grouping and progressive disclosure. Repeated list surfaces should prefer low-cost, low-relief presets over layered decorative effects.

## 4.6 Critical-surface strategy
Ritual guidance, RIC, emergency, medical, active wayfinding, and trusted-write failure surfaces must prefer explicit contrast, strong boundaries, and solid/low-relief treatment in both appearances.

## 4.7 Map styling strategy
Map controls may use Soft Surface floating/overlay roles, but route geometry, labels, confidence state, floor state, and fallback instructions always outrank decorative depth.

# 5. Token architecture

The design system separates reusable decisions into five layers.

## 5.1 Foundation tokens
Foundation tokens are primitives and scales:
- base palette,
- typography scale,
- spacing scale,
- radius/shape scale,
- icon-size scale,
- border-width scale,
- depth primitives,
- opacity primitives,
- motion durations,
- motion curves.

Foundation tokens are implementation inputs, not feature-widget APIs.

## 5.2 Semantic tokens
Semantic tokens translate primitives into meaning. Required families include:
- `color.canvas`,
- `color.surface.base`,
- `color.surface.raised`,
- `color.surface.inset`,
- `color.surface.floating`,
- `color.surface.interactive`,
- `color.surface.selected`,
- `color.surface.critical`,
- `color.surface.modal`,
- `color.surface.mapOverlay`,
- `color.text.primary`,
- `color.text.secondary`,
- `color.text.inverse`,
- `color.icon.primary`,
- `color.border.subtle`,
- `color.border.strong`,
- `color.action.primary`,
- `color.action.secondary`,
- `color.status.success`,
- `color.status.warning`,
- `color.status.critical`,
- `color.map.routePrimary`,
- `color.map.anchorSaved`,
- `color.focus`,
- `color.scrim`,
- semantic spacing and motion roles,
- semantic Soft Surface effect roles from section 4.4.

## 5.3 Component tokens
Component tokens define stable anatomy and variants for buttons, cards/surface containers, navigation/chrome, quick actions, inputs, progress, map controls, ritual surfaces, emergency surfaces, group/state cards, and account/settings rows. They must source semantic roles rather than raw primitives.

## 5.4 Appearance mappings
Every appearance-sensitive semantic token must map intentionally for Light and Dark.

Geometry normally remains appearance-independent: spacing, radii, touch targets, information hierarchy, and component anatomy.

Mode-sensitive properties may include surface colors, text/icon colors, border intensity, shadow/highlight strength, ambient glow, scrims, system chrome brightness, and map overlay treatment.

## 5.5 Platform adaptation
Platform adaptation may refine native behavior and presentation mechanics while consuming the same semantic/component roles. Platform tokens must not become separate iOS/Android brand systems.

## 5.6 Figma variable translation rule
Verified Figma variables and repeated design decisions may inform foundation/semantic mappings. One-off decorative values, generated code values, or component-local artifacts remain local evidence unless repeated use and semantic need justify promotion.

## 5.7 Feature-consumption rule
Feature modules consume semantic/component roles only. They must not depend directly on primitive palette names, raw Figma variable names, raw effect parameters, or screenshot-derived constants.

# 6. Theme architecture in Flutter

## 6.1 Theme ownership
All appearance construction is centralized in the design-system layer.

## 6.2 Mandatory appearance modes
The product must support exactly these user-facing appearance modes:
- **System** — follows the OS appearance,
- **Light** — forces the complete Light theme,
- **Dark** — forces the complete Dark theme.

System is the recommended default.

## 6.3 Appearance behavior contract
Appearance selection must work without account or network, require no Supporter entitlement, persist locally, apply immediately, survive restart, preserve navigation and active feature state, and remain independent from Simple Mode.

## 6.4 Required theme layers
The Flutter design system must expose shared foundation tokens, complete Light and Dark themes, semantic theme extensions, component theme mappings, Soft Surface effect presets, and platform adaptation hooks.

## 6.5 Recommended implementation pattern
Use Flutter theming plus custom `ThemeExtension` structures for app-specific semantic colors, surface/depth roles, spacing, motion, and map/status semantics. The app shell maps the persisted Appearance preference to `ThemeMode.system`, `ThemeMode.light`, or `ThemeMode.dark`. Feature modules must not own `ThemeMode`.

## 6.6 Required theme outputs
Expose `ColorScheme` mappings where appropriate, semantic surface/text/icon/border/status/map colors, typography, spacing/shape accessors, effect/depth accessors, component themes, focus/scrim behavior, and platform behavioral adapters.

## 6.7 Theme-switch integrity
Switching appearance must not recreate domain state, reset navigation, restart an active ritual, discard map/group state, or alter entitlement/auth/offline truth.

## 6.8 Forbidden theme behavior
Forbidden: optional/partial Dark Mode, naive inversion, feature-level mini-themes, scattered hardcoded appearance checks, raw Figma values in feature code, or visual changes that alter product semantics.

# 7. Color system

## 7.1 Color-system goals
The color system must preserve calm readability, clear hierarchy, semantic status, complete Light/Dark support, localization/accessibility stability, map/emergency clarity, and restrained brand-cyan identity.

## 7.2 Primitive palette
A primitive palette may include verified brand/accent values and neutral/status scales. Figma values may inform this layer only after they are verified as true variables or repeated decisions. Do not promote every local layer color globally.

## 7.3 Semantic color roles
Define paired Light/Dark mappings for canvas; base/raised/inset/floating/interactive/selected/critical/modal/map-overlay surfaces; primary/secondary/inverse text; icons; subtle/strong borders; actions; success/warning/critical states; route/anchor/confidence roles; focus ring; and scrim.

## 7.4 Light appearance rule
Light appearance may be calibrated directly from the approved light-oriented Figma reference where variables and repeated design decisions are verified.

## 7.5 Dark appearance rule
Dark appearance preserves the same semantic hierarchy and component anatomy without naive inversion. It must use tonal separation, borders, highlights, and restrained shadows together; avoid crushed black-on-black cards; preserve strong contrast; keep state boundaries explicit; avoid excessive cyan glow; and strengthen boundaries when accessibility settings require them.

## 7.6 Status-color rule
Color alone must never carry critical meaning. Status requires copy, iconography, structure, or another non-color cue.

## 7.7 Critical-content rule
Emergency, medical, ritual-critical, RIC, route-critical, and trusted-write failure content must use explicit high-clarity surface/text/boundary combinations in both appearances.

## 7.8 Map-color rule
Map route, anchor, confidence, and fallback roles remain centralized and contrast-tested against both map imagery and Light/Dark overlay surfaces.

# 8. Typography system

Material 3 provides tokenized type roles, and Flutter accessibility guidance emphasizes scalable readable text. ([m3.material.io](https://m3.material.io/styles/typography/overview))

## 8.1 Typography goals
Typography must support:
- calm readability,
- quick scanning,
- multilingual support,
- large text scaling,
- strong distinction between key guidance and secondary detail.

## 8.2 Typography structure
The typography system should define:
- display styles
- headline styles
- title styles
- body styles
- label styles
- caption/micro styles if truly necessary

## 8.3 Semantic text roles
Feature code should use semantic text roles such as:
- `text.heroTitle`
- `text.screenTitle`
- `text.sectionTitle`
- `text.stepTitle`
- `text.bodyPrimary`
- `text.bodySecondary`
- `text.meta`
- `text.button`
- `text.emergencyLarge`

## 8.4 Typography usage rules
- Ritual instructions should use strong readable body/text hierarchy.
- Emergency mode should define very large accessible styles.
- Dense secondary metadata must remain readable and not become tiny by default.
- Text styles must scale correctly under larger text settings.

## 8.5 Font-family rule
The app may define a branded typography choice, but it must preserve multilingual readability and fallback safety.

## 8.6 Forbidden typography behaviors
Forbidden:
- hardcoded font sizes in arbitrary widgets,
- separate unofficial text hierarchies per feature,
- local “temporary” text styles that drift into production reuse.

---

# 9. Spacing system

## 9.1 Purpose
Spacing tokens create rhythm, hierarchy, and maintainability.

## 9.2 Required scale
The design system should define a limited consistent spacing scale.

Example categories:
- 0
- 2
- 4
- 8
- 12
- 16
- 20
- 24
- 32
- 40
- 48
- 64

Exact numeric values may be tuned, but the scale must remain small, intentional, and reusable.

## 9.3 Semantic spacing roles
Examples:
- `space.inline.xs`
- `space.inline.sm`
- `space.inline.md`
- `space.stack.sm`
- `space.stack.md`
- `space.stack.lg`
- `space.section.md`
- `space.page.horizontal`
- `space.page.vertical`

## 9.4 Rule
Feature code should prefer semantic spacing helpers or tokens rather than arbitrary literal values.

---

# 10. Shape and corner-radius system

## 10.1 Goals
Shape supports a calm, approachable, touch-friendly identity without decorative noise.

## 10.2 Required shape tokens
Define reusable radius tiers for compact controls, standard controls, cards/surfaces, sheets/modals, and pills/full rounding.

## 10.3 Usage rules
Geometry normally remains identical between Light and Dark. Platform adaptation may refine native container behavior without changing product identity.

---

# 11. Depth, shadow, highlight, border, glow, opacity, and scrim system

## 11.1 Goal
Depth clarifies hierarchy and interaction rather than simulating physical material for its own sake.

## 11.2 Required effect roles
Provide limited reusable tiers for subtle outer shadow, raised shadow, inset shadow, inner highlight, ambient accent glow, subtle border, strong boundary, focus ring, scrim, and none.

## 11.3 Appearance-aware depth
Light and Dark may map the same semantic effect role to different shadow/highlight/border intensities. Dark Mode must not rely on dark shadow alone for boundaries.

## 11.4 Performance-safe effect tiers
Define normal presets for prominent surfaces, low-cost variants for dense/repeated lists, simplified fallbacks for performance-constrained contexts, and `effect.none` where decorative depth reduces clarity.

A component must not reproduce every Figma shadow layer if doing so risks scrolling, animation, or map-control jank. Visual fidelity preserves hierarchy, shape, color relationship, depth intent, and component identity—not every effect layer regardless of runtime cost.

---

# 12. Pilgrims Soft Surface depth system

## 12.1 Purpose
Pilgrims Soft Surface provides calm dimensional grouping through mostly opaque surfaces, tonal separation, raised/inset depth, subtle boundaries, and restrained accent glow.

## 12.2 Surface-role rule
Components choose a semantic surface role based on hierarchy and interaction meaning, not screenshot resemblance.

## 12.3 Approved decorative treatment
Soft-relief depth may be used on Home dashboard cards, quick actions, selected navigation/chrome, lightweight floating controls, planner/group summaries, non-critical sectional containers, and map controls when contrast remains explicit.

## 12.4 Low-decoration zones
Prefer solid or low-relief surfaces for long ritual guidance, RIC reasoning/results, emergency/medical content, active wayfinding instructions, dense forms, critical warnings, trusted-write failures, and large-text layouts where depth reduces clarity.

## 12.5 Accessibility fallback
Custom material, depth, overlay, transparency, glow, and decorative effects must degrade to clearer high-contrast surfaces when accessibility settings require it.

Soft Surface depth must never be the only cue for selected, error, stale, disabled, route, emergency, or focus state.

## 12.6 Transparency rule
Transparency/blur may still be used selectively for platform-native overlays or contextual effects, but it is not the product identity and must have an opaque/clear fallback.

## 12.7 Platform rule
iOS and Android share the same Pilgrims Soft Surface identity. Platform-specific surface behavior is subordinate to the shared semantic system and file `09`.

# 13. Motion and animation system

## 13.1 Goals
Motion should support comprehension and calmness, not spectacle.

## 13.2 Required motion tokens
- duration fast
- duration standard
- duration emphasized
- curve standard
- curve entrance
- curve exit
- curve emphasized
- spring or physics presets only if explicitly standardized

## 13.3 Motion roles
- page transition
- modal transition
- sheet expansion/collapse
- state-change emphasis
- map control response
- loading placeholder behavior
- micro feedback transitions

## 13.4 Motion rules
- Motion must reinforce hierarchy and continuity.
- Emergency and safety interactions should feel quick and dependable, not theatrical.
- Repeated motion patterns must use centralized tokens.
- Reduced-motion settings must be supported with simplified transitions.

## 13.5 Forbidden behaviors
Forbidden:
- ad hoc durations in arbitrary widgets,
- overuse of bounce or playful curves in serious contexts,
- motion that delays access to urgent information.

---

# 14. Iconography system

## 14.1 Goals
Icons should support recognition, not replace readable labels in critical contexts.

## 14.2 Required rules
- Icon size must use tokenized sizes.
- Icon color must use semantic roles.
- Safety or emergency meaning should not rely on icon alone.
- Map controls may use icon-first patterns only when discoverability remains strong.

## 14.3 Critical-context rule
For emergency, safety, and ritual actions, labels should usually accompany icons unless the pattern is universally understood and tested.

---

# 15. Layout system

Apple’s layout guidance and Flutter’s adaptive design guidance both emphasize designing for usable space and adapting the interface rather than merely squeezing it. ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/layout))

## 15.1 Layout goals
The system must support:
- phones first,
- adaptive layouts for larger screens,
- one-handed usability for high-priority flows,
- predictable spacing and grouping,
- direction-aware layouts.

## 15.2 Layout primitives
The design system should standardize:
- page padding
- section spacing
- content max widths where appropriate
- card/list row padding
- horizontal inset rules
- safe-area-aware top and bottom spacings

## 15.3 Adaptive layout rules
- Large screens may adapt navigation and panel behavior.
- Primary flows must remain obvious on phones.
- Bottom bars, side rails, and split layouts should come from centralized adaptive layout rules, not per-screen improvisation.

---

# 16. Accessibility system rules

## 16.1 Required accessibility considerations
The design system must support scalable text, sufficient contrast in Light/Dark, visible focus, practical touch targets, screen-reader semantics, keyboard/focus navigation where relevant, reduced motion, reduced transparency for remaining transparent/native material, increased-contrast treatment, RTL/bidi-safe structure, and non-color-only status meaning.

## 16.2 Appearance contrast rule
No component is complete until important states are readable in both Light and Dark. Dark Mode may not reduce the contrast standard or make boundaries depend on shadow alone.

## 16.3 Focus rule
Interactive controls require an explicit semantic focus treatment visible across both appearances and accessibility contrast settings.

## 16.4 Touch target rule
Controls maintain practical target sizes in standard and Simple Mode, especially in stress-sensitive flows.

## 16.5 Effect-degradation rule
When accessibility settings require stronger clarity, decorative depth, glow, transparency, and motion simplify without changing information hierarchy or state meaning.

## 16.6 Emergency and critical-flow rule
Emergency, medical, ritual-critical, RIC, active-wayfinding, and trusted-write failure surfaces use high-clarity variants. Decorative depth cannot delay or obscure the primary action.

# 17. Component architecture

Material 3 treats components as structured interactive building blocks, which aligns with this project’s need for a reusable component library. ([m3.material.io](https://m3.material.io/components))

## 17.1 Component goals
Components should:
- express product semantics clearly,
- encapsulate repeated styling and state behavior,
- reduce duplication,
- remain adaptable through tokens,
- expose safe APIs for feature teams.

## 17.2 Component categories
The system should define at least these categories:
- app chrome components
- action components
- input components
- content containers
- feedback components
- navigation components
- list/item components
- map overlay components
- ritual-specific components
- emergency/safety components
- paywall/upgrade components

## 17.3 Component contract structure
Each shared component definition should include:
- purpose
- anatomy
- allowed variants
- states
- semantic tokens used
- accessibility notes
- content rules
- platform adaptation notes
- Flutter API expectations

---

# 18. Core component inventory

This section defines the minimum canonical shared component set.

## 18.1 App chrome components
- App top bar
- Bottom navigation bar / tab bar
- Navigation rail or large-screen nav shell if used
- Section header
- Search/filter bar
- Modal/sheet header

## 18.2 Action components
- Primary button
- Secondary button
- Tertiary/ghost button
- Icon button
- Floating action tray button
- Destructive action button
- Quick action tile

## 18.3 Input and selector components
- Text input field
- Search field
- Toggle/switch
- Checkbox/radio selector if used
- Segmented control
- Chip/filter chip
- Dropdown/selector row
- Date/time picker trigger row

## 18.4 Content containers
- Solid card
- Elevated card
- Raised / inset / floating Soft Surface card variants
- Sheet/container surface
- Panel container
- Inline info strip
- List row container

## 18.5 Feedback components
- Banner
- Snackbar/toast pattern
- Inline validation message
- Loading placeholder/skeleton
- Empty state
- Offline state panel
- Retry state panel

## 18.6 Map-specific components
- Route chip
- Location/anchor card
- Map control cluster
- Destination picker row
- Recenter control
- Route summary panel
- Saved gate chip/panel

## 18.7 Ritual-specific components
- Ritual step card
- Remedy card
- Progress tracker
- Content note block
- Bookmark action row

## 18.8 Group and coordination components
- Group member tile
- Check-in status row
- Regroup pin card
- Live-board item row

## 18.9 Emergency and safety components
- Emergency shortcut card
- Big-text phrase card
- Safety alert banner/card
- Emergency information sheet

## 18.10 Monetization and account components
- Upgrade card
- Entitlement status row
- Purchase option tile
- Restore purchase row
- Settings section row

---

## 18.11 Home composition components from the approved visual reference

The supplied approved Home visual reference establishes the following reusable composition patterns for the standard Home experience:

- **Profile greeting header** — avatar/profile affordance, greeting + user name, notification action, and Settings action.
- **Prayer/context hero** — large rounded cyan/turquoise contextual surface showing current prayer/status information, location context, weather/supportive context where available, and compact prayer-time selectors.
- **Quick-action tile row** — compact icon-led actions with short labels; the visual reference demonstrates five slots: Bacaan, Save Gate, Tata Cara, Emergency, and Lainnya. Canonical feature routing and localization remain owned by feature/navigation specs.
- **Ritual progress card** — progress percentage, elapsed/remaining context where available, horizontal progress visualization, and named ritual milestones.
- **Compact context-summary cards** — paired Saved Gate and Jama’ah Group summaries with concise status metadata and a clear continuation action.
- **Planner schedule card** — date strip, vertical timeline/progress treatment, task title/time, and stateful action button.
- **Bottom navigation shell with central floating action slot** — Home, Ibadah, Group, and Map destinations plus one visually prominent centered action slot.

These patterns are visual/component contracts only. They do not create new feature semantics. In particular, the centered floating action slot must be mapped to an already-approved product action before implementation; agents must not infer scanner, camera, QR, or other behavior solely from its iconography in a mockup.

### 18.11.1 Home composition styling rules
- Large Home sections use generous rounded corners and soft elevation rather than thin card borders alone.
- Cyan/turquoise is the dominant active/accent family; orange may be used for planner/action status where semantically justified.
- Small utility cards remain mostly light/opaque with restrained soft shadow.
- The prayer/context hero may use the strongest accent surface on Home, but text contrast must remain explicit.
- Repeated quick-action tiles and summary cards must use performance-safe low-cost Soft Surface effect tiers.
- The same component anatomy must map intentionally into Dark Mode without naive inversion.
- Profile imagery is dynamic user content and must not be treated as a static design-system asset.

# 19. Component state rules

## 19.1 Required state coverage
Shared components must define, where relevant:
- default
- pressed
- focused
- disabled
- selected
- loading
- error
- success
- active/inactive
- offline or unavailable

## 19.2 State rule
A shared component is not complete if state styling is only defined for the default case.

## 19.3 Feedback rule
State changes should be visible through multiple cues when important: color, text, icon, motion, or structure.

---

# 20. Flutter implementation rules for the design system

## 20.1 Centralized source rule
All tokens, themes, and shared components must live in the design-system package/module.

## 20.2 No feature-level token redefinition
Feature modules may not create unofficial parallel token sets.

## 20.3 Theme access rule
Feature widgets must obtain styling from theme extensions, semantic helpers, or shared component APIs.

## 20.4 Component API rule
Component APIs should be semantic and product-friendly.

Good example:
- `AppPrimaryButton(emphasis: ..., size: ..., icon: ...)`

Weak example:
- `Button(blur: 18, opacity: 0.16, radius: 22, shadowPreset: 3)`

## 20.5 Promotion rule
If a one-off style pattern appears in more than one place, it should be promoted into the shared design system.

## 20.6 Generated token support
If tokens are generated from design tooling, generated outputs must still map to stable semantic theme APIs rather than leak raw design-export structures into feature code.

---

# 21. Recommended Flutter design-system structure

```text
packages/pilgrims_design_system/
  lib/
    src/
      tokens/
        color_tokens.dart
        typography_tokens.dart
        spacing_tokens.dart
        radius_tokens.dart
        elevation_tokens.dart
        opacity_tokens.dart
        blur_tokens.dart
        motion_tokens.dart
        icon_tokens.dart
      themes/
        app_theme.dart
        app_color_scheme.dart
        app_text_theme.dart
        theme_extensions/
          semantic_color_extension.dart
          spacing_extension.dart
          effects_extension.dart
          motion_extension.dart
          map_theme_extension.dart
      components/
        chrome/
        actions/
        inputs/
        containers/
        feedback/
        maps/
        rituals/
        safety/
        monetization/
      patterns/
        empty_states/
        loading_states/
        offline_states/
      platform/
        ios/
        android/
```

## 21.1 Rule
Exact filenames may differ, but this separation of tokens, themes, components, patterns, and platform adaptation must remain clear.

---

# 22. Platform adaptation rules

## 22.1 Shared identity
Pilgrims Soft Surface is the single visual identity across iOS and Android.

## 22.2 Platform adaptation may change
Native navigation behavior, modal/sheet mechanics, haptics, system bars, transition feel, permission UI/settings handoff, and platform-native map/store/notification/location/BLE/asset-delivery behavior may differ.

## 22.3 Platform adaptation must not change
Semantic surface roles, component meaning, core hierarchy, the Light/Dark requirement, critical-state meaning, or product/feature semantics must remain shared.

## 22.4 iOS rule
Use iOS-appropriate interaction and presentation conventions while rendering the same semantic Pilgrims Soft Surface roles. Native translucent system material may be used where appropriate, but it is not the app’s defining visual identity.

## 22.5 Android rule
Use Android-appropriate interaction and presentation conventions while rendering the same semantic Pilgrims Soft Surface roles. Android must not be treated as a secondary “solid fallback” product.

## 22.6 Shared behavior rule
File `09` owns platform adaptation and native bridges. File `08` owns visual identity and theme semantics.

# 23. Design-system quality gates

## 23.1 A token is ready when
- it has a clear semantic purpose,
- it is not duplicative,
- it maps cleanly into Flutter access patterns,
- it supports intended states,
- it will likely be reused.

## 23.2 A component is ready when
- purpose is clear,
- anatomy and states are defined,
- accessibility is considered,
- semantic tokens are wired,
- platform adaptation is known,
- feature teams can use it without local style hacks.

## 23.3 A variant is not justified when
- it only exists because one screen was implemented ad hoc,
- it differs only by raw styling values that should be tokenized,
- it adds maintenance complexity without real semantic benefit.

---

# 24. Anti-patterns forbidden by this design system

## 24.1 Hardcoded repeated colors in feature widgets
Use semantic tokens.

## 24.2 Hardcoded repeated text styles in feature widgets
Use canonical typography roles.

## 24.3 One-off depth/effect stacks per screen
Use shared Pilgrims Soft Surface effect roles and tiers.

## 24.4 Multiple unofficial card/button systems inside feature modules
Promote stable variants into shared components.

## 24.5 Styling based on raw palette or Figma variable names
Feature code consumes semantic/component roles only.

## 24.6 Decorative depth under dense critical text
Critical content uses explicit readable boundaries and low-relief/solid treatment.

## 24.7 Naive Dark Mode inversion
Dark is an intentionally mapped semantic theme, not an inverted Light theme.

## 24.8 Appearance branching inside feature modules
Theme selection belongs to the app shell/design system.

## 24.9 Motion values invented ad hoc
Use shared motion roles.

## 24.10 Color-only or depth-only status communication
Important states require non-color and non-depth cues.

## 24.11 Per-feature icon sizing systems
Use centralized icon roles.

## 24.12 Platform identity fork
Do not create separate iOS and Android product identities.

## 24.13 Raw Figma export leakage
Do not copy generated code, raw shadow stacks, local layer colors, or component-local font choices directly into feature implementation without semantic translation.

# 25. Design-system recommendations adopted from current direction

## 25.1 Recommendation — Pilgrims Soft Surface as the canonical visual language
Use mostly opaque surfaces, soft raised/inset depth, restrained accent glow, rounded geometry, and explicit semantic boundaries.

## 25.2 Recommendation — semantic token architecture first
Translate verified Figma primitives and repeated decisions into foundation → semantic → component → appearance mappings before screen implementation.

## 25.3 Recommendation — mandatory dual appearance
System, Light, and Dark are first-class product behavior. Light and Dark must both be complete and release-tested.

## 25.4 Recommendation — map overlay clarity
Map controls use the shared surface/effect system without competing with routes, labels, confidence, or fallback guidance.

## 25.5 Recommendation — Simple Mode and emergency variants
Simple Mode may reduce decorative depth to lower cognitive load; emergency/critical contexts default to high-clarity treatment.

## 25.6 Recommendation — platform adaptation through shared semantics
iOS and Android may adapt native behavior while retaining one visual identity.

# 26. When this file must be updated

This file must be updated when any of the following changes:
- token categories or structure
- theme architecture
- color or typography system direction
- surface/depth usage rules
- component inventory or component contracts
- accessibility requirements tied to styling
- platform adaptation behavior
- design-system package structure
- central theming implementation strategy

If those evolve but this file is not updated, the codebase will begin to fork visually and structurally.

---

# 27. Summary

This file defines the canonical visual system for Pilgrims Mobile App.

It establishes:
- the design principles,
- the token architecture,
- the theme architecture,
- the color, typography, spacing, shape, and motion systems,
- the controlled surface/depth rules,
- the accessibility requirements,
- the shared component inventory,
- the Flutter implementation boundaries for tokens, themes, and components.

Its purpose is to make the app:
- visually consistent,
- calm and readable,
- adaptable across platforms,
- easy to restyle centrally,
- and safe for long-term AI-assisted development without styling sprawl.

