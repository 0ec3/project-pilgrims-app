# 24 — FEATURE: ACCOUNT, SUBSCRIPTIONS, ENTITLEMENTS, AND SETTINGS

## Document status
- **Type:** Normative feature-family specification
- **Priority:** Highest
- **Audience:** Founder, product lead, backend engineers, Flutter engineers, design lead, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical feature contract for account access, authentication gating, subscriptions, purchase validation and restore behavior, entitlement truth, downgrade/refund handling, settings ownership, local preference behavior, and release-readiness expectations.
- **Authority level:** This file is the canonical source of truth for account-facing product behavior, subscription UX, entitlement-driven lock states, restore flows, and settings ownership. If implementation, UI, or tests diverge from this file, this file wins unless a higher-level normative contract or approved decision record explicitly changes it.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`, `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`, `10-PERSONAS-IA-USER-JOURNEYS-AND-TASK-FLOWS.md`, `11-SCREENS-STATES-NAVIGATION-AND-UI-BLUEPRINTS.md`, `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`, `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`, `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `17-ANALYTICS-OBSERVABILITY-AND-PERFORMANCE-BUDGETS.md`
- **Related files:** `18`, `19`, `20`, `21`, `22`, `23`, `25`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This file exists because account/auth, subscription behavior, entitlement enforcement, and settings are trust-boundary features.

If this feature family is vague, teams and AI agents create especially dangerous problems:
- account creation gets forced too early and harms first-use value,
- client code starts inventing entitlement state instead of trusting the server,
- paid-vs-free boundaries drift inconsistently across modules,
- restore and downgrade behavior becomes unreliable or misleading,
- platform store differences are ignored and the product promises impossible parity,
- local settings are scattered across many modules without ownership,
- sensitive protected state is shown as current when it is only cached,
- sacred or safety-critical flows become polluted by poorly placed upgrade prompts.

This file prevents those failures by defining:
- what this feature family is responsible for,
- what the user can and cannot expect from account and subscription behavior,
- how sign-in gating works,
- how purchases, restore, downgrade, and refund handling work,
- how entitlement truth is obtained and cached,
- what Settings owns,
- how other feature families must depend on this module.

---

# 2. Feature purpose and user value

## 2.1 Feature family purpose
This feature family exists to help the user:
- access trusted online features only when necessary,
- understand and manage Supporter status clearly,
- restore purchases safely,
- keep preferences and app behavior understandable,
- trust what is free, what is paid, and what remains available offline.

## 2.2 Main user value statement
A pilgrim should be able to open account and settings surfaces and quickly answer questions like:
- Do I need to sign in for this?
- Am I a Supporter right now?
- Why is this feature locked or unavailable?
- How do I restore my purchase on this device?
- What app preferences can I safely control?
- How do I manage subscriptions or privacy-related settings without getting lost?

## 2.3 Feature-level promise
This feature family must feel:
- calm,
- trustworthy,
- low-friction,
- explicit about protected versus local state,
- ethically monetized,
- platform-aware without becoming fragmented.

---

# 3. Scope and boundaries

## 3.1 In scope
This feature family includes:
- optional account gate behavior,
- account/profile viewing and editing where supported,
- Support this App / subscription entry surfaces,
- native purchase initiation handoff,
- restore purchase flow,
- trusted entitlement refresh behavior,
- downgrade, cancel, and refund reflection behavior,
- lock-state and upgrade messaging rules,
- settings-root information architecture,
- local preference ownership and persistence rules,
- permission-summary and system-settings redirection surfaces,
- sign-out and re-auth behavior for protected features.

## 3.2 Out of scope
This feature family does **not** include:
- identity-provider implementation internals,
- direct store receipt validation logic in Flutter feature code,
- backend webhook implementation details,
- ads,
- payment wallet behavior,
- cross-device sync of general local feature data,
- broad customer-support operations tooling,
- feature-specific settings that properly belong inside another feature unless this file explicitly claims the preference surface.

## 3.3 Boundary with file `13`
File `13` defines the canonical server-side data model for `profiles`, `user_entitlements`, and `purchase_receipts`, plus the local rule that settings and UX dismissals are device-local.
This file does not redefine those persistence truths. It defines the user-facing and runtime behavior built on top of them.

## 3.4 Boundary with file `14`
File `14` defines the HTTP contracts for `GET /v1/entitlements`, `POST /v1/purchases/validate`, and `POST /v1/purchases/restore`.
This file defines how those APIs are used in product behavior and how users experience them.

