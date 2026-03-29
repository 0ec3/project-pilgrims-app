# 25 — FEATURE: ONBOARDING, HOME, AND SIMPLE MODE

## Document status
- **Type:** Normative feature-family specification
- **Priority:** Highest
- **Audience:** Founder, product lead, design lead, Flutter engineers, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical feature contract for first launch, startup resolution, onboarding, language and preference setup, Home Root behavior, urgent shortcut architecture, Simple Mode behavior, first-use pack awareness, and the visual/platform rules that govern the app’s calm entry experience.
- **Authority level:** This file is the canonical source of truth for onboarding, Home, and Simple Mode behavior. If implementation, UI, or tests diverge from this file, this file wins unless a higher-level normative contract or approved decision record explicitly changes it.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`, `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`, `10-PERSONAS-IA-USER-JOURNEYS-AND-TASK-FLOWS.md`, `11-SCREENS-STATES-NAVIGATION-AND-UI-BLUEPRINTS.md`, `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`, `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`, `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `17-ANALYTICS-OBSERVABILITY-AND-PERFORMANCE-BUDGETS.md`, `18-FEATURE-RITUALS-RIC-AND-RELIGIOUS-CONTENT.md`, `19-FEATURE-MAPS-SAVE-MY-GATE-AND-3D-WAYFINDING.md`, `20-FEATURE-GROUP-HUB-CHECKINS-REGROUP-AND-SHARED-COORDINATION.md`, `21-FEATURE-PLANNER-REMINDERS-WALLET-NOTES-AND-BOOKMARKS.md`, `22-FEATURE-PHRASEBOOK-EMERGENCY-SAFETY-AND-ASSISTIVE-TOOLS.md`, `24-FEATURE-ACCOUNT-SUBSCRIPTIONS-ENTITLEMENTS-AND-SETTINGS.md`
- **Related files:** `23`, `26`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This file exists because onboarding, Home, and Simple Mode are the user’s first and most repeated contact with the product.

If these entry surfaces are weak, the entire product feels harder than it actually is.

For this project, these surfaces are unusually sensitive because:
- many users are first-time pilgrims with limited mental bandwidth,
- some users are elderly or low-confidence with smartphones,
- the app must remain useful on first launch even with poor connectivity,
- urgent tasks must stay reachable without hunting through the app,
- Home can easily decay into a cluttered dashboard if it is not governed tightly,
- Simple Mode can easily become either cosmetic theater or an unstable “second app,”
- iOS visual treatment is expected to feel modern and Liquid-Glass-aware, but the product must still preserve calmness, legibility, and platform honesty.

This file prevents those failures by defining:
- how startup resolution works,
- what onboarding is and is not allowed to do,
- how language and initial preferences are set,
- how Home behaves as a calm recovery surface,
- how Simple Mode reduces complexity without forking the architecture,
- how urgent shortcut architecture works,
- how these surfaces behave under offline, stale, or protected-state conditions,
- how iOS and Android differ visually without becoming two separate products.

---

# 2. Feature purpose and user value

## 2.1 Feature family purpose
This feature family exists to help pilgrims:
- enter the app without confusion,
- understand the value of the product quickly,
- begin the right next task with minimal friction,
- recover into the correct section when they are stressed or unsure,
- use a reduced-complexity mode when the standard interface feels too dense.

## 2.2 Main user value statement
A pilgrim should be able to open the app and quickly answer questions like:
- Where do I start?
- What should I do now?
- How do I get back to the most important actions?
- Where is emergency help or phrase support?
- How can I simplify the app if it feels overwhelming?

## 2.3 Feature-level promise
This feature family must feel:
- calm,
- welcoming,
- low-friction,
- readable,
- offline-capable,
- structurally simple,
- respectful of platform expectations.

---

# 3. Scope and boundaries

## 3.1 In scope
This feature family includes:
- startup resolution,
- first-launch detection,
- onboarding welcome behavior,
- language and initial preference setup,
- Home Root behavior,
- first-use empty and early-use states,
- urgent shortcut cluster behavior,
- pack-awareness summary behavior on Home,
- Simple Mode activation, persistence, and behavior,
- Simple Mode Home and shortcut entry surfaces,
- contextual routing from Home into Rituals, Maps, Group, Emergency, Phrasebook, and Tools.

## 3.2 Out of scope
This feature family does **not** include:
- deep ritual logic,
- map routing or saved-anchor persistence ownership,
- group membership truth,
- subscription or entitlement truth,
- pack installation lifecycle ownership,
- emergency-card content governance,
- phrasebook content governance,
- a disconnected alternate app for accessibility users,
- forcing a full permissions or account setup wizard on first launch.

## 3.3 Boundary with file `24`
Account, subscriptions, entitlements, and settings own:
- account gate behavior,
- Support this App surfaces,
- entitlement truth,
- local preference persistence authority.

