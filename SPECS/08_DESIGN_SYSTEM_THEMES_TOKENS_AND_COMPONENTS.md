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

It exists because this project has strong visual and operational constraints:
- the app must feel calm, trustworthy, readable, and practical,
- the app must support an iOS-specific adaptation inspired by Apple’s Liquid Glass design direction
- the app must still feel coherent on Android rather than becoming a poor imitation of iOS
- the app must remain legible in stressful and low-vision conditions,
- the Flutter codebase must avoid hardcoded style duplication,
- AI coding agents must be guided toward consistent component use and tokenized implementation,
- the visual system must remain easy to evolve without major refactors.

This file therefore defines:
- design principles,
- theme architecture,
- token categories,
- color and typography semantics,
- motion/effect rules,
- glass/material usage rules,
- component families and states,
- accessibility rules,
- platform adaptation rules,
- Flutter implementation boundaries.

---

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
The design must keep user content and actions more important than decorative surface treatment.

## 3.2 Calm before expressive
The app may be polished and elegant, but never at the expense of focus and clarity.

## 3.3 Semantic styling over raw values
Widgets should be styled using semantic roles and tokens, not raw color literals, arbitrary spacing values, or copied effects.

## 3.4 Reuse before reinvention
If a UI pattern appears more than once or represents a stable product behavior, it should become a shared component or shared tokenized variant.

## 3.5 Legibility over translucency
Apple’s Liquid Glass guidance focuses on adopting the new material thoughtfully, and Apple’s design guidance emphasizes legibility and continuity rather than indiscriminate translucency. ([developer.apple.com](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass))

## 3.6 One product, selective platform expression
The app should feel like one product across platforms, but not by forcing identical styling everywhere.

## 3.7 Stress-safe hierarchy
The design must remain scannable and obvious when the user is tired, rushed, or anxious.

---

# 4. Visual identity direction

## 4.1 Overall visual tone
The visual language should feel:
- clean,
- respectful,
- premium but not flashy,
- modern but not experimental,
- calm under pressure,
- lightweight in cognitive load.

## 4.2 Surface strategy
The visual system should use a combination of:
- strong solid surfaces for dense or critical content,
- soft elevated surfaces for sectional grouping,
- controlled glass/material surfaces for chrome, overlays, and selected floating controls,
- clear tonal hierarchy rather than excessive ornament.

## 4.3 Information-density strategy
High-density information should be broken into calm, modular panels and progressive disclosure patterns rather than one giant content wall.

## 4.4 Map styling strategy
Map UI chrome should remain clear and lightweight. Controls layered over maps may use material/glass treatment when contrast remains strong, but route clarity and labels must stay more important than decorative styling.

---

# 5. Token architecture