## 3.5 Boundary with file `15`
File `15` defines the offline snapshot and refresh policy for entitlements and other protected state.
This file applies those rules to account and settings UX.

## 3.6 Boundary with files `18`–`23`
Other feature families do not own entitlement truth.
They may react to entitlements or settings, but the authoritative meaning of gates, restore behavior, and account gating belongs here.

## 3.7 Boundary with file `29`
Deep privacy, compliance, and risk controls belong to file `29`.
This file only defines the feature-facing privacy and user-trust behavior required at runtime.

---

# 4. Product rules that govern this feature family

## 4.1 No forced account before value rule
The app must not force sign-in at first launch unless product direction changes.
Authentication should be requested only when a trusted online feature actually requires it.

## 4.2 No paywall on correctness or safety rule
Supporter must never gate:
- ritual correctness,
- RIC access,
- baseline map recovery,
- phrase text,
- emergency tools,
- basic group join and manual coordination fallback.

## 4.3 Server-truth entitlement rule
The client may cache entitlement snapshots for continuity, but the server remains authoritative.
The app must not invent, extend, or silently assume Supporter access.

## 4.4 Ethical upgrade placement rule
Upgrade messaging must never interrupt ritual-critical, emergency, or recovery-critical tasks.

## 4.5 Platform-difference honesty rule
The product-level meaning of `FREE` and `SUPPORTER` must remain shared, but store, restore, and family-related behavior may differ by platform.
Do not promise identical store behavior where the platforms do not offer it.

## 4.6 Settings are not a junk drawer rule
Settings must expose clear account, preference, privacy, and app-management options without becoming a dumping ground for unrelated feature configuration.

## 4.7 Protected-state honesty rule
If entitlement or account state is stale, unverified, or offline-only, the UI must reflect that clearly where the distinction matters.

## 4.8 Calm copy rule
Account and subscription copy must stay calm, grateful, and respectful.
It must not shame free users or use aggressive monetization language.

---

# 5. Canonical terminology for this feature family

## 5.1 Account gate
A screen or flow that requests authentication only because a protected action requires it.

## 5.2 Profile
The server-backed app-specific user metadata row linked 1:1 with the authenticated user.

## 5.3 Supporter
The paid tier that unlocks selected convenience and offline-enrichment features while preserving ethical free access boundaries.

## 5.4 Entitlement snapshot
The normalized trusted access state returned by the backend, including tier and gates.

## 5.5 Restore purchase
The user-initiated action that asks the app and backend to recover the current trusted entitlement state from store-linked purchase history.

## 5.6 Lock state
A screen or feature state where a richer variant is unavailable because of entitlement, platform support, missing pack, or other controlled reason.

## 5.7 Settings Root
The canonical screen for account, preferences, privacy, support, and app-management options.

## 5.8 Support this App
The user-facing subscription and restore entry surface.

## 5.9 Auth-linked settings
Settings that only make sense when the user has an authenticated account context.

## 5.10 Local preference
A device-local user preference or UX-management toggle that is not server-authoritative by default.

---

# 6. User stories

## 6.1 Optional account access
- **As a new pilgrim**, I can use the app without creating an account until I need a protected online feature.
- **As a user**, if I try to join a group or restore purchases, the app explains why sign-in is needed.

## 6.2 Supporter and restore
- **As a user**, I can see what Supporter provides without being pressured during sacred or urgent flows.
- **As a user**, I can initiate purchase or restore from a clear trusted surface.
- **As a user**, if restore fails or I am offline, I understand what happened and what to do next.

## 6.3 Settings and preferences
- **As a user**, I can manage language, app behavior, download preferences, and notification-related settings without hunting through many screens.
- **As a user**, I can open system settings when a permission or platform setting matters.

## 6.4 Downgrade and continuity
- **As a downgraded or refunded user**, I can still use the free features calmly and understand what changed.
- **As an offline user**, I do not see fake current entitlement certainty when the app cannot verify it.

---

# 7. Account and authentication behavior

## 7.1 Identity source rule
`auth.users` remains the canonical authentication identity source.
The product must not create a parallel credentials system for app sign-in.

## 7.2 Profile rule
`profiles` store app-specific metadata linked 1:1 with the authenticated user.
The feature family may surface editable profile information such as display name or optional phone-display metadata where supported.