This file owns the feature-facing meaning of onboarding, Home, and Simple Mode and may depend on preferences owned by file `24` such as selected language or simple-mode preference.

## 3.4 Boundary with file `11`
File `11` defines the canonical screen inventory and screen blueprint rules.
This file does not replace that screen-level contract.
It defines the feature-family behavior and policy that those screens must express.

## 3.5 Boundary with files `18`–`22`
Home and Simple Mode may launch directly into Rituals, Maps, Group, Planner, Phrasebook, or Emergency, but they do not own the deeper logic of those feature families.

## 3.6 Boundary with file `15`
Offline behavior, cached flags, pack manifest caching, and protected-state continuity rules come from file `15`.
This file applies those rules to first-use and Home behavior.

## 3.7 Boundary with file `09`
Platform-specific visual and native-bridge rules come from file `09`.
This file applies those rules specifically to onboarding, Home, and Simple Mode surfaces.

---

# 4. Product rules that govern this feature family

## 4.1 Home is a recovery surface, not a feature dump
Home must help the user resume, recover, and reach urgent help quickly.
It must not try to showcase every feature equally.

## 4.2 Onboarding must be short and task-oriented
Onboarding exists to get a user into a usable state quickly.
It must not become a feature dump, marketing carousel, or full settings wizard.

## 4.3 No forced account before value rule
The user must not be forced through account creation or sign-in before the local-first value of the app is clear.

## 4.4 No permission wall rule
The app must not request all permissions up front.
Permissions must be requested later, in context, when their value is clear.

## 4.5 Simple Mode is strategic, not cosmetic
Simple Mode must materially reduce cognitive load and make high-priority actions easier to reach.
It must not be a shallow theme toggle or a separate disconnected app.

## 4.6 Same product, reduced complexity rule
Simple Mode uses the same product truth, same feature families, and same data.
It reduces visible complexity and navigation burden without forking logic.

## 4.7 Urgent shortcut rule
Emergency help, phrase support, saved gate recall, and group safety actions must remain fast to reach from Home and Simple Mode.

## 4.8 Offline-first entry rule
If the app is opened without network, the startup and Home experience must still lead the user into local-capable value quickly.

## 4.9 Umrah-first rule
Onboarding and Home defaults must remain Umrah-first unless season and approved scope explicitly permit different behavior.
Hajj-specific complexity must not leak into the default first-use path.

## 4.10 Ethical monetization placement rule
Upgrade or Support this App messaging must never dominate first-use value and must never interrupt ritual-critical, emergency, or urgent recovery tasks.

---

# 5. Canonical terminology for this feature family

## 5.1 Startup Resolver
The system entry screen that resolves launch state and routes the user to the correct next screen.

## 5.2 Onboarding Welcome
The first-use entry flow that introduces the app’s value and continues the user into a usable state.

## 5.3 Language / Preferences Setup
The initial lightweight setup step for language and limited first-run preferences.

## 5.4 Home Root
The app’s primary dashboard or landing surface after onboarding/login state resolution.

## 5.5 Recovery surface
A screen designed to help the user resume, recover, or reach high-priority actions under stress.

## 5.6 Simple Mode
A simplified operating mode intended to reduce cognitive load and make high-priority actions easier to access.

## 5.7 Simple Home
The reduced-complexity Home entry surface shown when Simple Mode is active.

## 5.8 Urgent shortcut cluster
The group of high-priority actions on Home or Simple Mode that provides fast access to emergency, phrase support, saved gate, or group safety tasks.

## 5.9 First-use empty state
The state in which the user has not yet started a ritual session, saved an anchor, joined a group, or built personal planning context.

## 5.10 Personalized Home
The Home state after the app can show meaningful local or cached context such as an active ritual session, saved gate, planner items, or group summary.

---

# 6. User stories

## 6.1 First launch
- **As a first-time pilgrim**, I can start using the app quickly without being forced through sign-in or too many setup questions.
- **As a first-time pilgrim**, I can choose my language and see what to do next.
- **As a user with no network**, I can still land in a usable Home state.

## 6.2 Home and recovery
- **As a pilgrim**, I can open the app and see the most useful next step immediately.
- **As a stressed user**, I can reach emergency help, phrasebook, group, or my saved gate quickly.
- **As a returning user**, I can resume my ritual or recent map/group action without hunting.

## 6.3 Simple Mode
- **As an elderly or low-confidence user**, I can use a simpler home surface with bigger actions and less clutter.
- **As a user who prefers fewer choices**, I can keep Simple Mode on permanently.
- **As a user in Simple Mode**, I still reach the same canonical features and data as standard mode.

## 6.4 Early preparation
- **As a planner user**, I can notice useful pack readiness or reminder context without Home becoming crowded.
- **As a user exploring the app calmly before travel**, I can still use the standard mode and deeper sections without Simple Mode blocking me.