Material Design 3 defines tokens as reusable design decisions that can be used across design tools and code, and Flutter’s current architecture guidance supports centralized app theming and separation of concerns. ([m3.material.io](https://m3.material.io/foundations/design-tokens))

## 5.1 Token philosophy
Every reusable visual decision should exist as one of the following:
- a foundation token,
- a semantic token,
- a component token,
- or a platform-adaptation token.

## 5.2 Foundation tokens
Foundation tokens define reusable primitive scales.

Categories:
- base color palette
- typography scale
- spacing scale
- shape/radius scale
- elevation scale
- opacity scale
- blur scale
- motion duration scale
- motion curve scale
- icon size scale
- border width scale

## 5.3 Semantic tokens
Semantic tokens translate primitives into meaning.

Examples:
- `color.surface.primary`
- `color.surface.elevated`
- `color.text.primary`
- `color.text.secondary`
- `color.action.primary`
- `color.action.destructive`
- `color.status.success`
- `color.status.warning`
- `color.status.critical`
- `color.map.routePrimary`
- `color.map.anchorSaved`
- `space.section.large`
- `motion.transition.standard`
- `effect.glass.chrome`

## 5.4 Component tokens
These express component-specific variants while still sourcing from semantic tokens.

Examples:
- button heights
- card padding variants
- input corner radius
- icon-button blur/elevation style
- banner emphasis levels
- route-chip size and icon spacing

## 5.5 Platform-adaptation tokens
These support platform-specific values without forking the whole product system.

Examples:
- iOS navigation-bar material token
- iOS floating-control glass opacity/blur token
- Android elevated-surface tonal variant token
- platform-specific transition presets

---

# 6. Theme architecture in Flutter

## 6.1 Theme ownership
All app theming must be defined centrally in the design-system layer.

## 6.2 Required theme layers
The Flutter design system should expose at least:
- base theme foundations,
- light theme,
- dark theme if supported,
- semantic extensions,
- component theme mappings,
- platform-adaptation overlays or extensions.

## 6.3 Recommended implementation pattern
Use Flutter theming plus custom `ThemeExtension` structures for domain-specific semantic tokens and effects, because Flutter’s theming model supports extension-based custom theme data in a scalable way. ([docs.flutter.dev](https://docs.flutter.dev/ui/design/material))

## 6.4 Required theme outputs
The design-system layer should expose:
- `ColorScheme` mapping where appropriate,
- custom theme extensions for app-specific semantic colors,
- text-theme mapping,
- spacing/effect accessors,
- component theme definitions,
- platform-specific material presets.

## 6.5 Forbidden theme behavior
Forbidden:
- defining parallel shadow/color systems in feature modules,
- bypassing theme extensions by using hardcoded literals,
- per-screen “mini theme systems” that duplicate central tokens.

---

# 7. Color system

Material 3 organizes color through roles rather than ad hoc raw color values, which aligns with the maintainability and semantic requirements of this project. ([m3.material.io](https://m3.material.io/styles/color/roles))

## 7.1 Color-system goals
The color system must:
- support calm readability,
- create clear hierarchy,
- communicate status semantically,
- work across light/dark modes if used,
- remain stable under localization and accessibility changes,
- support map overlays and emergency signals responsibly.

## 7.2 Color-token layers
### Primitive palette tokens
Examples:
- neutral 0–100
- brand primary range
- accent/supportive range
- success range
- warning range
- critical range
- map-specific route/anchor/reference range

### Semantic color roles
Examples:
- background
- surface
- surfaceElevated
- surfaceFloating
- surfaceGlass
- textPrimary
- textSecondary
- textInverse
- iconPrimary
- borderSubtle
- borderStrong
- actionPrimary
- actionSecondary
- actionGhost
- statusSuccess
- statusWarning
- statusCritical
- focusRing
- scrim

## 7.3 Color-role rules
Colors must be referenced through semantic roles in feature code, not primitive palette names.

## 7.4 Status-color usage rules
Status colors must always be supported by iconography, copy, or structural cues. Color alone must not carry critical meaning.

## 7.5 Critical-content rule
Emergency and safety content must use strong, unambiguous contrast and not rely on low-contrast material surfaces.

## 7.6 Map-color rule
Map tokens may define special route/anchor/status colors, but these should still be centralized and contrast-tested.

---

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
Shape should reinforce friendliness and calmness without becoming overly soft or playful.

## 10.2 Required shape tokens
The system should define a limited set of radii and shape roles.

Examples:
- radius none
- radius small
- radius medium
- radius large
- radius extraLarge
- radius pill
- radius full

## 10.3 Usage rules
- Cards, sheets, and overlays should use predictable radius tiers.
- Buttons and chips should follow variant-specific radius rules.
- Floating glass controls may use a more rounded family if consistent with platform adaptation.

---

# 11. Elevation, shadow, opacity, and border system

## 11.1 Goals
Use depth sparingly to clarify hierarchy rather than dramatize the interface.

## 11.2 Required effect tokens
- elevation levels
- shadow presets
- border emphasis levels
- opacity presets
- scrim strengths

## 11.3 Usage rules
- Elevated surfaces should remain legible and not muddy text contrast.
- Glass surfaces may use less traditional shadow language than solid cards, but depth rules must remain explicit.
- Borders should be semantic and not randomly chosen per feature.

---

# 12. Glass/material system

Apple’s current design direction emphasizes Liquid Glass as a system material and advises adopting it thoughtfully in controls, bars, and structures rather than using it indiscriminately. Apple also notes that accessibility settings such as Reduce Transparency and Increase Contrast interact with this material system. ([developer.apple.com](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass))

## 12.1 Purpose
This app supports a controlled glass/material design language, especially on iOS.

## 12.2 Design rule
Glass is a material system, not a blanket stylistic theme.

## 12.3 Approved glass usage zones
Glass or liquid-like material may be used for:
- navigation bars and top chrome
- tab bars and bottom chrome
- floating action trays
- map overlay controls
- filter chips or route chips where contrast is controlled
- modal headers or lightweight overlay containers
- contextual toolbars

## 12.4 Forbidden or strongly discouraged glass usage zones
Glass should not be the default for:
- long ritual text blocks
- dense instructions
- emergency cards
- safety-critical warnings
- dense forms
- complex list rows with lots of metadata
- low-contrast map labels or route instructions

## 12.5 Required glass token categories
- blur level
- fill opacity
- tint strategy
- border/highlight strategy
- shadow/depth preset
- content-on-glass color roles
- pressed/hover/focus states
- reduced-transparency fallback style

## 12.6 Accessibility fallback rules
When transparency reduction or contrast enhancement is active, glass surfaces must degrade to stronger solid/elevated surfaces with preserved hierarchy. Apple specifically notes that Liquid Glass adapts with accessibility settings such as Reduce Transparency and Increase Contrast. ([developer.apple.com](https://developer.apple.com/forums/forums/topics/design-topic))

## 12.7 Platform rule
Glass treatment is strongest on iOS. Android should receive a coherent elevated/material adaptation, not a forced clone.

---

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

Flutter’s accessibility and adaptive-input guidance emphasizes accessibility features, semantics, keyboard navigation, and input diversity. ([docs.flutter.dev](https://docs.flutter.dev/ui/adaptive-responsive/best-practices))

## 16.1 Required accessibility considerations
The design system must support:
- scalable text
- sufficient color contrast
- focus visibility
- touch target consistency
- screen-reader semantics
- keyboard/focus navigation where relevant
- reduced motion
- reduced transparency fallback
- RTL support

## 16.2 Contrast rule
No approved component variant may ship if its default state produces unreliable legibility in its intended context.

## 16.3 Focus rule
Interactive controls must have visible focus treatment and not rely purely on platform defaults if those defaults become insufficient under custom styling.

## 16.4 Touch target rule
Controls must maintain practical target sizes, especially in stress-sensitive flows.

## 16.5 Emergency-mode rule
Emergency mode must define extra-large, high-clarity variants for text and actions.

---

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
- Glass card
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

Flutter’s adaptive design guidance and Apple’s design documentation both support explicit platform adaptation rather than pretending every platform should feel identical. ([docs.flutter.dev](https://docs.flutter.dev/ui/adaptive-responsive))

## 22.1 Shared core, selective expression
The app should keep a shared semantic design system while allowing platform-adapted component behavior and surface treatment.

## 22.2 iOS rules
- Stronger glass/material presence in bars, overlays, and floating controls.
- Strong continuity and smooth material transitions.
- Respect system conventions around bars, controls, and presentations.
- Always preserve readability over glass treatment.

## 22.3 Android rules
- Use elevated/material surfaces rather than trying to mimic iOS glass everywhere.
- Preserve the product’s calm premium feel using the shared semantic system.
- Use platform-appropriate motion, layout, and surface treatment.

## 22.4 Shared behavior rule
Product semantics, hierarchy, and core component meaning should remain aligned across platforms even when styling differs.

---

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

The following are forbidden unless explicitly approved.

## 24.1 Hardcoded repeated colors in feature widgets
Forbidden.

## 24.2 Hardcoded repeated text styles in feature widgets
Forbidden.

## 24.3 One-off glass effects created per screen
Forbidden.

## 24.4 Multiple unofficial card/button systems inside feature modules
Forbidden.

## 24.5 Styling based on raw palette names instead of semantic roles
Forbidden.

## 24.6 Using low-contrast glass under dense critical text
Forbidden.

## 24.7 Motion values invented ad hoc per interaction
Forbidden.

## 24.8 Color-only status communication for important states
Forbidden.

## 24.9 Per-feature icon sizing systems
Forbidden.

## 24.10 Treating platform adaptation as copy-paste visual mimicry
Forbidden.

---

# 25. Design-system recommendations adopted from earlier analysis

## 25.1 Recommendation — controlled Liquid Glass, not universal translucency
The system now explicitly limits glass usage to appropriate structural and overlay zones.

## 25.2 Recommendation — semantic token architecture first
The system prioritizes semantic roles so future palette or style changes can happen centrally.

## 25.3 Recommendation — map overlay clarity
Map overlays are explicitly treated as a distinct styling context so controls can feel premium without harming route clarity.

## 25.4 Recommendation — simple mode and emergency mode variants
The system requires design support for stress-reduced and extra-readable contexts.

## 25.5 Recommendation — platform adaptation through shared semantics
The app keeps one product identity while allowing platform-appropriate surface and motion behavior.

---

# 26. When this file must be updated

This file must be updated when any of the following changes:
- token categories or structure
- theme architecture
- color or typography system direction
- glass/material usage rules
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
- the controlled glass/material rules,
- the accessibility requirements,
- the shared component inventory,
- the Flutter implementation boundaries for tokens, themes, and components.

Its purpose is to make the app:
- visually consistent,
- calm and readable,
- adaptable across platforms,
- easy to restyle centrally,
- and safe for long-term AI-assisted development without styling sprawl.