## 7.3 Auth method posture
The exact low-friction sign-in method may evolve beneath this contract, but it must:
- produce a valid authenticated user identity,
- remain practical for mobile pilgrimage use,
- avoid unnecessary complexity before value is established.

## 7.4 Optional account gate rule
Account gating is triggered only for trusted or account-linked features such as:
- group join,
- purchase restore or validate,
- protected account settings,
- other future approved protected operations.

## 7.5 No-first-launch-auth rule
The app must not require authentication before users can explore the local-first core experience.

## 7.6 Re-auth rule
If a JWT expires or protected refresh fails due to auth state:
- protected reads/writes must stop,
- local-only features must remain usable,
- the user should be routed to a safe re-auth path only when needed.

## 7.7 Sign-out rule
Signing out should:
- remove authenticated access to protected server features,
- preserve device-local data that is intentionally local-first unless a separate explicit delete action exists,
- clear cached protected snapshots or mark them unusable according to security policy.

## 7.8 No misleading anonymous-account language rule
If the user is not signed in, the product must explain the practical consequence clearly rather than implying the app is broken.

## 7.9 Account deletion availability rule
If the product offers account creation or maintains server-backed personal data, authenticated users must be able to find a clear delete-account / data-deletion path from Settings Root.
This path may be an immediate in-app delete flow, a governed request flow, or a clearly explained handoff, but it must not be hidden behind support-only email copy or undocumented support channels.

## 7.10 Web deletion handoff rule
Where store policy or legal/compliance posture requires an external deletion resource, the app must expose a trusted web handoff from the same account/data-management area.
The hosted page or support flow may live outside the app, but discoverability from the app remains this feature family’s responsibility.

---

# 8. Subscriptions and product offering behavior

## 8.1 Product posture
The app offers a free baseline and a Supporter tier.
The purpose of Supporter is to fund operations, translations, accessibility, maps, audio, and maintenance while preserving ethical access boundaries.

## 8.2 Free baseline
Free access must continue to include the baseline capabilities already defined across the feature-family files.
This file does not override those free guarantees.

## 8.3 Supporter value categories
Supporter may unlock convenience and enrichment such as:
- offline pack conveniences,
- offline audio,
- live group board,
- smart planner suggestions,
- extended notes/bookmarks capability.

## 8.4 Subscription-group posture
The paid tier should be exposed to the user as one coherent Supporter offering even if store-side product IDs, durations, or future levels differ internally.

## 8.5 No billing sprawl rule
The app must not surface a confusing matrix of plans or billing jargon unless product strategy later expands deliberately.

## 8.6 Regionalized pricing rule
Displayed pricing should respect platform/store regionalization and must not hardcode one global amount in product copy.

## 8.7 Trial and intro-offer posture
If a trial or introductory offer is enabled, it must be disclosed clearly and must not create hidden assumptions elsewhere in the product.
Any server-enforced trial limits must remain product-governed and documented.

---

# 9. Canonical entitlement model

## 9.1 Entitlement truth
The canonical trusted source of entitlement truth is the server-backed `user_entitlements` record and the normalized entitlement responses from the authenticated API.

## 9.2 Tier values
The canonical high-level tier values are:
- `FREE`
- `SUPPORTER`

## 9.3 Gate snapshot
The current normalized gate snapshot includes at minimum:
- `PACK_AUTO_DOWNLOAD`
- `AUDIO_OFFLINE`
- `SMART_PLANNER`
- `GROUP_LIVE_BOARD`
- `NOTES_BOOKMARKS_EXTENDED`

## 9.4 Gate semantics rule
Gate meanings are centralized here and must not be reinterpreted independently in feature modules.

### `PACK_AUTO_DOWNLOAD`
Allows Supporter convenience behavior for auto-download flows when user consent and network/device conditions permit.

### `AUDIO_OFFLINE`
Allows offline audio pack access where supported by content and pack state.

### `SMART_PLANNER`
Allows supportive planner suggestions where approved.

### `GROUP_LIVE_BOARD`
Allows richer live-board access where group authorization also permits it.

### `NOTES_BOOKMARKS_EXTENDED`
Allows richer notes/bookmarks features such as markdown, tags, multiple attachments, and richer export according to the personal-tools feature contract.

## 9.5 Legacy alias rule
Older materials may refer to `NOTES_BOOKMARKS`.
Current implementation and tests must treat `NOTES_BOOKMARKS_EXTENDED` as authoritative while preserving compatibility awareness where legacy references still exist.

