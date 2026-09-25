# 24 — FEATURE: ACCOUNT, SUBSCRIPTIONS, ENTITLEMENTS, AND SETTINGS

## Document status
- **Type:** Normative feature-family specification
- **Priority:** Highest
- **Audience:** Founder, product lead, backend engineers, Flutter engineers, design lead, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical feature contract for account access, authentication gating, subscriptions, purchase validation and restore behavior, entitlement truth, downgrade/refund handling, Settings ownership, Privacy & Data behavior, local preference behavior, and release-readiness expectations.
- **Authority level:** This file is the canonical source of truth for account-facing product behavior, subscription UX, entitlement-driven lock states, restore flows, Settings ownership, and Privacy & Data UX. File `14` owns API contracts. File `29` owns privacy/security/compliance boundaries. File `31` and `CONTRACTS/entitlement_capability_policy.yaml` harden entitlement policy.
- **Last-updated-by:** AI-assisted quality-first hardening pass (validated 2026-06-11)
- **Primary dependencies:** `01`, `03`, `04`, `07`, `08`, `09`, `10`, `11`, `12`, `13`, `14`, `15`, `17`, `29`, `31`, `CONTRACTS/entitlement_capability_policy.yaml`, `CONTRACTS/screen_feature_traceability.yaml`
- **Related files:** `18`, `19`, `20`, `21`, `22`, `23`, `25`, `27`, `28`, `30`

---

# 1. Purpose of this file

This file exists because account/auth, subscription behavior, entitlement enforcement, Privacy & Data controls, and Settings are trust-boundary features.

If this feature family is vague, teams and AI agents create especially dangerous problems:
- account creation gets forced too early and harms first-use value,
- client code starts inventing entitlement state instead of trusting the server,
- paid-vs-free boundaries drift inconsistently across modules,
- restore and downgrade behavior becomes unreliable or misleading,
- platform store differences are ignored and the product promises impossible parity,
- local settings are scattered across many modules without ownership,
- sensitive protected state is shown as current when it is only cached,
- deletion/export/retention flows become hidden or inconsistent,
- sacred or safety-critical flows become polluted by poorly placed upgrade prompts.

This file defines:
- account gate behavior,
- what users can and cannot expect from account and subscription behavior,
- how sign-in gating works,
- how purchases, restore, downgrade, and refund handling work,
- how entitlement truth is obtained and cached,
- how Privacy & Data surfaces behave,
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
- manage privacy/data actions without hunting or support-only ambiguity,
- trust what is free, what is paid, what is local-only, and what remains available offline.

## 2.2 Main user value statement
A pilgrim should be able to open account and settings surfaces and quickly answer:
- Do I need to sign in for this?
- Am I a Supporter right now?
- Why is this feature locked or unavailable?
- How do I restore my purchase on this device?
- What app preferences can I safely control?
- What data is local-only versus server-backed?
- How do I request deletion or export without getting lost?

## 2.3 Feature-level promise
This feature family must feel:
- calm,
- trustworthy,
- low-friction,
- explicit about protected versus local state,
- ethically monetized,
- privacy-clear,
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
- Settings Root information architecture,
- Privacy & Data flow,
- deletion request/status UX,
- data export request UX,
- retention-summary UX,
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
File `14` defines HTTP contracts for:
- `GET /v1/entitlements`,
- `POST /v1/purchases/validate`,
- `POST /v1/purchases/restore`,
- `POST /v1/account/deletion-request`,
- `GET /v1/account/deletion-status`,
- `POST /v1/privacy/export-request`,
- `GET /v1/privacy/retention-summary`.

This file defines how those APIs are used in product behavior and how users experience them.

## 3.5 Boundary with file `15`
File `15` defines offline snapshot and refresh policy for entitlements and other protected state.
This file applies those rules to account and settings UX.

## 3.6 Boundary with files `18`–`23`
Other feature families do not own entitlement truth.
They may react to entitlements or settings, but authoritative meaning of gates, restore behavior, and account gating belongs here.

## 3.7 Boundary with file `29`
Deep privacy, compliance, retention, deletion, incident, SDK, and risk controls belong to file `29`.
This file defines the feature-facing privacy and user-trust behavior required at runtime.

## 3.8 Boundary with machine-readable contracts
Implementation must validate account and entitlement behavior against:
- `CONTRACTS/entitlement_capability_policy.yaml`,
- `CONTRACTS/screen_feature_traceability.yaml`.

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
- medical profile basics,
- basic group join and manual coordination fallback.

## 4.3 Server-truth entitlement rule
The client may cache entitlement snapshots for continuity, but the server remains authoritative.
The app must not invent, extend, or silently assume Supporter access.