---

# 7. Startup Resolver behavior

## 7.1 Purpose
Startup Resolver exists to route the user to the correct next screen quickly and safely.

## 7.2 Canonical decision order
Startup Resolver should resolve launch state in a way that prioritizes:
1. app integrity and required local migrations,
2. deep-link or direct task intent when safe,
3. first-launch or onboarding-required state,
4. standard versus Simple Mode landing state,
5. protected-state refresh where it can happen without blocking local-first value.

## 7.3 Required startup inputs
The resolver may consider:
- whether onboarding is complete,
- selected language or locale preference,
- whether Simple Mode is enabled,
- whether a deep link is present,
- local ritual session state,
- saved local preferences,
- cached flags/manifest presence,
- account/auth state only when a deep-linked destination or required gate makes it relevant.

## 7.4 Non-blocking startup rule
The resolver must not wait on non-essential online calls before routing the user to a usable state.

## 7.5 Offline startup rule
If the app is offline at launch, Startup Resolver must still route the user into:
- onboarding if required,
- Simple Home if enabled,
- or Home Root,

using local state and cached data where available.

## 7.6 Deep-link rule
If a deep link points to a valid, meaningful task:
- it may bypass Home,
- but must still land the user in a coherent section context,
- and must fail safely back to Home or Simple Home if the destination cannot be resolved.

## 7.7 Startup error rule
Startup errors should be rare and minimal.
If a startup problem occurs, the app should favor recovery into a basic local-capable shell rather than trapping the user behind a dense error surface.

---

# 8. Onboarding behavior

## 8.1 Purpose
Onboarding exists to help the user understand the value of the app and reach a usable state quickly.

## 8.2 Onboarding scope rule
Onboarding is not:
- a full feature tour,
- a permissions gauntlet,
- a monetization wall,
- an account-creation funnel,
- a complex multi-step wizard.

## 8.3 Required onboarding jobs
The onboarding flow must:
- orient the user to the product’s purpose,
- let them confirm or choose language,
- optionally let them choose a simpler setup path,
- land them in a usable Home state with clear next actions.

## 8.4 Recommended onboarding structure
The default onboarding structure should be:
1. welcome/value screen,
2. language and minimal preferences setup,
3. optional simple-setup choice,
4. continue to Home or Simple Home.

## 8.5 Value framing rule
Onboarding must frame the app around the real jobs to be done:
- what to do next,
- what to do when unsure,
- how to stay oriented,
- how to coordinate,
- how to reach urgent help.

## 8.6 Skip rule
A user should be able to continue with essentials rather than being trapped in a long onboarding sequence.

## 8.7 Pack-awareness rule
Onboarding may lightly introduce offline packs or preparation value, but must not force pack install before the user has seen the Home experience.

## 8.8 Account rule
Onboarding must not push account creation unless the user explicitly chooses a protected feature later.

## 8.9 Supporter rule
Onboarding must not lead with Supporter conversion.
Any monetization message during early use must remain secondary, calm, and optional.

---

# 9. Language and initial preferences setup

## 9.1 Purpose
Language / Preferences Setup exists to establish a small number of first-run preferences that matter immediately.

## 9.2 Allowed first-run preferences
The initial setup may include only a small set of high-value preferences such as:
- app language or locale override,
- Simple Mode preference,
- possibly a preparation preference if product direction later approves one.

## 9.3 Forbidden first-run overload
Do not include large settings bundles such as:
- full pack management,
- detailed notification settings,
- extensive accessibility configuration already provided by the OS,
- complete profile/account editing,
- complex monetization choices.

## 9.4 Language selection rule
If locale selection is shown, it must be:
- fast,
- readable,
- searchable if necessary,
- resilient to unsupported locale fallback.

## 9.5 Preference persistence rule
Selected language and Simple Mode preference are stored as device-local settings according to file `24` and must apply immediately.

## 9.6 Unsupported-locale fallback rule
If the preferred device locale is unsupported, the user should still be able to confirm a reasonable default and continue quickly.

## 9.7 No permission request rule
This screen must not request location, notifications, BLE, media, or account permissions directly unless a later approved design change makes one permission genuinely essential at this exact point.

---

# 10. Home Root behavior

## 10.1 Purpose
Home Root is the calm control surface for resume, recovery, and quick access to high-priority actions.

## 10.2 Home’s primary job
Home must answer these questions quickly:
- What should I do next?
- How do I resume my current journey?
- Where is urgent help?
- How do I reach my map or saved gate?
- How do I get back to my group or check in?