## 9.6 Entitlement-response contract
The canonical normalized entitlement response includes:
- `tier`
- optional `active_until`
- `source`
- `gates`
- optional `last_validated_at`

## 9.7 Source rule
`source` is a normalized backend value such as a store/provider source string.
Flutter feature code must not infer product meaning from raw provider receipts or transaction details.

---

# 10. Purchase, validate, and restore behavior

## 10.1 Purchase initiation rule
Purchase initiation occurs through the platform-native purchase flow exposed through the store bridge.
Flutter feature modules must not talk directly to raw platform store APIs from screen widgets.

## 10.2 Backend validation rule
After a purchase succeeds locally, the app must call the trusted backend validation endpoint and use the normalized entitlement response that comes back.

## 10.3 Restore rule
Restore is a user-initiated action available from:
- Support this App surface,
- gated feature surfaces where appropriate,
- Settings Root.

The app must call the trusted restore endpoint and use the normalized entitlement response.

## 10.4 Idempotency rule
Purchase validate and restore must use the idempotency and retry rules already defined in the API contract.

## 10.5 Auth requirement rule
Trusted purchase validate and restore flows require authenticated user context.
If a user tries to restore while signed out, the app must route through the account gate first.

## 10.6 Success behavior
On successful purchase validation or restore:
- the cached entitlement snapshot is updated,
- feature gates react quickly,
- the user sees a calm success confirmation,
- related convenience prompts such as pack preparation may appear only when contextually appropriate.

## 10.7 Failure behavior
Failure states must distinguish between:
- user canceled purchase,
- temporary network or store error,
- auth required,
- validation failure,
- restore found no active entitlement,
- backend integration error.

## 10.8 No fake success rule
The app must not unlock paid features permanently based only on client-side purchase optimism without trusted validation.

## 10.9 Restore expectation rule
Restore is for recovering current or valid store-backed entitlement state, not for bypassing the platform subscription lifecycle.

---

# 11. Cancel, downgrade, refund, and expiry behavior

## 11.1 Cancel behavior
Subscription cancellation is managed by the store, not by a custom in-app cancellation workflow.
The app may surface a platform-appropriate “Manage Subscription” handoff, but it must not imply it controls cancellation directly.

## 11.2 Downgrade behavior
When the user’s paid access lapses or the backend reflects downgrade:
- the tier and gate snapshot update accordingly,
- free features remain fully available,
- richer gated capabilities become unavailable or read-only according to their feature contracts,
- the app explains the change without panic language.

## 11.3 Refund behavior
Refund or revoked purchase state must be reflected through the trusted backend path and then propagated into the entitlement snapshot.
The app must close paid gates gracefully while preserving ethical free access.

## 11.4 Expiry rule
If `active_until` is past and the app cannot verify a new active state, it must not imply current Supporter certainty.

## 11.5 Graceful read-only rule
Where a gated feature supports read-only downgrade behavior, the feature family that owns it must implement that behavior, but file `24` owns the entitlement truth that triggers it.

## 11.6 No punitive UX rule
Do not use scary or manipulative copy when Supporter ends. The user should still feel welcomed in the free product.

---

# 12. Family-sharing and cross-platform account behavior

## 12.1 Shared product meaning rule
The product-level meaning of Supporter remains shared across platforms, but family and restore semantics may differ by store.

## 12.2 Apple-family behavior caution
If Apple family-sharing support is enabled for the subscription product, the app may reflect that through normalized entitlement state.
The app must not hardcode family-sharing assumptions into product logic outside the normalized backend contract.

## 12.3 Android-family behavior caution
Do not assume Android offers the same subscription family-sharing semantics as Apple.
Any family-related entitlement experience on Android must come from trusted normalized backend truth rather than product assumptions.

## 12.4 Cross-platform linking rule
Entitlements should follow the authenticated user account as normalized by the backend, not remain device-isolated.
The app must not imply that buying on one device automatically bypasses the need for account-linked restore/validation on another.

## 12.5 Wording rule
Family-related copy must be platform-aware and cautious.
Do not promise identical family behavior across Apple and Google if the platforms differ.

---

# 13. Offline entitlement continuity behavior

## 13.1 Continuity rule
The app may cache the last-known entitlement snapshot for UX continuity only.