## 4.4 Capability-policy rule
Feature gates must validate against `CONTRACTS/entitlement_capability_policy.yaml`.
No feature may add, rename, or reinterpret entitlement keys without updating this file, file `14`, affected feature specs, and the contract artifact together.

## 4.5 Ethical upgrade placement rule
Upgrade messaging must never interrupt ritual-critical, emergency, medical, group recovery, or urgent orientation tasks.

## 4.6 Platform-difference honesty rule
The product-level meaning of `FREE` and `SUPPORTER` must remain shared, but store, restore, and family-related behavior may differ by platform.
Do not promise identical store behavior where platforms do not offer it.

## 4.7 Settings are not a junk drawer rule
Settings must expose clear account, preference, privacy, and app-management options without becoming a dumping ground for unrelated feature configuration.

## 4.8 Protected-state honesty rule
If entitlement, account, deletion, export, or privacy state is stale, unverified, offline-only, or local-only, the UI must reflect that clearly where the distinction matters.

## 4.9 Calm copy rule
Account, privacy, and subscription copy must stay calm, grateful, and respectful.
It must not shame free users or use aggressive monetization language.

---

# 5. Canonical terminology

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

## 5.8 Privacy & Data flow
The settings flow that helps users understand local-only data, server-backed account data, deletion, export, retention, and privacy-related handoffs.

## 5.9 Support this App
The user-facing subscription and restore entry surface.

## 5.10 Auth-linked settings
Settings that only make sense when the user has an authenticated account context.

## 5.11 Local preference
A device-local user preference or UX-management toggle that is not server-authoritative by default.

---

# 6. User stories

## 6.1 Optional account access
- **As a new pilgrim**, I can use the app without creating an account until I need a protected online feature.
- **As a user**, if I try to create/join a group or restore purchases, the app explains why sign-in is needed.

## 6.2 Supporter and restore
- **As a user**, I can see what Supporter provides without being pressured during sacred or urgent flows.
- **As a user**, I can initiate purchase or restore from a clear trusted surface.
- **As a user**, if restore fails or I am offline, I understand what happened and what to do next.

## 6.3 Settings and preferences
- **As a user**, I can manage language, app behavior, download preferences, privacy/data actions, and notification-related settings without hunting through many screens.
- **As a user**, I can open system settings when a permission or platform setting matters.

## 6.4 Downgrade and continuity
- **As a downgraded or refunded user**, I can still use free features calmly and understand what changed.
- **As an offline user**, I do not see fake current entitlement certainty when the app cannot verify it.

## 6.5 Privacy and data
- **As a user**, I can understand which data is local-only and which data is server-backed.
- **As a signed-in user**, I can request account deletion and see deletion status where applicable.
- **As a signed-in user**, I can request a scoped export of server-backed personal data where applicable.
- **As a user**, I can delete or manage local-only data without being misled that it was uploaded.

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
- group creation,
- group join,
- purchase restore or validate,
- protected account settings,
- deletion/export/status requests,
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

---

# 8. Entitlement behavior

## 8.1 Entitlement source of truth
The backend returns the trusted entitlement snapshot.
Client code consumes this snapshot and must not invent gates.

## 8.2 Canonical gates
Current Supporter-linked gates are defined in `CONTRACTS/entitlement_capability_policy.yaml` and may include:
- `PACK_AUTO_DOWNLOAD`,
- `AUDIO_OFFLINE`,
- `SMART_PLANNER`,
- `GROUP_LIVE_BOARD`,
- `NOTES_BOOKMARKS_EXTENDED`.

## 8.3 Never-gate capabilities
Capabilities marked `never_gate` in the contract must remain available in the relevant free/guest/local state.
Release tests must prove this for correctness-critical and emergency-critical flows.

## 8.4 Offline entitlement continuity
When offline:
- the app may use the last-known entitlement snapshot for short-term continuity,
- it must not falsely confirm new paid access,
- it must not imply post-expiry certainty without trusted verification.

## 8.5 Downgrade behavior
Downgrade must preserve ethical free access.
Where a gated feature has read-only downgrade behavior, that behavior is owned by the feature family but triggered by entitlement truth owned here.

---

# 9. Purchase, restore, refund, and platform behavior

## 9.1 Purchase initiation
Purchase initiation may use native platform purchase surfaces.
The app should explain Supporter calmly and avoid interrupting urgent flows.

## 9.2 Restore behavior
Restore is user-initiated and must call the trusted backend/store validation path.
Restore failure must distinguish:
- offline,
- auth required,
- store unavailable,
- no active purchase found,
- backend validation failure.