## 10.3 Canonical content priority order
Home should prioritize content in roughly this order:
1. current ritual guidance / quick start,
2. urgent shortcut cluster,
3. saved gate or recent map action,
4. active group summary if applicable,
5. planner/reminder summary,
6. pack readiness or preparation summary if useful,
7. lower-priority entry surfaces such as tools or settings.

## 10.4 Home content blocks
Home may include, where relevant:
- active ritual status card or Start Umrah card,
- urgent shortcut cluster,
- saved gate / recent map card,
- group summary card,
- planner/reminder summary card,
- non-blocking safety banner strip,
- pack readiness/preparation card,
- low-priority Settings or Tools entry.

## 10.5 Home must avoid
Home must avoid:
- exposing too many equal-priority actions,
- forcing horizontal browsing to find core tasks,
- acting like a stats dashboard,
- leading with decorative content,
- surfacing stale protected data as if it were unquestionably current.

## 10.6 Home default states
Home must support:
- first-use empty / onboarding-oriented state,
- normal personalized state,
- offline local-only state,
- stale remote-summary state,
- minimal error state if supportive remote content fails.

## 10.7 Home routing rule
Primary Home actions must land users in coherent section contexts such as:
- Rituals Root or active ritual flow,
- Map Root,
- Group Root,
- Emergency Root,
- Tools Root.

## 10.8 Safety-banner rule
If a current safety banner exists, Home may render it in a non-blocking strip near the top.
This strip must remain calm, short, and dismissible as defined in file `22`.

## 10.9 Upgrade placement rule
Supporter prompts or pack upsell cues on Home must remain secondary and must never outrank urgent shortcuts, current ritual recovery, or emergency access.

---

# 11. First-use Home state

## 11.1 Purpose
First-use Home exists to help the user begin a meaningful journey without showing empty product machinery.

## 11.2 Required first-use emphasis
If the user has no active ritual, no saved gate, no group, and no planner context, Home should emphasize:
- Start Umrah or equivalent ritual entry,
- emergency/phrase support shortcut,
- map/save gate education only in a lightweight way,
- calm explanation that more personal context appears after use.

## 11.3 First-use empty-state rule
Empty states on Home should feel encouraging and action-oriented, not barren or technical.

## 11.4 First-use pack awareness
Pack awareness may appear as a lightweight preparation card or reminder, but should not overwhelm the first-use Home surface or imply the app is unusable without a pack.

## 11.5 First-use group behavior
If the user has no active group, Home may omit the group summary card or show a low-priority Join Group shortcut, but it must not crowd the top of the screen.

---

# 12. Personalized Home state

## 12.1 Purpose
Personalized Home exists once the app can show meaningful local or cached context.

## 12.2 Ritual priority rule
If an active ritual session exists, the ritual card should usually be the primary Home card.
Home should help the user resume where they left off rather than rediscover the correct section.

## 12.3 Saved gate / recent map behavior
If the user has a saved anchor or recent recovery action, Home should offer a fast return to it.
If no anchor exists, Home may suggest Save My Gate at appropriate times without becoming repetitive.

## 12.4 Group summary behavior
If the user has an active group snapshot, Home may surface:
- latest regroup context,
- latest safe-status relevance,
- quick entry to Group.

It must not imply live tracking by default.

## 12.5 Planner summary behavior
Planner summary on Home should remain lightweight, such as:
- next reminder,
- today’s next item,
- overdue local item.

It must not turn Home into a full planner dashboard.

## 12.6 Pack readiness summary behavior
Home may show useful pack-preparation or storage readiness context when:
- the app can infer genuine value,
- a pack is missing for a relevant upcoming journey,
- the card does not crowd out more urgent tasks.

## 12.7 Stale data rule
If group, entitlement, or other protected/supportive data is stale, Home must reflect that honestly where the distinction matters.

---

# 13. Urgent shortcut architecture

## 13.1 Purpose
Urgent shortcuts exist because many users will reach Home or Simple Home while stressed, lost, or cognitively overloaded.

## 13.2 Canonical urgent shortcuts
The canonical urgent shortcuts may include:
- Phrasebook,
- Emergency,
- Save My Gate / open Map,
- I’m Safe / open Group.

## 13.3 Shortcut priority rule
Urgent shortcuts must remain easy to see and easy to tap, especially on smaller screens and in large-text contexts.

## 13.4 Shortcut ownership rule
These shortcuts are owned here as entry architecture, but the deeper behaviors remain owned by the destination feature families.

## 13.5 Dynamic label rule
Shortcuts may adapt labels based on context where helpful, for example:
- `Map` versus `My Gate`,
- `Group` versus `I’m Safe`,

but must preserve clarity.

## 13.6 No clutter rule
The urgent shortcut cluster must remain small.
Do not turn it into a grid of every feature.

---

# 14. Simple Mode behavior

## 14.1 Purpose
Simple Mode exists to reduce cognitive load and make high-priority tasks easier to access for users who struggle with dense navigation or changing UI states.