## 13.2 Refresh triggers
The entitlement snapshot should be refreshed when online at least on:
- app start,
- purchase success transition,
- restore flow,
- relevant account/auth transitions,
- other purchase-related transitions where appropriate.

## 13.3 Offline-safe behavior
When offline:
- the app may use the last-known entitlement snapshot for short-term continuity,
- it must not falsely confirm new paid access,
- it must not imply post-expiry certainty without trusted verification.

## 13.4 Expiry-aware rule
If the cached snapshot indicates active access still within a clearly valid time window, the app may preserve gated UX continuity.
Once that state is expired, missing, or unverifiable, gated features must fail safe.

## 13.5 Protected-state staleness rule
Screens must clearly distinguish between:
- current verified paid access,
- cached last-known access,
- unavailable because server confirmation is required,
- locked because no valid trusted access is known.

## 13.6 Offline local-only rule
Even when paid features are locked due to unverifiable protected state, local-first free features remain usable.

---

# 14. Settings ownership and information architecture

## 14.1 Purpose of Settings Root
Settings Root exists to expose account, preferences, pack/download options, notifications-related surfaces, privacy/help links, and app-management actions in one coherent place.

## 14.2 Settings ownership rule
This feature family owns the settings surface and the user-facing meaning of settings categories.
It does not own every deep implementation detail behind each setting.

## 14.3 Canonical settings sections
Settings Root should group items into sections such as:
- account and profile,
- Support this App,
- app preferences,
- packs and downloads,
- notifications and permissions,
- privacy and data,
- help/about/app info.

## 14.4 Settings anti-sprawl rule
Do not create dozens of fine-grained toggles when a simpler explanation or handoff is better.

## 14.5 Auth-linked settings rule
Some settings are only meaningful when authenticated.
Those must render honestly as available or unavailable rather than as broken rows.

---

# 15. Local preference model

## 15.1 Local settings posture
Most preferences in this feature family are device-local by default unless a future approved contract makes them server-backed.

## 15.2 Canonical locally owned preferences
Representative locally owned preferences include:
- selected app language or language override where applicable,
- simple-mode preference,
- pack/download preferences such as Wi-Fi-only and auto-download consent,
- notification-related local UX preferences,
- support prompt dismissal state,
- other app-level UX toggles explicitly approved here.

## 15.3 Not everything belongs here
Feature-specific dismissals or domain-specific storage may live in their owning feature family even if surfaced from Settings.
Examples:
- safety-banner dismissals,
- note-specific editor defaults,
- map runtime session state.

## 15.4 Local persistence rule
Local preferences must remain functional offline and should load immediately without waiting on network.

## 15.5 No ad hoc strings rule
Preference keys and enum values must remain centralized and typed. Do not invent ad hoc string literals in feature widgets.

---

# 16. Support this App surface behavior

## 16.1 Purpose
Support this App is the canonical purchase and restore entry surface.

## 16.2 Placement
This surface may appear as:
- a full screen reachable from Settings Root,
- a dedicated detail page reachable from gated screens,
- a contextually invoked purchase sheet when ethically appropriate.

## 16.3 Required content blocks
Support this App should include:
- short explanation of why Supporter exists,
- what remains free,
- what Supporter unlocks,
- pricing as resolved through the store/product layer,
- Become a Supporter CTA,
- Restore Purchase CTA,
- Manage Subscription handoff where appropriate,
- fine-print or disclosure copy as required by policy.

## 16.4 Ethical messaging rule
Copy must reinforce:
- no ads,
- no paywall on correctness or safety,
- Supporter helps keep the app available for everyone.

## 16.5 Placement rule
Do not open this surface inside ritual-critical, emergency, or urgent recovery moments.

---

# 17. Settings Root UX contract

## 17.1 Canonical screen
This feature family owns `settings_root` and strongly depends on `account_gate`.

## 17.2 Settings Root primary purpose
Expose account, preferences, pack settings, notifications, privacy, and app options in a calm, structured layout.

## 17.3 Required content blocks
Settings Root must include, where relevant:
- account summary card or sign-in prompt,
- Support this App entry,
- language/preferences section,
- packs/download preferences section,
- notification/permission summary section,
- privacy and data section,
- account/data management section when signed in or when account-linked deletion/help must be shown,
- help/about section.

## 17.4 Required states
- default content,
- signed-out state,
- auth-linked settings available,
- auth-linked settings unavailable,
- offline with local settings only,
- permission-summary states,
- entitlement-stale state where it materially matters,
- account/data-management availability state where auth or connectivity changes what can be shown.