## 9.3 Refund and revocation behavior
Refund or revoked purchase state must be reflected through the trusted backend path and then propagated into the entitlement snapshot.
The app must close paid gates gracefully while preserving ethical free access.

## 9.4 Family/cross-platform caution
Entitlements may follow authenticated account truth as normalized by the backend.
The app must not promise identical family-sharing or cross-platform restore semantics unless the implementation and store policy truly support it.

---

# 10. Settings Root

## 10.1 Purpose
Settings Root is the low-noise place for account, support, privacy, permissions, preferences, packs, and app information.

## 10.2 Required categories
Settings Root must include:
- Account & profile,
- Support this App / purchase and restore,
- Privacy & Data,
- App preferences, including Appearance,
- Packs & downloads,
- Notifications & permissions,
- Help / About / App info.

## 10.3 Avoid junk drawer behavior
Settings must not become a random dumping ground. Feature-specific controls should live in the owning feature unless the setting is global.

## 10.4 Local preference behavior
Simple Mode, Appearance, language preference, dismissal states, and selected app preferences remain local unless future specs approve server sync.

## 10.5 Appearance preference
Settings Root must expose **Appearance** under App preferences with exactly:
- System,
- Light,
- Dark.

Behavior:
- default: System,
- available to guests and signed-in users,
- not entitlement-gated,
- no network dependency,
- persisted locally,
- applied immediately,
- survives restart,
- does not reset navigation or active feature state,
- independent from Simple Mode,
- does not alter auth, entitlement, protected-data, or offline truth.

System follows the OS appearance. Light and Dark force the corresponding complete themes defined by file `08`.

---

# 11. Privacy & Data flow

## 11.1 Purpose
Privacy & Data helps users understand and manage account-linked data, local-only data, deletion, export, and retention without fear or confusion.

## 11.2 Required content blocks
The flow must include:
- local-only data explanation,
- server-backed account data explanation,
- delete account / request deletion,
- deletion status where a request exists,
- delete local-only data explanation or entry points,
- export server-backed personal data request where applicable,
- retention summary,
- public deletion/help handoff where required,
- privacy policy and legal links where applicable.

## 11.3 Local-only data explanation
The UI must clearly say that these are device-local by default unless a future approved feature changes that boundary:
- ritual progress,
- saved gates / anchors,
- planner items,
- notes,
- bookmarks,
- local wallet artifacts,
- medical profile,
- pack inventory.

## 11.4 Server-backed data explanation
The UI must distinguish server-backed data such as:
- profile metadata,
- entitlements,
- purchase validation records,
- groups and group membership,
- group check-ins/regroup pins/itinerary where used,
- account deletion/export request status.

## 11.5 Delete account/request deletion
If the product offers account creation or maintains server-backed personal data, authenticated users must be able to find a clear delete-account or data-deletion path from Settings Root.

The path may be a governed request flow, but must not be hidden behind undocumented support-only channels.

## 11.6 Deletion status
Where deletion is asynchronous, the UI must show understandable status states:
- no request,
- requested,
- in progress,
- completed,
- blocked pending user/support/legal action,
- failed with next step.

## 11.7 Export request
Any export must be explicit, scoped, and understandable.
The app must not create broad casual export surfaces for sensitive local-only data.

## 11.8 Retention summary
Retention copy must explain that some records may be retained longer for purchase restore, accounting, fraud prevention, security, backup, legal hold, or compliance evidence.
It must not promise immediate deletion of records that lawfully require retention.

## 11.9 Public web deletion handoff
Where required, the app must expose a trusted web handoff from the same Privacy & Data area.
The hosted page or support flow may live outside the app, but discoverability from the app remains this feature family’s responsibility.

## 11.10 Offline behavior
When offline:
- local-only data explanations remain available,
- deletion/export server requests are unavailable until online,
- cached request status may be shown only with stale/offline labeling.

---

# 12. Account Gate behavior

## 12.1 Purpose
Account Gate explains why sign-in is needed for a specific protected action.

## 12.2 Approved triggers
Account Gate may appear for:
- group creation,
- group join,
- purchase validation/restore,
- deletion/export/status requests,
- protected account settings,
- any future approved protected feature.

## 12.3 Required content blocks
- clear explanation of why sign-in is needed,
- sign-in action(s),
- cancel/back action where appropriate,
- offline explanation if auth cannot proceed.

## 12.4 Required states
- sign-in choice,
- loading,
- auth failure,
- offline unavailable for auth-required action.

## 12.5 Rule
Do not frame this as “you must make an account to use the app.”
Frame it as “this trusted feature needs sign-in.”

---

# 13. Lock-state behavior

## 13.1 General lock-state rule
If a feature or richer variant is gated, the lock state must:
- explain the value clearly,
- preserve ethical free access boundaries,
- avoid implying that correctness or safety is being withheld.