## 14.2 Product meaning
Simple Mode is a supported operating mode of the same app.
It is not:
- a separate app,
- an elderly-only label,
- a child mode,
- a stripped product with different data truth.

## 14.3 Activation entry points
Simple Mode may be activated from:
- onboarding’s simple setup choice,
- Settings Root,
- possibly a contextual suggestion surface if the product later adds one carefully.

## 14.4 Persistence rule
Simple Mode preference is device-local and should persist across launches until the user changes it.

## 14.5 Default landing rule
When Simple Mode is enabled, the app should land users on `simple_home` instead of standard `home_root` unless a deep link or protected route requires something else.

## 14.6 Simple Mode core changes
Simple Mode may change:
- visible complexity,
- card density,
- action sizing,
- copy brevity,
- navigation emphasis,
- visual treatment,
- first-screen priority.

It must **not** change:
- core feature ownership,
- data truth,
- entitlement meaning,
- offline guarantees,
- privacy boundaries.

## 14.7 Simple Mode priority order
Simple Mode should prioritize, in order:
1. Start/Resume Ritual,
2. Save My Gate / Map,
3. I’m Safe / Group,
4. Phrasebook / Emergency,
5. one low-priority more/help/settings path.

## 14.8 Reduced-surface rule
Simple Mode should intentionally hide or de-emphasize low-priority browsing and exploratory content by default.

## 14.9 Clear exit rule
The user must always be able to leave Simple Mode through a clear settings or mode toggle path.

---

# 15. Simple Home behavior

## 15.1 Purpose
Simple Home is the reduced-complexity root screen shown when Simple Mode is active.

## 15.2 Required content blocks
Simple Home should contain at minimum:
- Start / Resume Ritual,
- Save My Gate / Map,
- I’m Safe / Group,
- Phrasebook / Emergency,
- optional one compact context card such as active ritual state or saved gate summary,
- optional low-priority entry to More / Settings.

## 15.3 Optional context block rule
Simple Home may show only one or two supporting context blocks beyond the core shortcuts.
It must not grow into a miniature version of the full Home dashboard.

## 15.4 Active ritual shortcut state
If an active ritual session exists, Simple Home should strongly favor Resume Ritual rather than generic start language.

## 15.5 Group shortcut state
If the user has an active group, the shortcut may emphasize `I’m Safe` or `Group` based on context.
If not, it may still route to Group Root without implying hidden live membership.

## 15.6 Map shortcut state
If the user has a saved gate or recent anchor, the shortcut should favor that recovery language rather than generic map exploration language.

## 15.7 Emergency visibility rule
Emergency/Phrasebook access must remain obvious and never be displaced by secondary content.

## 15.8 Offline rule
Simple Home must remain usable offline and must not assume live summaries are available.

---

# 16. Simple shortcut screens

## 16.1 Purpose
Simple shortcut screens exist only to provide simplified framing and routing into canonical task flows.

## 16.2 Canonical shortcuts
The canonical shortcut surfaces are:
- `simple_ritual_shortcut`
- `simple_map_shortcut`
- `simple_group_shortcut`
- `simple_emergency_shortcut`

## 16.3 Reuse rule
These shortcut surfaces should reuse canonical destination screens or flows wherever possible instead of duplicating product logic.

## 16.4 Allowed simplification
A simple shortcut surface may:
- simplify copy,
- simplify choice count,
- enlarge targets,
- remove low-value secondary actions.

It must not create conflicting logic, separate data stores, or independent state machines.

## 16.5 Emergency shortcut rule
The emergency shortcut must remain the most fail-safe and least visually complex of the shortcut surfaces.

---

# 17. Platform and visual adaptation rules

## 17.1 Shared product rule
Onboarding, Home, and Simple Mode share the same information architecture and product behavior on iOS and Android.
Presentation may adapt by platform.

## 17.2 iOS design goal for this family
On iOS, these surfaces should feel refined, calm, layered, and structurally aligned with current platform expectations.

## 17.3 iOS Liquid Glass usage rule
On iOS, Liquid-Glass-like treatment is allowed only where it improves hierarchy and calmness without harming readability.
Preferred zones for this feature family include:
- top bars,
- bottom/tab chrome,
- lightweight floating shortcut trays,
- selected filter or quick-action chips,
- selected hero or section headers where text remains legible.

## 17.4 iOS discouraged zones
On iOS, glass/material treatment should be reduced or avoided on:
- dense onboarding explanation text,
- large ritual or safety instruction cards,
- emergency emphasis surfaces,
- dense settings or form-like surfaces,
- any large-text or reduced-transparency context where clarity would suffer.

## 17.5 Android expression rule
Android should use stronger solid/elevated surfaces and Android-appropriate motion rather than imitate Liquid Glass literally.