## 17.5 Primary actions
- sign in or manage account,
- open Support this App,
- restore purchase,
- open platform manage subscription surface where appropriate,
- open system settings for permissions when needed,
- open account/data deletion flow or trusted web handoff when applicable,
- edit local preferences.

## 17.6 Rule
Settings Root must not feel like a billing dashboard or technical admin panel.

---

# 18. Account Gate UX contract

## 18.1 Canonical screen
This feature family strongly owns `account_gate`.

## 18.2 Primary purpose
Request authentication only because a trusted online feature requires it.

## 18.3 Entry points
- Group join,
- purchase restore/validation,
- protected account settings,
- any future approved protected feature.

## 18.4 Required content blocks
- clear explanation of why sign-in is needed,
- sign-in action(s),
- cancel or back action where appropriate,
- offline explanation if auth cannot proceed.

## 18.5 Required states
- sign-in choice,
- loading,
- auth failure,
- offline unavailable for auth-required action.

## 18.6 Rule
Do not frame this as “you must make an account to use the app.”
Frame it as “this trusted feature needs sign-in.”

---

# 19. Lock-state behavior

## 19.1 General lock-state rule
If a feature or richer variant is gated, the lock state must:
- explain the value clearly,
- preserve ethical free access boundaries,
- avoid implying that correctness or safety is being withheld.

## 19.2 Example lock-state uses
- supporter-only pack states,
- group live board,
- offline audio convenience,
- extended notes/bookmarks features.

## 19.3 Protected vs unavailable distinction
The UI must distinguish between:
- locked by entitlement,
- unavailable because offline verification is required,
- unavailable because a pack is missing,
- unavailable because a permission or device capability is missing.

## 19.4 No deceptive dark-pattern rule
Do not use countdown pressure, guilt language, or misleading “limited time” framing unless the store/product configuration genuinely requires it and legal/policy review has approved it.

---

# 20. Copy, localization, RTL, and accessibility rules

## 20.1 Copy tone
Account and subscription copy must be:
- calm,
- grateful,
- respectful,
- plain-language,
- not aggressive,
- not overly technical.

## 20.2 Support copy guidance
Preferred framing includes:
- “Support this app”
- “Help keep guidance and safety tools free for everyone.”
- “Restore Purchase”
- “Manage Subscription”

Avoid copy that sounds like:
- a high-pressure sale,
- a rewards scheme,
- a punishment for free users.

## 20.3 Pricing and disclosure rule
Displayed pricing, trial language, and renewal language must reflect platform/store truth and localization.
Do not hardcode obsolete price strings into the product.

## 20.4 RTL and mixed-content rule
Plan names, product IDs, dates, purchase states, and mixed-language support copy must remain bidi-safe in RTL contexts.

## 20.5 Accessibility requirements
This feature family must support:
- large text,
- screen-reader clarity for price and restore/manage actions,
- non-color-only lock-state meaning,
- simple segmented information hierarchy,
- full-screen flows for dense account or restore tasks rather than cramped modal overload.

## 20.6 Error-copy rule
Store, restore, and auth errors must be translated into calm user-appropriate messages rather than exposing raw platform or backend error details.

---

# 21. Security and privacy rules for this feature family

## 21.1 No raw receipt leakage rule
Raw store receipts, tokens, or signed transaction payloads must not be logged or surfaced casually in client UI.

## 21.2 Entitlement trust rule
Only the trusted backend writes or updates `user_entitlements` and purchase-validation records.

## 21.3 Minimal profile rule
Profile data should remain minimal and practical for product needs such as display name and group display context.

## 21.4 Protected cache rule
Cached entitlement snapshots and protected account state must remain app-private and should not be treated like public configuration.

## 21.5 User-initiated purchase actions rule
All purchase, restore, and manage-subscription actions remain explicitly user-initiated.

## 21.6 No hidden monetization tracking rule
Do not collect more purchase-related telemetry than needed for product quality, conversion analysis, and fraud/debug operations within the broader analytics policy.

## 21.7 Account-deletion discoverability rule
If account deletion is supported or required, the app must make the path easy to find from Settings and must describe what is deleted immediately, what may be retained for legal, fraud, accounting, or support reasons, and when a web handoff is being used instead of an immediate in-app destructive action.

---

# 22. Reactions required from other feature families