## 13.2 Example lock-state uses
- supporter-only pack states,
- group live board,
- offline audio convenience,
- extended notes/bookmarks features.

## 13.3 Protected vs unavailable distinction
The UI must distinguish between:
- locked by entitlement,
- unavailable because offline verification is required,
- unavailable because a pack is missing,
- unavailable because a permission or device capability is missing,
- unavailable because auth is required,
- unavailable because deletion/export requires online trusted server action.

## 13.4 No deceptive dark-pattern rule
Do not use countdown pressure, guilt language, or misleading “limited time” framing unless the store/product configuration genuinely requires it and legal/policy review has approved it.

---

# 14. Analytics and observability

## 14.1 Required analytics events
This feature family should emit privacy-safe events for:
- account_gate_view,
- account_gate_complete,
- support_view,
- purchase_start,
- purchase_complete,
- purchase_fail,
- restore_start,
- restore_complete,
- restore_fail,
- entitlement_refresh_complete,
- entitlement_refresh_fail,
- settings_view,
- settings_preference_change (including safe `appearance_mode: system | light | dark`),
- privacy_data_view,
- account_deletion_request_start,
- account_deletion_request_complete,
- account_deletion_request_fail,
- data_export_request_start,
- data_export_request_complete,
- data_export_request_fail.

## 14.2 Forbidden analytics values
Do not send:
- raw receipt values,
- raw tokens,
- medical profile contents,
- personal notes,
- exact private location,
- join codes,
- deletion/export payload details.

---

# 15. Testing and release evidence

## 15.1 Required test coverage
Tests must cover:
- guest first-use path without forced account,
- account gate for group creation/join,
- purchase/restore success and failure states,
- expired/downgraded entitlement state,
- offline entitlement continuity,
- no paywall on never-gate capabilities,
- Privacy & Data entry from Settings Root,
- deletion request success/failure/offline states,
- deletion status display,
- export request success/failure/offline states,
- retention summary copy,
- sign-out preserving local-only data,
- large text and screen reader behavior,
- System / Light / Dark switching while the app is running and after restart,
- theme switching while navigation/feature state is active,
- independence between Appearance and Simple Mode.

## 15.2 Release evidence
Release evidence must include:
- platform purchase/restore proof where applicable,
- entitlement policy proof against `CONTRACTS/entitlement_capability_policy.yaml`,
- privacy/data flow proof,
- account deletion/public handoff proof where applicable,
- evidence that urgent/sacred/recovery flows are not interrupted by monetization.

---

# 16. Definition of done

This feature family is ready when:
- account is optional until protected online value requires it,
- Supporter gates are ethical and contract-backed,
- entitlement state is server-truth and stale-aware,
- Privacy & Data is first-class in Settings,
- deletion/export/status behavior matches file `14` and file `29`,
- local-only data boundaries are clear,
- purchase/restore behavior is platform-aware and calm,
- analytics are privacy-safe,
- accessibility and release evidence are complete,
- Appearance exposes System / Light / Dark as a local, non-entitled, immediate preference.

---

# 17. AI-agent checklist

Before editing account, subscription, entitlement, or settings code, an AI agent must:
1. Read files `03`, `13`, `14`, `24`, `29`, and `31`.
2. Read `CONTRACTS/entitlement_capability_policy.yaml`.
3. Check whether the change affects any `never_gate` capability.
4. Check whether privacy/deletion/export behavior is affected.
5. Update affected feature specs and tests together.
6. Never add monetization prompts to ritual-critical, emergency, medical, group recovery, or urgent map recovery flows.

# Guide Marketplace account/provider/entitlement amendment

Guide Marketplace uses the existing authentication identity.

Rules:
- `auth.users` remains the only app authentication identity source;
- a normal authenticated user may apply to become a provider;
- provider application/status is a separate server-trusted domain, not an auth role toggle;
- the client must not write or infer provider verification/public eligibility;
- provider application, profile/listing management, and other protected guide operations require authentication as defined by files `14` and `32`;
- ordinary local-first app value remains available without sign-in.

Initial pilgrim Guide Marketplace capabilities are **not Supporter gates**:
- browse,
- search/filter,
- trust/credential information,
- guide profile,
- contact,
- report.

Provider monetization, if ever approved, is a distinct commercial policy and must not be represented through the pilgrim Supporter entitlement.

Paying PILGRIMS must never strengthen a provider's verification badge, credential state, public eligibility, or apparent trustworthiness.

Settings may expose provider-account management entry points only where useful; provider verification truth itself remains owned by file `32`, not Settings.

---

End of file.