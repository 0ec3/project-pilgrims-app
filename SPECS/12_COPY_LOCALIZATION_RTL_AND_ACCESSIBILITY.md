# 12 — COPY, LOCALIZATION, RTL, AND ACCESSIBILITY

## Document status
- **Type:** Normative content, language, and inclusive UX document
- **Priority:** Highest
- **Audience:** Product lead, content lead, design lead, Flutter engineers, QA, AI coding agents, reviewer agents, translation contributors, religious governance contributors
- **Purpose:** Define the canonical rules for user-facing copy, multilingual support, localization structure, RTL behavior, transliteration and translation policy, accessibility requirements, and inclusive communication so the app remains respectful, readable, culturally appropriate, and usable across supported audiences.
- **Authority level:** This file is the canonical source of truth for app copy behavior, localization scope, RTL handling, and accessibility requirements. Screen designs, Flutter implementation, translations, and QA must not contradict this file.
- **Primary dependencies:** `01_README_AND_MASTER_INDEX.md`, `03_PRODUCT_CHARTER_AND_SCOPE.md`, `08_DESIGN_SYSTEM_THEMES_TOKENS_AND_COMPONENTS.md`, `09_PLATFORM_ADAPTATION_IOS_ANDROID_AND_NATIVE_BRIDGES.md`, `10_PERSONAS_IA_USER_JOURNEYS_AND_TASK_FLOWS.md`, `11_SCREENS_STATES_NAVIGATION_AND_UI_BLUEPRINTS.md`
- **Related files:** `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`

---

# 1. Purpose of this file

This app operates in a context where language quality and inclusive usability are not cosmetic concerns. They directly affect trust, clarity, ritual correctness, recovery under stress, and the ability of real pilgrims to use the app safely.

This file exists because the product must:
- communicate respectfully in religious and emotionally sensitive contexts,
- support multiple languages with different reading directions,
- remain readable and usable under stress,
- support larger text, reduced motion, reduced transparency, screen readers, and different input abilities,
- avoid AI-generated copy drift and inconsistent translation behavior,
- ensure that localization is structured and maintainable rather than scattered across features.

This file defines:
- tone and voice rules,
- copy categories and constraints,
- supported-language strategy,
- translation and localization rules,
- Arabic and transliteration policy,
- RTL behavior rules,
- accessibility requirements,
- error, safety, and paywall messaging rules,
- implementation and QA rules for copy and accessibility.

---

# 2. Design and platform grounding