## 22.1 Rituals
Ritual flows must never show monetization interruption inside correctness-critical moments.
Ritual audio convenience or related enrichments may react to entitlement state but cannot redefine it.

## 22.2 Maps
Maps may use entitlement state for pack-related convenience and lock states, but anchor recovery and baseline orientation remain free.

## 22.3 Group
Group join depends on account gating when trusted auth is required, and Live Board depends on entitlement plus membership authorization.

## 22.4 Planner / Notes / Wallet
Planner reacts to `SMART_PLANNER`, and Notes/Bookmarks reacts to `NOTES_BOOKMARKS_EXTENDED`, but those modules must treat file `24` as the owner of entitlement truth and downgrade semantics trigger.

## 22.5 Phrasebook / Emergency
Phrasebook reacts to `AUDIO_OFFLINE` and local preferences surfaced through Settings, but must not own subscription truth.

---

# 23. Performance and operational rules for this feature family

## 23.1 Performance authority
Global budgets are defined in file `17`.
This feature family must obey them.

## 23.2 Feature-level operational priorities
This feature family must optimize for:
- fast opening of Settings Root from local data,
- low-friction account gate transitions,
- quick post-purchase or post-restore state convergence,
- honest offline behavior for protected state.

## 23.3 Recommended operational targets
Representative targets:
- Settings Root open from local data p95 ≤ **400 ms**,
- account gate open p95 ≤ **350 ms**,
- post-restore entitlement state visible quickly after the trusted response returns,
- no visible spinner-only gating in sacred or urgent flows.

---

# 24. Analytics and observability requirements

## 24.1 Canonical events from file `17`
This feature family must emit at minimum:
- `entitlement_snapshot_refresh`
- `entitlement_restore_start`
- `entitlement_restore_complete`
- `entitlement_restore_fail`
- `entitlement_upgrade_view`
- `entitlement_upgrade_start`
- `entitlement_upgrade_complete`
- `entitlement_upgrade_fail`
- `settings_preference_change`

## 24.2 Recommended feature parameters where relevant
- `surface`
- `tier_before`
- `tier_after`
- `source`
- `restore_platform`
- `network_state`
- `offline_continuity_used`
- `preference_key`
- `lock_reason`

## 24.3 Privacy-light telemetry rule
Do not send raw receipts, full store payloads, personal profile fields, or sensitive identifiers as analytics parameters.

## 24.4 Observability priorities
High-signal issues include:
- purchase validation failures,
- restore failures,
- stale-entitlement logic regressions,
- incorrect gate mapping,
- auth gate loops,
- sign-out state corruption,
- inconsistent downgrade behavior across modules.

---

# 25. Testing and validation requirements

## 25.1 Required automated coverage
Automated tests must cover at minimum:
- account-gate routing only for protected features,
- authenticated versus signed-out settings states,
- entitlement gate mapping for all current gates,
- purchase-validate success/failure handling,
- restore success/failure handling,
- cached entitlement continuity rules,
- post-expiry fail-safe behavior,
- downgrade behavior for extended notes/bookmarks,
- pack auto-download setting reactions,
- lock-state copy and navigation rules,
- account/data-management entry visibility and deletion-path routing rules.

## 25.2 Required manual/device validation
Manual or device validation must cover at minimum:
- first-use without account,
- triggering account gate from Group join,
- triggering account gate from restore purchase,
- successful Supporter purchase flow on iOS and Android test environments,
- restore on reinstall or new device path,
- offline after valid entitlement snapshot,
- expiry or refund reflection,
- signed-out local-only settings behavior,
- large-text and screen-reader usability of Support this App and Settings Root,
- platform-specific manage-subscription handoffs,
- delete-account or data-deletion discoverability and any required web handoff.

## 25.3 Real-world validation requirement
Before release, representative testing must validate:
- users understand why sign-in is needed when it appears,
- Supporter messaging does not feel coercive,
- restore is discoverable and understandable,
- settings structure is calm rather than cluttered,
- offline protected-state behavior is honest,
- authenticated users can find account/data-management and deletion help without support intervention.

## 25.4 Fake-success warning
A working purchase button is not enough evidence.
Release confidence requires restore, expiry, downgrade, offline continuity, and lock-state correctness across modules.

---

# 26. Definition of done for this feature family