## 17.6 Home visual hierarchy rule
Visual layering must reinforce content priority.
Current ritual, urgent shortcuts, and recovery surfaces must never be obscured by decorative chrome or hero treatment.

## 17.7 Simple Mode visual rule
Simple Mode should generally use stronger solids, reduced visual ornament, and clearer separators even on iOS.
Its job is clarity first, not visual expressiveness.

## 17.8 Accessibility adaptation rule
If reduced transparency, increased contrast, large text, or similar accessibility settings are active, these surfaces must favor clarity over decorative material effects.

---

# 18. Data and local preference behavior

## 18.1 Ownership rule
Local preference authority lives in file `24`, and device-local persistence categories live in file `13`.
This file defines the feature-facing meaning of those values.

## 18.2 Representative locally relevant values
This feature family may depend on local values such as:
- onboarding completion state,
- onboarding version seen,
- selected language or locale override,
- Simple Mode enabled state,
- support prompt dismissal state,
- selected Home presentation preferences if later approved.

## 18.3 Required invariants
- onboarding completion must be explicitly persisted,
- Simple Mode must persist locally,
- startup routing must not depend on network to read these values,
- resetting onboarding must not corrupt unrelated user-local data.

## 18.4 No duplicate truth rule
Do not create duplicate “home config” or “simple mode store” logic outside the canonical local preference and settings ownership boundaries.

---

# 19. Screen and UX contract for this feature family

## 19.1 Canonical screens
This feature family owns or strongly depends on:
- `startup_resolver`
- `onboarding_welcome`
- `language_preferences_setup`
- `home_root`
- `simple_home`
- `simple_ritual_shortcut`
- `simple_map_shortcut`
- `simple_group_shortcut`
- `simple_emergency_shortcut`

## 19.2 Startup Resolver UX contract
### Required content blocks
- minimal branding / launch surface,
- no dense content,
- no distracting loading dashboard.

### Required states
- initializing,
- rare startup error,
- offline-capable routing path.

### Rule
Resolve quickly and route to usable state.

## 19.3 Onboarding Welcome UX contract
### Required content blocks
- concise value framing,
- continue action,
- optional choose language inline or handoff,
- optional continue with essentials or simple setup path.

### Required states
- default,
- locale fallback,
- offline still usable.

### Rule
Keep it short and task-oriented.

## 19.4 Language / Preferences Setup UX contract
### Required content blocks
- language selection,
- Simple Mode preference if shown here,
- continue action,
- clear default choice presentation.

### Required states
- default,
- unsupported locale fallback,
- persisted selection applied.

### Rule
Do not overload with many settings.

## 19.5 Home Root UX contract
### Required content blocks
- ritual status/start card,
- urgent shortcut cluster,
- saved gate/recent map card,
- group summary if applicable,
- planner/reminder summary,
- pack readiness summary if useful,
- optional non-blocking safety banner strip.

### Required states
- first-use empty,
- personalized content,
- offline local-only,
- stale remote summary,
- supportive remote-summary failure.

### Rule
Home is a recovery surface, not a cluttered dashboard.

## 19.6 Simple Home UX contract
### Required content blocks
- large primary shortcuts,
- optional one or two context cards,
- low-priority settings/more path,
- clear exit path from Simple Mode.

### Required states
- default,
- offline local-only,
- active ritual state,
- saved gate present/not present,
- active group present/not present.

### Rule
This is a simplified lens onto the same product, not a disconnected second app.

## 19.7 Simple shortcut UX contract
### Required content blocks
- large primary action,
- simplified short explanation,
- route into canonical destination,
- clear back or cancel path.

### Required states
- default,
- offline/degraded when destination is affected,
- unavailable only when canonical destination genuinely unavailable.

### Rule
Do not duplicate destination logic.

---

# 20. Copy, localization, RTL, and accessibility rules

## 20.1 Copy tone
Onboarding, Home, and Simple Mode copy must be:
- calm,
- direct,
- reassuring,
- action-oriented,
- low on jargon,
- never salesy in early-use or urgent contexts.

## 20.2 Onboarding copy rule
Prefer concise framing such as:
- “Know what to do.”
- “Recover when unsure.”
- “Stay oriented and get help quickly.”

Avoid dense feature lists or marketing flourishes.

## 20.3 Home copy rule
Home copy should help the user act, not admire the product.
Examples:
- “Start Umrah”
- “Resume your ritual”
- “Find your gate”
- “I’m Safe”
- “Open Phrasebook”
- “Emergency help”

## 20.4 Simple Mode copy rule
Simple Mode copy must be even shorter and clearer than standard mode.
It should avoid dense labels or exploratory language.

## 20.5 Ethical copy rule
Early-use and Home surfaces must not imply:
- that sign-in is required for the whole app,
- that safety/correctness is being sold,
- that Supporter value outranks urgent help.