This file reflects several current product-quality principles reinforced by platform guidance:
- accessibility must be built into the interface, not added later, which Flutter explicitly emphasizes in its accessibility guidance ([docs.flutter.dev](https://docs.flutter.dev/ui/accessibility-and-internationalization/accessibility))
- internationalization must be designed structurally, including text direction and locale-aware formatting, which Flutter and Unicode guidance both support ([docs.flutter.dev](https://docs.flutter.dev/ui/accessibility-and-internationalization/internationalization))([unicode.org](https://unicode.org/reports/tr9/))
- Apple and Material guidance both emphasize clarity, readable hierarchy, and accessibility over visual style alone, which matters even more for this app because many users will be stressed, tired, or using larger text.([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/accessibility))([m3.material.io](https://m3.material.io/foundations/accessible-design/overview))

These principles are applied here as product rules.

---

# 3. Copy strategy summary

## 3.1 What the copy must do
The app’s copy must help users:
- know what to do,
- recover when uncertain,
- navigate confidently,
- coordinate calmly,
- get urgent help quickly,
- trust the product.

## 3.2 What the copy must avoid
The copy must avoid:
- sounding casual in the wrong context,
- sounding preachy, patronizing, or legalistic by default,
- using dense technical or religious jargon without need,
- overexplaining in urgent moments,
- using playful or salesy language in safety or ritual-critical contexts,
- treating machine translation as automatically acceptable.

## 3.3 Communication priorities
When tradeoffs happen, copy should prioritize:
1. clarity
2. correctness
3. calmness
4. respectfulness
5. brevity where appropriate
6. polish

---

# 4. Tone and voice

## 4.1 Canonical tone
The app should sound:
- respectful
- calm
- practical
- trustworthy
- supportive
- concise
- never flippant

## 4.2 Tone by context
### Ritual guidance
- clear
- respectful
- steady
- not overly casual

### Recovery / RIC
- reassuring
- focused
- not judgmental
- not alarmist unless truly necessary

### Maps and wayfinding
- direct
- concise
- confidence-aware
- landmark-oriented when useful

### Group coordination
- simple
- practical
- socially neutral
- low-friction

### Emergency and assistance
- very clear
- high-contrast in meaning and structure
- short
- immediate

### Settings and preparation
- neutral
- practical
- not overly verbose

### Upgrade / entitlement surfaces
- ethical
- informative
- not manipulative
- never implying that basic correctness or essential safety is being sold

---

# 5. Copy categories

## 5.1 Category A — Ritual-critical copy
Examples:
- ritual step summaries
- RIC questions
- remedy guidance
- ritual warnings

### Requirements
- highest correctness standard
- linked to governed content where relevant
- careful wording
- easy to scan

## 5.2 Category B — Safety and urgent assistance copy
Examples:
- emergency shortcuts
- emergency cards
- safety banners
- high-priority alerts

### Requirements
- extremely clear
- high-urgency readable structure
- minimal ambiguity
- no decorative phrasing

## 5.3 Category C — Wayfinding copy
Examples:
- route instructions
- low-confidence positioning prompts
- destination labels
- anchor hints

### Requirements
- short
- direct
- floor-aware when relevant
- stress-friendly

## 5.4 Category D — Coordination copy
Examples:
- join group flow text
- “I’m Safe” actions
- regroup pin labels
- itinerary labels

### Requirements
- plain language
- non-invasive wording
- avoids surveillance framing

## 5.5 Category E — Utility and settings copy
Examples:
- settings descriptions
- pack install messages
- planner and notes labels
- local reminder setup

### Requirements
- clear and functional
- avoids jargon where possible

## 5.6 Category F — Monetization copy
Examples:
- upgrade prompts
- supporter plan descriptions
- entitlement messages

### Requirements
- ethical
- accurate
- non-coercive
- must preserve the product’s ethical boundary

---

# 6. Copy rules by scenario

## 6.1 Instructional copy
Instructional copy should answer:
- what the user should do,
- what happens next,
- what matters most.

## 6.2 Error copy
Error copy should answer:
- what happened,
- what the user can do next,
- whether the problem is temporary, local, or permission-related.

## 6.3 Empty-state copy
Empty-state copy should answer:
- what is missing,
- why the screen is empty,
- what action the user can take.

## 6.4 Loading copy
Loading text should be optional and brief. Do not narrate every technical operation.

## 6.5 Offline copy
Offline messaging should explain whether:
- the feature still works locally,
- cached data is being shown,
- the requested action needs the internet.

## 6.6 Confidence-aware map copy
When location certainty is weak, copy must reflect uncertainty honestly.

Examples:
- “Your position may be approximate.”
- “Try using a saved gate or nearby landmark.”

---

# 7. Religious respect and content language rules

## 7.1 Respect principle
All religiously relevant copy must remain respectful in tone and formatting.

## 7.2 No casual simplification of governed guidance
If a piece of content is religiously sensitive, do not shorten it so much that it changes meaning.

## 7.3 No artificial certainty rule
If a ritual-related flow cannot confidently determine a result, the copy must not pretend certainty.

## 7.4 No sensationalism
Do not use dramatic fear-based wording in ritual guidance unless the content governance explicitly requires a stronger warning.

## 7.5 User-facing explanation rule
Internal labels such as “RIC” may exist in product architecture, but user-facing copy must still be understandable without product-internal jargon.

---

# 8. Supported language strategy

## 8.1 Canonical initial supported languages
The initial supported-language strategy should prioritize:
- English
- Arabic
- Indonesian

Additional languages may be added later only with quality support and maintenance capacity.

## 8.2 Why these languages
This reflects:
- likely user needs discussed in product planning,
- pilgrimage context,
- the user-base direction implied by the product scope,
- the need for both RTL and LTR support from the start.

## 8.3 Language quality rule
Do not add a language just to claim support if translation quality, RTL/layout handling, or QA cannot be maintained.

---

# 9. Localization structure

## 9.1 Localization architecture goals
Localization must be:
- centralized
- feature-organized
- maintainable
- testable
- safe for AI-agent implementation

## 9.2 Localization file organization
Localization keys should be organized by:
- shared/common
- feature-family
- state/system messages
- safety/emergency
- monetization/account

## 9.3 Key naming rule
Keys should be:
- stable
- descriptive
- domain-oriented
- not tied to temporary visual layout names

Good examples:
- `home.resume_ritual`
- `map.route.position_uncertain`
- `group.join.invalid_code`
- `emergency.saved_gate_missing`

Weak examples:
- `text1`
- `button_new`
- `label_red_card`

## 9.4 No inline reusable strings
Reusable user-facing strings must not be hardcoded repeatedly in widgets.

---

# 10. Localization implementation rules

## 10.1 Single source of truth rule
The localization system must be the single source of truth for reusable user-facing strings.

## 10.2 Feature ownership rule
Each feature family should own its domain strings while shared/common patterns stay centralized.

## 10.3 State-message reuse rule
Common state messages such as offline, retry, permissions, and generic button labels should come from shared localization resources where reuse is real.

## 10.4 Generated localization rule
Generated localization code is implementation support, not the conceptual source of truth.

---

# 11. Arabic and transliteration policy

## 11.1 Arabic support principle
Arabic must be treated as a first-class supported language, not a cosmetic add-on.

## 11.2 Transliteration policy
Where transliteration is needed, it must be:
- intentional
- consistent
- reviewed for usability
- never mixed randomly with unrelated spelling patterns

## 11.3 Translation vs transliteration rule
The product should distinguish between:
- translated meaning
- Arabic source phrase
- transliterated pronunciation aid

These are not interchangeable.

## 11.4 Ritual and phrasebook handling rule
Phrasebook and ritual content may need structured support for:
- Arabic text
- translated meaning
- transliteration or pronunciation helper

The exact content model is defined in content-governance docs, but UI must support the distinction clearly.

## 11.5 Consistency rule
Do not use inconsistent spellings for the same term across the app without documented reason.

## 11.6 Script-aware typography fallback
Localization must not assume that a font visible in the approved Figma reference supports every supported script.

File `08` owns font stacks and semantic text roles. This file requires those stacks to preserve:
- correct Arabic shaping and diacritics,
- readable Latin-script English and Indonesian,
- stable mixed Arabic/Latin bidirectional runs,
- semantic hierarchy across fallback fonts,
- large-text accessibility and required weight coverage.

Feature code and localization files must not select ad hoc font families to work around missing glyphs. Missing-script or missing-weight coverage is a design-system defect to fix centrally and verify with realistic localized content.

---

# 12. Locale and formatting rules

## 12.1 Locale-aware formatting
The app must format locale-sensitive content correctly where relevant.

Examples:
- dates
- times
- number formatting
- pluralization
- punctuation spacing conventions where supported by locale tooling

## 12.2 Time formatting rule
Use user-appropriate localized time formatting rather than forcing one global style everywhere.

## 12.3 Pluralization rule
Plural-sensitive strings must use proper localization mechanisms, not manual concatenation.

## 12.4 Mixed-language rule
When the UI contains mixed Arabic and Latin content, text handling must remain directionally stable and readable.

---

# 13. RTL principles

## 13.1 RTL is a structural requirement
RTL support is not just text alignment. It affects layout direction, control ordering, icon mirroring where appropriate, and reading flow.

## 13.2 Direction-aware layout rule
Use direction-aware layout APIs and spacing semantics rather than hardcoded left/right assumptions.

## 13.3 Mirroring rule
Mirror UI structure where appropriate for RTL.

Examples:
- leading/trailing icon positions
- row alignment
- back/up directional affordances
- progress or step indicators when meaning depends on direction

## 13.4 Non-mirroring rule
Do not mirror elements that would become semantically wrong if reversed.

Examples may include:
- certain maps or real-world directional references
- photographs
- some branded or symbolic assets

## 13.5 Route and map rule
The map subsystem must handle RTL copy and labels appropriately, but real-world route geometry and floor references must remain truthful rather than visually mirrored in a misleading way.

---

# 14. Bidirectional text handling

## 14.1 Bidi handling rule
When Arabic and Latin text appear together, the UI must handle bidirectional text safely and predictably.

## 14.2 Mixed-content examples
Examples:
- “Gate 79” inside Arabic UI
- floor or map codes inside Arabic sentences
- alphanumeric join codes
- English pack names inside Arabic or Indonesian contexts if not translated

## 14.3 Isolation rule
Use appropriate text isolation or bidi-safe formatting patterns so mixed strings do not reorder unpredictably. The Unicode Bidirectional Algorithm is the underlying standard that governs this behavior.([unicode.org](https://unicode.org/reports/tr9/))

## 14.4 Testing rule
Bidi-heavy screens must be tested with realistic mixed content, not just fully translated placeholder text.

---

# 15. Accessibility principles

## 15.1 Accessibility is a product requirement
Accessibility is part of correctness for this app.

## 15.2 Accessibility must support stressed users too
Features that are accessible only in calm settings are not sufficient for this product.

## 15.3 Accessibility must be built into components and screens
Do not rely only on QA at the end to “make things accessible.”

## 15.4 Accessibility must survive platform adaptation
Custom material, depth, overlay, transparency, glow, map-overlay, and motion treatments must not break accessibility. Platform-native material behavior may differ, but accessibility meaning and fallback quality must remain shared.

---

# 16. Core accessibility requirements

## 16.1 Text scaling
The app must support larger text sizes without breaking critical flows.

## 16.2 Contrast
Critical text and actions must maintain strong contrast in both Light and Dark.

Dark Mode must preserve semantic hierarchy rather than use naive inversion. Important surface boundaries, text/icon contrast, focus, selection, error, stale, disabled, route, and emergency states must remain explicit and must not depend on shadow alone.

## 16.3 Touch target size
Interactive elements must remain easy to tap, especially in emergency and walking contexts.

## 16.4 Screen-reader semantics
Important labels, actions, status changes, and section headings must be exposed meaningfully to screen readers.

## 16.5 Reduced motion
Motion should reduce gracefully where supported or required.

## 16.6 Reduced transparency and decorative-effect reduction
When transparency reduction, increased contrast, or comparable accessibility settings require clearer presentation:
- transparent or native-material overlays must become more opaque where needed,
- custom depth, shadow, inner-highlight, glow, and decorative effects must simplify when they reduce clarity,
- hierarchy and text/icon contrast must remain understandable in both Light and Dark,
- selected, error, stale, disabled, route, emergency, and focus states must never rely on depth or color alone.

## 16.7 Keyboard/focus accessibility where relevant
Focus order and visibility must remain coherent in contexts where keyboard or non-touch navigation matters.

---

# 17. Accessibility by context

## 17.1 Ritual screens
Must support:
- readable step content
- large text
- expandable detail without losing structure
- clear heading hierarchy

## 17.2 Map screens
Must support:
- large enough controls
- clear label contrast
- route instruction fallback beyond visual map-only signals
- low-confidence state communication that is understandable without subtle visual cues

## 17.3 Group screens
Must support:
- clear action labels
- freshness indicators that do not rely on color alone
- easy join and check-in input handling

## 17.4 Emergency screens
Must support:
- extra-large readable text
- strong contrast
- minimal clutter
- low-precision tapping tolerance

## 17.5 Pack/install screens
Must support:
- understandable install states
- progress clarity
- non-color-only state changes

---

# 18. Error, offline, and unavailable message rules

## 18.1 Error copy rules
Error messages must:
- explain what failed in simple terms,
- tell the user what they can do next,
- avoid raw technical internals,
- distinguish between validation, permission, connectivity, and service errors where useful.

## 18.2 Offline copy rules
Offline copy must distinguish between:
- still usable offline,
- showing cached data,
- requires internet for this action.

## 18.3 Unavailable-state rules
Unavailable states must explain whether something is unavailable because of:
- missing permission
- missing pack
- missing group/account state
- unsupported capability
- entitlement boundary

## 18.4 Retry copy rules
Retry actions should be labeled clearly and not hidden behind vague messages.

---

# 19. Safety and emergency copy rules

## 19.1 Safety copy must be immediate
Safety and emergency messaging must prioritize direct action and readability.

## 19.2 No decorative language
Avoid playful, motivational, or overly branded phrasing in emergency contexts.

## 19.3 Missing-data rule
If emergency-supporting data is missing, copy must stay useful rather than collapsing into a dead end.

Examples:
- no saved gate
- no medical profile
- no group active

## 19.4 Big-text rule
Emergency cards and urgent phrase surfaces must support especially large text variants.

---

# 20. Monetization and entitlement copy rules

## 20.1 Ethical boundary rule
Copy must never imply that core pilgrimage correctness or essential safety is being sold.

## 20.2 Upgrade explanation rule
Upgrade copy should explain convenience or enrichment clearly.

Examples:
- richer offline packs
- extended notes/bookmarks limits
- premium planning enhancements

## 20.3 No coercive copy
Do not use manipulative urgency or shame-based language.

## 20.4 Lock-state copy rule
If a feature is gated, the screen must still be honest about what remains available for free.

---

# 21. Copy structure rules for AI agents

## 21.1 AI agents must not invent product terminology casually
They must use canonical terms from file `04` and feature files.

## 21.2 AI agents must not create inline copy drift
If a pattern exists centrally, reuse it.

## 21.3 AI agents must not change user-facing meaning to make strings shorter or prettier
Meaning and trust come first.

## 21.4 AI agents must not bypass localization resources
No repeated hardcoded user-facing strings in feature widgets.

## 21.5 AI agents must ask or defer when copy touches governed religious meaning
Do not improvise around ritual-critical wording.

---

# 22. Accessibility implementation rules for Flutter

## 22.1 Semantics rule
Use proper semantics labels, hints, and structure where the interface requires them.

## 22.2 Large-text layout rule
Layout must be resilient under text scaling and should avoid clipping or overlapping primary actions.

## 22.3 Directionality rule
RTL support must use Flutter direction-aware widgets and layout primitives rather than manual reversal hacks.

## 22.4 Focus visibility rule
Custom components must preserve visible focus and selected states.

## 22.5 Motion/transparency/depth rule
Custom material, depth, glow, overlay, and transparency behavior must integrate with reduced-motion, reduced-transparency, and increased-contrast preferences. Accessibility fallbacks must preserve state meaning and interaction hierarchy in both Light and Dark.

---

# 23. Testing and QA requirements

## 23.1 Localization QA
Must include:
- missing-key detection
- overflow detection in larger text sizes
- mixed-language screens
- Bidi rendering checks
- locale formatting checks

## 23.2 RTL QA
Must include:
- shell navigation
- Home
- Rituals
- Map overlays and route instructions
- Group join flow
- emergency screens
- settings

## 23.3 Accessibility QA
Must include:
- large text
- screen reader basics on major flows
- contrast review on critical surfaces in Light and Dark
- reduced transparency/reduced motion/increased-contrast checks where relevant
- tap target checks on urgent actions

## 23.4 Critical-flow QA
At minimum test:
- Start Ritual
- RIC result
- Save My Gate
- route launch
- Join Group
- I’m Safe
- emergency shortcut
- pack install state changes

---

# 24. Canonical shared copy patterns

## 24.1 Generic action labels
Examples that should be standardized centrally where reused:
- Continue
- Try Again
- Save
- Cancel
- Open Settings
- Download
- Resume
- Start

## 24.2 Shared state labels
Examples:
- Offline
- Approximate location
- Requires internet
- Permission needed
- Not installed
- Downloading
- Verifying
- Installed

## 24.3 Shared explanatory patterns
Examples:
- internet-required explanation
- pack-not-installed explanation
- location-permission value explanation
- low-confidence map explanation

## 24.4 Rule
These patterns should be centralized when reused across features.

---

# 25. Recommendations adopted into this specification

## 25.1 Recommendation — calm, respectful, task-oriented language
The app now has an explicit tone system tied to real product contexts rather than generic UX writing advice.

## 25.2 Recommendation — Arabic and RTL are first-class from the start
RTL and Arabic are now treated structurally, not as late translation add-ons.

## 25.3 Recommendation — accessibility is built into screen and component contracts
Accessibility rules are now tied directly to flows and contexts like maps and emergency screens.

## 25.4 Recommendation — mixed-language and bidi handling is explicit
This is especially important for gate codes, floor names, join codes, and map references inside Arabic UI.

## 25.5 Recommendation — ethical monetization copy is enforced at language level
Upgrade and lock-state messaging must now preserve the product’s ethical boundary.

---

# 26. Anti-patterns forbidden by this specification

The following are forbidden unless explicitly approved.

## 26.1 Repeated hardcoded user-facing strings in widgets
Forbidden.

## 26.2 Treating Arabic text as decorative instead of first-class content
Forbidden.

## 26.3 Treating RTL as “flip some alignment” only
Forbidden.

## 26.4 Using playful or salesy copy in ritual-critical or emergency contexts
Forbidden.

## 26.5 Translating or shortening governed religious meaning casually
Forbidden.

## 26.6 Color-only status communication for important states
Forbidden.

## 26.7 Shipping large-text or RTL-broken layouts as acceptable debt
Forbidden.

## 26.8 Treating accessibility as QA-only work
Forbidden.

## 26.9 Upgrade copy that implies correctness or safety is being sold
Forbidden.

---

# 27. When this file must be updated

This file must be updated whenever any of the following changes:
- supported language strategy
- tone and voice rules
- Arabic/transliteration policy
- RTL handling expectations
- accessibility requirements
- shared copy patterns
- monetization copy rules
- emergency copy rules
- localization file organization
- bidi handling conventions

If any of these evolve but this file is not updated, content quality, translation consistency, and accessibility will drift quickly.

---

# 28. Summary

This file defines the canonical language and inclusive UX rules for Pilgrims Mobile App.

It establishes:
- the tone and voice of the product
- copy behavior by context
- supported language strategy
- localization structure and implementation rules
- Arabic and transliteration policy
- RTL and bidirectional text behavior
- accessibility principles and requirements
- error, offline, safety, and entitlement messaging rules
- testing and QA expectations

Its purpose is to ensure that the product remains:
- respectful
- clear
- culturally and linguistically appropriate
- accessible
- and safe for long-term AI-assisted implementation without content drift.



# 24. Guide Marketplace copy, terminology, and accessibility

The user-facing English feature name is **Hire a Guide**. The canonical English provider term in product/spec identifiers is **Mutawef**, aligned with current official Nusuk English usage. Legal/regulatory sources may use different terms or spellings and must not be rewritten to fit product terminology.

Copy must distinguish:
- Mutawef / Umrah ritual accompaniment,
- Tourist Guide licensing,
- separately verified religious credentials,
- PILGRIMS verification of a specific fact.

Trust copy must say what was verified and avoid ambiguous claims such as "official", "guaranteed", "certified scholar", or generic "verified guide" when the underlying fact is narrower.

Until the competent Mutawef authorization model is legally resolved, public copy must not use **Verified Mutawef** or equivalent as a trust badge.

Contact copy must make clear that:
- the user is choosing an external contact channel,
- PILGRIMS is not silently messaging on the user's behalf,
- V1 contact does not mean PILGRIMS booked, paid for, or guaranteed the service.

Accessibility requirements:
- trust/credential state is announced in meaningful screen-reader text;
- current/stale/expired/suspended/revoked cannot depend on color alone;
- licence/credential labels, pricing, inclusions/exclusions, and contact/report actions remain usable at large text;
- Arabic RTL ordering must preserve label/value, price/currency, status/freshness, and action meaning;
- translated religious/service terminology requires human language review where ambiguity could affect trust or ritual meaning.