This feature family is not ready for release unless all of the following are true:
- account gate appears only when a trusted feature requires it,
- `profiles`, `user_entitlements`, and purchase-validation behavior stay aligned with files `13` and `14`,
- purchase validate and restore use normalized trusted entitlement responses,
- offline continuity does not overclaim certainty after expiry or failed verification,
- free versus Supporter boundaries remain ethical and consistent across modules,
- settings own the agreed account/preferences/privacy/help/account-data-management structure without feature-sprawl confusion,
- platform differences are reflected honestly,
- account deletion or deletion-request pathways are discoverable, truthful, and aligned with the actual server-side deletion/retention posture,
- analytics hooks align with file `17`,
- real-device validation confirms restore, downgrade, and lock-state clarity.

---

# 27. Cross-file dependency rules

## 27.1 If entitlement keys or product meaning changes
Update:
- this file,
- file `14`,
- file `13` if persistence meaning changes,
- all affected feature-family files,
- analytics and tests.

## 27.2 If pricing or store-offer policy changes
Update:
- this file,
- relevant copy/localization assets,
- backend product-id or plan mappings,
- release evidence where needed.

## 27.3 If settings categories or ownership changes
Update:
- this file,
- file `11`,
- affected feature-family files,
- app architecture docs if module boundaries change.

## 27.4 If restore or purchase flow changes
Update:
- this file,
- file `14`,
- file `09` if bridge expectations change,
- tests and QA scenarios.

## 27.5 If offline continuity policy changes
Update:
- this file,
- file `15`,
- file `17` if observability or alerting changes,
- lock-state rules in affected screens.

---

# 28. Anti-patterns forbidden by this document

The following are forbidden unless explicitly approved.

## 28.1 Forcing account creation before the user can access the core local-first product
Forbidden.

## 28.2 Letting the client invent or extend entitlement truth
Forbidden.

## 28.3 Showing paywalls inside ritual-critical or emergency-critical flows
Forbidden.

## 28.4 Promising identical family-sharing behavior across Apple and Google without store-backed truth
Forbidden.

## 28.5 Hiding restore behind obscure navigation or support-only flows
Forbidden.

## 28.6 Treating stale entitlement state as definitely current when freshness materially matters
Forbidden.

## 28.7 Scattering settings ownership across unrelated feature widgets without central control
Forbidden.

## 28.8 Logging raw receipt payloads or exposing store internals in user-facing copy
Forbidden.

## 28.9 Building a custom in-app cancellation system that pretends to replace store-managed subscription control
Forbidden.

## 28.10 Using aggressive or guilt-based monetization copy in a stress-sensitive product
Forbidden.

---

# 29. Implementation priorities

## 29.1 Phase 1 priorities
Implement first:
- account gate routing,
- normalized entitlement snapshot consumption,
- Support this App baseline surface,
- purchase validate and restore integration,
- Settings Root baseline sections,
- local preference persistence for app-level settings.

## 29.2 Phase 2 priorities
Then add:
- profile editing polish,
- manage-subscription handoffs,
- richer lock-state refinement across modules,
- better downgrade/read-only behavior messaging,
- family-related explanatory wording where supported.

## 29.3 Phase 3 priorities
Then refine:
- stronger platform-tailored subscription UX,
- better conversion and restore diagnostics,
- deeper contextual upgrade surfaces that still respect ethical placement,
- post-launch simplification based on real user confusion data.

---

# 30. When this file must be updated

This file must be updated whenever any of the following changes:
- auth-gate policy,
- profile fields exposed to users,
- Supporter product meaning,
- entitlement gate list or semantics,
- purchase validate or restore flow behavior,
- downgrade/refund/expiry handling,
- settings categories or ownership,
- offline entitlement continuity policy,
- account or subscription analytics hooks,
- release-readiness expectations tied to subscriptions or settings.

If these truths change but this file is not updated, lock-state behavior, purchase flows, and other feature-family contracts will drift quickly.

---

# 31. Summary

This file defines the canonical feature-facing contract for Account, Subscriptions, Entitlements, and Settings in Pilgrims Mobile App.

It establishes:
- optional account-gate behavior,
- Supporter and restore UX behavior,
- trusted entitlement truth and gate semantics,
- downgrade, refund, and expiry handling,
- offline continuity rules for protected state,
- Settings Root ownership,
- copy, accessibility, analytics, and testing requirements.

Its purpose is to ensure this trust-boundary feature family remains:
- calm,
- honest,
- ethically monetized,
- platform-aware,
- and maintainable for long-term AI-assisted implementation.