## 20.6 RTL and mixed-content rule
Shortcut labels, pack names, map terms, join codes, dates, and mixed-language strings must remain bidi-safe and readable in RTL layouts.

## 20.7 Accessibility requirements
These surfaces must support:
- large text,
- obvious focus order,
- strong tap targets,
- non-color-only meaning,
- reduced-motion-safe transitions,
- reduced-transparency-safe surfaces,
- screen-reader clarity for primary shortcuts and mode toggles.

## 20.8 Simple Mode accessibility rule
Simple Mode should be especially safe for:
- low-vision users,
- motor-limited users,
- cognitively overloaded users,
- users who struggle with nested navigation.

---

# 21. Offline behavior and degraded states

## 21.1 Offline tier
This feature family is strongly local-first for its own essential behavior.

## 21.2 Offline guarantees
The following must remain meaningful offline:
- startup resolution using local state,
- onboarding flow continuation,
- Home Root local-capable content,
- Simple Home shortcuts into local-first destinations,
- use of local ritual, saved anchor, planner, and safety context.

## 21.3 Cached support-state rule
When supportive server-backed state such as group summary, flags, or entitlement snapshot is stale, Home may still show it if the UI clearly indicates its stale nature where needed.

## 21.4 No-network first launch rule
A first-launch user with no network must still be able to:
- complete onboarding,
- reach Home or Simple Home,
- start local-capable journeys such as ritual guidance and urgent help.

## 21.5 No-fake-truth rule
Home must not present live group, entitlement, or pack state as unquestionably current if it is only cached.

---

# 22. Security and privacy rules for this feature family

## 22.1 Minimal personal-data rule
Home and onboarding should not expose unnecessary personal data.

## 22.2 No hidden tracking rule
Shortcut architecture must not imply hidden location or presence tracking.
It must route into the privacy-light behaviors owned by Maps and Group.

## 22.3 No hidden monetization profiling rule
These surfaces should not accumulate aggressive monetization profiling or conversion logic beyond what is necessary for respectful product improvement.

## 22.4 Local preference privacy rule
Onboarding completion and Simple Mode preference remain app-private device-local settings by default.

---

# 23. Analytics and observability requirements

## 23.1 Canonical analytics events
This feature family must emit the canonical screen and journey events from file `17` where relevant, including at minimum:
- `screen_home_view`
- `app_launch_start`
- `app_launch_complete`
- `session_start`
- `settings_preference_change` when Simple Mode or related app-level preferences change.

## 23.2 Onboarding telemetry naming rule
Because file `17` currently centers explicit onboarding-related telemetry less than feature-family telemetry, onboarding events in this feature family should use canonically governed screen or journey patterns such as:
- `screen_onboarding_welcome_view`
- `screen_language_preferences_setup_view`
- `journey_onboarding_complete`
- `journey_simple_mode_enable`

These names must be governed consistently with file `17` conventions.

## 23.3 Suggested feature parameters where relevant
- `simple_mode_enabled`
- `surface`
- `entry_point`
- `season`
- `network_state`
- `has_active_ritual`
- `has_saved_anchor`
- `has_active_group`
- `has_planner_items`

## 23.4 Privacy-light analytics rule
Do not log sensitive personal data, emergency details, or hidden location traces from Home or onboarding flows.

## 23.5 Observability priorities
High-signal issues include:
- startup routing failures,
- onboarding completion-state corruption,
- Home personalization regressions,
- incorrect Simple Mode persistence,
- shortcut misrouting,
- stale protected-state misrepresentation on Home.

---

# 24. Testing and validation requirements

## 24.1 Required automated coverage
Automated tests must cover at minimum:
- startup routing decisions,
- first-launch vs returning-user routing,
- onboarding completion persistence,
- language preference application,
- Simple Mode enable/disable persistence,
- Home card priority rules,
- urgent shortcut routing,
- offline Home and offline onboarding behavior,
- stale remote-summary labeling behavior,
- deep-link fallback to Home or Simple Home when destination fails.

## 24.2 Required manual/device validation
Manual or device validation must cover at minimum:
- first launch with network,
- first launch without network,
- onboarding skip / continue with essentials,
- onboarding with Simple Mode selected,
- returning launch into standard Home,
- returning launch into Simple Home,
- large-text Home and Simple Home usability,
- reduced-transparency and contrast behavior on iOS,
- Android elevated-surface Home behavior,
- emergency shortcut discoverability,
- ritual resume from Home,
- saved gate recall entry from Home.

## 24.3 Real-world validation requirement
Before release, representative field validation should confirm:
- first-time pilgrims understand where to begin,
- stressed users can reach emergency or phrase support quickly,
- elderly or low-confidence users can complete key actions in Simple Mode,
- Home remains calm rather than crowded,
- platform-adapted chrome does not harm readability or action clarity.

## 24.4 Fake-success warning
A visually attractive Home mockup is not enough evidence.
Release confidence requires real-device validation of onboarding speed, shortcut discoverability, offline routing, Simple Mode clarity, and accessibility behavior.

---

# 25. Definition of done for this feature family

This feature family is not ready for release unless all of the following are true:
- onboarding is short and gets the user to a usable state quickly,
- account creation is not forced before value,
- Home behaves as a calm recovery surface rather than a feature dump,
- urgent shortcuts are fast to reach and route correctly,
- Simple Mode materially reduces complexity without forking product logic,
- offline first launch and offline Home remain meaningful,
- iOS Liquid-Glass-like treatment is used selectively and legibly,
- Android remains platform-appropriate rather than imitating iOS,
- analytics hooks align with file `17`,
- real-device validation confirms that these surfaces reduce confusion under stress.

---

# 26. Cross-file dependency rules

## 26.1 If onboarding or Home priorities change
Update:
- this file,
- file `10`,
- file `11`,
- file `12` if user-facing copy changes,
- file `05` if roadmap or status meaning changes.

## 26.2 If Simple Mode scope changes
Update:
- this file,
- file `10`,
- file `11`,
- file `24` if preference ownership or persistence changes,
- file `27` and `28` where validation requirements change.

## 26.3 If startup routing changes
Update:
- this file,
- file `11`,
- file `15` if offline assumptions change,
- file `17` if telemetry changes,
- tests and startup fixtures.

## 26.4 If Home shortcut architecture changes
Update:
- this file,
- destination feature-family files as needed,
- file `10` and `11`,
- file `12` if copy or accessibility expectations change.

## 26.5 If iOS or Android visual adaptation policy changes for these surfaces
Update:
- this file,
- file `08`,
- file `09`,
- file `11` where screen contracts are affected,
- file `27` if device-lab expectations change.

---

# 27. Anti-patterns forbidden by this document

The following are forbidden unless explicitly approved.

## 27.1 Turning onboarding into a long feature dump
Forbidden.

## 27.2 Forcing sign-in or purchase setup before users can see core value
Forbidden.

## 27.3 Exposing too many equal-priority actions on Home
Forbidden.

## 27.4 Treating Home as a stats dashboard or marketing billboard
Forbidden.

## 27.5 Creating Simple Mode as a separate second app with divergent logic
Forbidden.

## 27.6 Letting Simple Mode become only a visual skin with no real complexity reduction
Forbidden.

## 27.7 Using heavy translucency or glass treatment where readability suffers
Forbidden.

## 27.8 Hiding emergency or urgent assistance behind secondary navigation
Forbidden.

## 27.9 Making first-use or Home require network to be meaningful
Forbidden.

## 27.10 Showing stale protected state as if it were live truth on Home
Forbidden.

---

# 28. Implementation priorities

## 28.1 Phase 1 priorities
Implement first:
- startup resolver,
- onboarding welcome,
- language and simple-mode setup,
- Home Root baseline with calm card hierarchy,
- urgent shortcut cluster,
- offline-capable first-use and returning-home behavior,
- Simple Home baseline.

## 28.2 Phase 2 priorities
Then add:
- better Home personalization,
- pack-readiness summary,
- safety-banner strip on Home,
- simplified shortcut framing screens,
- platform adaptation polish.

## 28.3 Phase 3 priorities
Then refine:
- field-tested card ranking improvements,
- smarter but calm early-use education,
- richer context-aware shortcut labeling,
- post-launch simplification based on real confusion data.

---

# 29. When this file must be updated

This file must be updated whenever any of the following changes:
- startup routing behavior,
- onboarding scope or structure,
- language/setup behavior,
- Home priorities or card hierarchy,
- urgent shortcut architecture,
- Simple Mode behavior or scope,
- Home platform-adaptation policy,
- analytics hooks for first-use or Home surfaces,
- release-evidence expectations tied to onboarding, Home, or Simple Mode.

If these truths change but this file is not updated, UX implementation, QA, and cross-feature routing will drift quickly.

---

# 30. Summary

This file defines the canonical feature-facing contract for onboarding, Home, and Simple Mode in Pilgrims Mobile App.

It establishes:
- how startup resolution works,
- how first launch and onboarding behave,
- how Home functions as a calm recovery surface,
- how urgent shortcuts are structured,
- how Simple Mode reduces complexity without becoming a second product,
- how these surfaces behave offline,
- how iOS Liquid Glass and Android adaptation rules apply here,
- what analytics, testing, and release-readiness expectations must be met.

Its purpose is to ensure the app’s entry and recovery experience remains:
- calm,
- understandable,
- accessible,
- offline-capable,
- and safe for long-term AI-assisted implementation.

