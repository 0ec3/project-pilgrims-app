# 29 — SECURITY, PRIVACY, COMPLIANCE, AND RISK REGISTER

## Document status
- **Type:** Normative security, privacy, compliance, and risk-management specification
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, backend engineers, Flutter engineers, QA lead, release owner, content/governance contributors, operations contributors, legal/compliance reviewers, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical security posture, privacy boundaries, data-classification model, sensitive-data handling rules, compliance obligations, legal-copy ownership, retention and deletion rules, abuse-prevention posture, and living risk register for Pilgrims Mobile App.
- **Authority level:** This file is the canonical source of truth for security, privacy, compliance, and risk posture. If implementation, dashboards, release pressure, vendor defaults, SDK behavior, or feature wishes conflict with this file, this file wins unless a higher-authority document or approved decision record explicitly changes it.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `06-SYSTEM-ARCHITECTURE.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`, `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`, `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`, `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `17-ANALYTICS-OBSERVABILITY-AND-PERFORMANCE-BUDGETS.md`, `20-FEATURE-GROUP-HUB-CHECKINS-REGROUP-AND-SHARED-COORDINATION.md`, `22-FEATURE-PHRASEBOOK-EMERGENCY-SAFETY-AND-ASSISTIVE-TOOLS.md`, `23-FEATURE-OFFLINE-PACKS-AUDIO-AND-CONTENT-DISTRIBUTION.md`, `24-FEATURE-ACCOUNT-SUBSCRIPTIONS-ENTITLEMENTS-AND-SETTINGS.md`, `25-FEATURE-ONBOARDING-HOME-AND-SIMPLE-MODE.md`, `26-CONTENT-MODEL-SCHOLAR-REVIEW-AND-PUBLISHING-WORKFLOW.md`, `27-TESTING-STRATEGY-TEST-MATRIX-AND-DEVICE-LAB.md`, `28-REAL-WORLD-VERIFICATION-RELEASE-GATES-AND-EVIDENCE.md`
- **Related files:** `05`, `11`, `18`, `19`, `21`, `30`

---

# 1. Purpose of this file

This file exists because Pilgrims Mobile App handles several domains where trust failures can become safety failures, privacy failures, store-compliance failures, or long-tail business risk.

For this project, security and privacy mistakes are especially dangerous because:
- the product is intentionally local-first and privacy-light, which means teams can easily re-centralize data without noticing,
- some features are used when the pilgrim is stressed, tired, elderly, lost, or unable to communicate clearly,
- group coordination and saved-location recovery can drift into hidden tracking if not governed tightly,
- emergency and medical-profile behavior can accidentally collect or expose sensitive data,
- entitlement, restore, and account flows cross app, backend, and store trust boundaries,
- downloadable packs and governed content introduce artifact-integrity and rollback risk,
- AI agents can over-log, over-collect, or silently weaken controls while still producing “working” code,
- app-store disclosures and legal promises can drift away from actual implementation if they are not tied to engineering truth.

This file prevents those failures by defining:
- what data is sensitive and how it must be classified,
- what the app is allowed and not allowed to collect,
- how secrets, tokens, files, and local storage must be protected,
- how location, group, medical, and private-support data must be constrained,
- which compliance obligations must be satisfied before release,
- who owns legal copy and policy disclosures,
- what the main risks are and how they are mitigated,
- how incident severity is classified for security and privacy events.

---

# 2. Scope and boundaries

## 2.1 In scope
This file includes:
- security principles and trust boundaries,
- privacy-light data-collection rules,
- canonical data-classification model,
- handling rules for sensitive personal data,
- local and server storage protection posture,
- session/token/secret rules,
- deletion, retention, and user-rights posture,
- location/privacy constraints,
- third-party SDK governance,
- app-store privacy and platform policy obligations,
- abuse-prevention and fraud-consideration posture,
- legal-copy ownership for privacy/security disclosures,
- risk register and mitigation plan,
- incident severity matrix for security/privacy events.

## 2.2 Out of scope
This file does **not** replace:
- the canonical schema or RLS model in file `13`,
- API contract details in file `14`,
- offline pack lifecycle details in file `15`,
- governed-content publishing workflow in file `26`,
- detailed testing matrix in file `27`,
- release evidence procedures in file `28`,
- deployment, hotfix, rollback, and incident runbooks in file `30`,
- full legal counsel review for every market.

This file defines the security and privacy contract those modules must obey.

## 2.3 Boundary with file `13`
File `13` owns the canonical data model, table-level ownership, and RLS policies.

This file defines:
- how those data classes must be protected,
- what may remain local only,
- what retention and deletion posture is required,
- what risk categories apply to those entities.

## 2.4 Boundary with file `14`
File `14` owns endpoint contracts and realtime event contracts.

This file defines:
- what those endpoints are allowed to process,
- how auth, rate limiting, auditability, and error redaction must behave,
- what compliance and disclosure implications apply.

## 2.5 Boundary with file `15`
File `15` owns offline, pack, cache, and manifest runtime behavior.

This file defines:
- the trust and integrity posture for local artifacts,
- what may and may not be stored in clear or durable form,
- how local data exposure risk should be minimized.

## 2.6 Boundary with file `26`
File `26` owns governed-content review and publishing workflow.

This file defines:
- how governed content systems fit into the broader security/privacy posture,
- who may access approval records,
- how provenance, audit logs, and sensitive review notes must be protected.

## 2.7 Boundary with file `30`
File `30` should define operational runbooks, deployment procedures, hotfix workflow, rollback operations, and incident execution.

This file defines:
- the policy posture,
- the severity model,
- the risk inventory,
- and the controls that operational runbooks must implement.

---

# 3. Core security and privacy principles

## 3.1 Protect trust before convenience
If a feature becomes easier to ship by weakening privacy, security, correctness, or user honesty, the weaker design loses.

## 3.2 Local-first and privacy-light by default
Private support data should stay on the device by default unless server truth is genuinely necessary for the product promise.

## 3.3 Minimize data collection
Collect only the minimum data needed for a defined product purpose. Do not “collect now, decide later.”

## 3.4 Separate operational truth from private support data
Protected shared state such as entitlements or group membership may be server-governed.
Private support data such as notes, ritual progress, medical profile, and personal planner context should remain local unless an approved decision changes that boundary.

## 3.5 No hidden tracking
The product must not drift into passive surveillance of pilgrims, especially for location, movement, or presence.

## 3.6 No silent downgrade of protections
Fallback behavior may reduce convenience, but it must not silently reduce confidentiality, integrity, or disclosure accuracy.

## 3.7 Defense in depth
No single control is enough. Sensitive features should rely on layered controls such as access boundaries, secure storage, auditability, validation, and release proof.

## 3.8 Security and privacy are release quality
A release with critical privacy or security gaps is not “almost ready.” It is not ready.

## 3.9 Honest disclosure rule
Store disclosures, privacy notices, in-app copy, and runtime behavior must say the same thing.

## 3.10 Human accountability rule
AI agents may assist with implementation and review, but accountable humans remain responsible for security, privacy, approvals, and incident decisions.

---

# 4. Roles and accountability

## 4.1 Founder / accountable product owner
Owns high-level risk appetite, ethical boundaries, and final acceptance or rejection of critical risk waivers.

## 4.2 Engineering lead
Owns implementation of the security baseline across client, backend, and delivery systems.

## 4.3 Backend owner
Owns service-side authorization, auditability, secret handling, API hardening, abuse controls, and data deletion behavior for server-backed domains.

## 4.4 Flutter/mobile owner
Owns secure local storage posture, token handling on device, permission flows, screenshot/preview leakage controls where used, and safe use of platform security primitives.

## 4.5 Content/governance owner
Owns access boundaries and review integrity for governed content, scholar-review records, provenance metadata, and emergency correction auditability.

## 4.6 QA / release owner
Owns verification evidence for security/privacy release gates together with engineering and product.

## 4.7 Legal/compliance reviewer
Owns review of privacy policy, terms, disclaimers, app-store disclosures, breach-notification obligations, and market-specific compliance interpretation.

## 4.8 AI-agent boundary
AI agents may:
- generate draft security checklists,
- scaffold tests,
- flag suspicious code patterns,
- summarize diffs,
- propose mitigations.

AI agents must not:
- invent compliance approvals,
- fabricate legal language as “final” without review,
- self-authorize data collection,
- silently reduce privacy protections to simplify implementation,
- alter risk severity or waiver status without human approval.

---

# 5. Threat model and trust boundaries

## 5.1 Primary threat families
The product must explicitly consider at minimum these threat families:
- unauthorized access to server-backed data,
- leakage of restricted local data on a lost or shared device,
- token/session theft,
- pack or content artifact tampering,
- SDK or dependency over-collection,
- misleading privacy or store disclosures,
- abuse of group coordination flows,
- location over-collection or hidden retention,
- over-logging of sensitive states,
- entitlement spoofing or downgrade confusion,
- incident or export workflows leaking private data,
- AI-assisted implementation drift that bypasses security review.

## 5.2 Canonical trust boundaries
Important trust boundaries include:
- mobile device vs backend service,
- device-local private store vs server-backed protected state,
- authenticated user vs anonymous/guest use,
- group member vs non-member,
- scholar/content reviewer systems vs public runtime,
- internal ops/logging systems vs user-facing APIs,
- app bundle/baseline content vs remotely delivered pack/content artifacts,
- first-party code vs third-party SDK code.

## 5.3 High-sensitivity domains
The highest-sensitivity domains for this product are:
- auth credentials and session tokens,
- precise or recent location in group/regroup contexts,
- medical profile data,
- purchase validation and entitlement proofs,
- governed-content approval records and incident notes,
- private personal notes or exports,
- security and audit logs that can identify users or devices.

---

# 6. Canonical data-classification model

## 6.1 Purpose
Every persisted or transmitted data element must have a classification.

## 6.2 Classification levels
Use the following canonical levels:

### Level P0 — Public
Disclosure causes little or no harm.
Examples:
- app-store marketing copy,
- public help content,
- bundled non-sensitive UI assets,
- public pack catalog metadata intended for broad visibility.

### Level P1 — Internal
Not public by default, but low sensitivity.
Examples:
- internal spec notes,
- build metadata,
- non-sensitive release evidence summaries,
- generalized operational dashboards without personal data.

### Level P2 — Confidential
Unauthorized disclosure is meaningful and must be controlled.
Examples:
- account profile data,
- group membership data,
- entitlement snapshots,
- non-public pack manifests,
- pseudonymous analytics and diagnostics.

### Level P3 — Restricted
Unauthorized disclosure or alteration can materially harm users or trust.
Examples:
- recent or precise location data,
- medical profile data,
- purchase validation records,
- private notes/bookmarks/planner data when exported or server-backed by exception,
- governed review records not intended for public exposure,
- detailed audit logs tied to a person or device.

### Level P4 — Highly Restricted
Exposure or misuse could create severe security or privacy harm.
Examples:
- refresh tokens,
- signing keys,
- service-account secrets,
- encryption keys,
- secret rotation material,
- incident forensics containing raw sensitive payloads,
- any data set containing combined restricted identities plus sensitive context.

## 6.3 Default classification rule
If a data element is unclear, classify upward until a documented decision says otherwise.

## 6.4 Handling summary by level
- **P0:** may be broadly distributed, integrity still matters.
- **P1:** protect from casual public exposure.
- **P2:** access controlled, redacted from ordinary logs.
- **P3:** strict access control, minimized retention, encryption in transit and at rest where applicable, limited export, strong auditability.
- **P4:** strongest storage and access controls, no routine exposure to app runtime except through tightly controlled interfaces, access logged and reviewed.

---

# 7. Canonical data inventory by domain

## 7.1 Identity and account
Typical classification:
- user id / profile metadata: `P2`
- verified email/phone or linked identity metadata: `P2`
- auth tokens/session material: `P4`

## 7.2 Entitlements and purchase
Typical classification:
- entitlement snapshot: `P2`
- purchase receipt or store validation proof: `P3`
- store transaction troubleshooting evidence with identifiers: `P3`

## 7.3 Group and coordination
Typical classification:
- group id and membership: `P2`
- check-in or regroup state: `P2`
- recent or precise group-related location context: `P3`
- historical continuous location trails: forbidden by default rather than merely classified

## 7.4 Private support data
Typical classification:
- ritual progress: `P2` or `P3` depending on sensitivity of associated metadata
- notes, bookmarks, planner items, saved gate labels: `P3`
- wallet/travel preparation details: `P3`

## 7.5 Emergency and medical
Typical classification:
- emergency card content templates: `P0` or `P1`
- medical profile fields entered by the user: `P3`
- emergency export payload: `P3`
- device-local protection secrets for medical-view gating: `P4`

## 7.6 Governed content and review records
Typical classification:
- published public governed content artifact: `P0` or `P1`
- internal draft/provenance/review records: `P2` to `P3`
- approval-system credentials or signing secrets: `P4`

## 7.7 Telemetry and observability
Typical classification:
- aggregate analytics: `P1` or `P2`
- pseudonymous event streams: `P2`
- crash traces containing identifiers: `P2` to `P3`
- raw debug logs with sensitive values: forbidden in production

---

# 8. Sensitive-data handling rules

## 8.1 Need-to-have rule
Sensitive data may only be collected, stored, exported, or transmitted when there is a defined user value and approved owner.

## 8.2 No reuse-without-purpose rule
Data collected for one purpose must not be repurposed for ads, profiling, unrelated experimentation, or vague “future personalization” without new approval and disclosure.

## 8.3 No hidden sync rule
Local-only sensitive data must not silently sync to the server.

## 8.4 No silent export rule
Sensitive local data must never be exported, copied, or shared automatically.

## 8.5 Redaction rule
Sensitive values must be redacted from logs, analytics, screenshots used as evidence, customer-support transcripts, and crash payloads wherever practical.

## 8.6 Least-privilege access rule
Internal systems and humans should see only the minimum sensitive data needed for their operational role.

## 8.7 Restricted-screen posture
For high-risk screens such as medical profile presentation or token-bearing debug views:
- avoid exposing raw values in casual screenshots,
- consider app-switcher snapshot obfuscation or redaction if supported,
- require stronger local confirmation for especially sensitive reveal/export actions.

---

# 9. Data minimization, purpose limitation, and transparency

## 9.1 Purpose register rule
Every meaningful data family must have a documented purpose.
If the purpose cannot be stated clearly, the data must not be collected.

## 9.2 Minimize fields rule
Collect the smallest useful field set.
Example:
- do not collect continuous location history when a one-time saved anchor or explicit regroup pin is enough,
- do not collect a full medical history when a short emergency profile is sufficient,
- do not collect broad contacts or device identifiers when a local-only feature needs neither.

## 9.3 Transparent disclosure rule
Users must be told, in the appropriate product and legal surfaces:
- what is collected,
- why it is collected,
- whether it stays local or goes to the server,
- what third parties are involved where relevant,
- what controls or deletion options exist.

## 9.4 No dark-pattern consent rule
Permission prompts and consent text must be clear and proportionate, not manipulative or bundled unnecessarily.

## 9.5 No ad-tech tracking rule
The product must not drift into cross-app tracking, ad-network profiling, or SDK-driven behavioral monetization without an explicit strategic decision and a full rework of this spec.
The current product posture assumes no ads and privacy-light analytics.

---

# 10. Collection boundaries by feature family

## 10.1 Onboarding, Home, and Simple Mode
These flows should collect only minimal local preferences such as language and Simple Mode state.
They must not silently collect account, location, contacts, or medical data at first launch.

## 10.2 Rituals and governed content
Ritual correctness content is governed content, not personal data by default.
Personal ritual progress is private support data and should remain local by default.

## 10.3 Maps and Save My Gate
Map usage may require foreground location when the user explicitly performs a location-dependent task.
The app must not collect continuous background location by default.

## 10.4 Group coordination
Group flows may process join codes, membership state, manual check-ins, regroup pins, or user-initiated location handoff.
They must not imply or implement hidden passive tracking.

## 10.5 Phrasebook, emergency, and assistive tools
Phrase lookup and emergency-card use should remain local when possible.
Medical profile remains local by default.

## 10.6 Packs, audio, and content delivery
Pack install flows may process manifest metadata, download state, checksums, local inventory, and entitlement-aware access decisions.
They must not collect unnecessary content-consumption data.

## 10.7 Account and purchases
Account, purchase validation, and restore may process protected identifiers and receipts, but only through clearly owned auth and backend boundaries.

---

# 11. Storage and encryption posture

## 11.1 In-transit rule
All server communication carrying `P2+` data must use HTTPS/TLS.
Do not allow cleartext transport for protected API traffic.

## 11.2 Server-side at-rest rule
Server-backed `P2+` data must reside in managed storage with encryption at rest and controlled access boundaries.

## 11.3 Device-local storage rule
Sensitive device-local data must use app-private storage.
Do not store restricted data in world-readable/shared storage.

## 11.4 OS-secure-storage rule
Secrets and session material must use platform security primitives:
- iOS Keychain for tokens and small sensitive secrets,
- Android Keystore-backed storage or equivalent secure wrapper for keys and token protection.

## 11.5 File protection rule
For `P3+` local files, use the strongest practical file-protection posture supported by the platform and runtime architecture.

## 11.6 Pack integrity rule
Downloaded packs and governed content artifacts must not become active until integrity verification succeeds.

## 11.7 No security-through-obscurity rule
Obfuscation can be additive, but it is not a substitute for real storage, access, and validation controls.

## 11.8 Backup rule
If local restricted data can appear in OS backups, the product must evaluate whether backup inclusion is appropriate or whether exclusion is required for that data class.

---

# 12. Secret management and key lifecycle

## 12.1 No hardcoded-secret rule
Secrets must never be hardcoded in the client, committed to source control, or embedded in downloadable configuration intended for public extraction.

## 12.2 Environment-separated secret rule
Development, staging, and production secrets must be isolated.
Cross-environment secret reuse is discouraged and must be justified if unavoidable.

## 12.3 Secret manager rule
Server and CI secrets must be stored in approved secret-management systems, not in plaintext config files, chat, or ad hoc shared documents.

## 12.4 Rotation rule
Critical secrets must be rotatable without destructive system rebuilds.
At minimum, the architecture should support rotation for:
- signing keys where operationally possible,
- service credentials,
- webhook verification secrets,
- backend API secrets,
- vendor tokens.

## 12.5 Access logging rule
Access to production secrets should be limited and auditable.

## 12.6 Build-time exposure rule
Mobile build systems must avoid leaking secrets into logs, crash reports, build artifacts, or downloadable symbol packages.

---

# 13. Authentication, sessions, and tokens

## 13.1 Canonical auth source
Authenticated identity comes from the canonical auth system defined elsewhere.
Do not create parallel credential stores in feature code.

## 13.2 Short-lived token posture
Use short-lived access tokens with refresh handled through secure mechanisms where the auth stack supports it.

## 13.3 Secure token storage rule
Access tokens, refresh tokens, and equivalent secrets must only be stored in protected OS-backed storage, not in plaintext preferences, SQLite tables, or logs.

## 13.4 No token-in-URL rule
Tokens and signed secrets must not appear in URLs, query strings, share links, screenshots, analytics payloads, or crash reports.

## 13.5 Sign-out hygiene rule
On sign-out:
- clear active tokens from secure storage,
- clear protected caches that should not survive account boundary changes,
- preserve only those local-first free data categories that are explicitly designed to remain device-local across account changes.

## 13.6 Session honesty rule
If a session is expired, revoked, or unverifiable, the app must stop treating protected state as current truth.

## 13.7 Reauthentication posture
Reauthentication may be required for especially sensitive account actions or export actions if later approved.

---

# 14. Authorization and access control

## 14.1 Server-enforced authorization rule
Protected server data must be protected by server-side authorization, not only by client UX.

## 14.2 RLS and least-privilege rule
User-scoped and group-scoped data must use row-level or equivalent access control consistent with file `13`.

## 14.3 No client-invented-membership rule
The client must not infer itself into group access it has not been granted by trusted server state.

## 14.4 Internal tooling access rule
Operational or editorial systems must have explicit role boundaries.
Not every internal user should see receipts, medical exports, precise location, or review-private notes.

## 14.5 Audit trail rule
Sensitive state changes such as:
- purchase validation outcomes,
- entitlement changes,
- governed-content publication activation,
- privileged role changes,
- group membership administration,

must be auditable.

---

# 15. Location, group, and movement privacy

## 15.1 Privacy-light location principle
Location use must stay narrow, explicit, and task-linked.

## 15.2 Foreground-first rule
Default location behavior should be foreground and user-initiated.
Do not request background location by default.

## 15.3 Background-location rule
Background location is out of scope by default.
It may only be introduced after an explicit approved decision, updated disclosures, stronger review, and evidence that it is essential to core functionality and allowed by platform policy.

## 15.4 Approximate-vs-precise rule
Request the least precise location level that still serves the user task.
Do not default to precise location if approximate is enough.

## 15.5 No historical trail rule
The product must not maintain a general historical location trail of pilgrims.
Operational snapshots may exist only where strictly necessary and must not quietly become behavior history.

## 15.6 Group-presence honesty rule
Group surfaces must not imply live tracking or current certainty when the state is stale, manually updated, or absent.

## 15.7 Share-by-action rule
Location or regroup information should be shared because the user took a clear action, not because the app assumed ongoing consent.

## 15.8 Location analytics rule
Do not send raw precise location into ordinary product analytics pipelines.

---

# 16. Medical profile and health-like data posture

## 16.1 Local-only default
Medical profile remains local by default.

## 16.2 Not-a-medical-device rule
The product must not imply that the app provides diagnosis, treatment, regulated emergency dispatch, or official medical authority unless a later approved scope change fully supports that claim.

## 16.3 Minimal-field rule
Medical profile should collect only what is genuinely useful for emergency handoff, not a broad medical record.

## 16.4 Extra-local-protection rule
Viewing, exporting, or revealing medical profile data may require stronger local protection such as biometric or app-passcode confirmation if enabled by product configuration.

## 16.5 No hidden analytics rule
Medical profile content must never be sent to analytics, ad tech, experimentation systems, or ordinary crash payloads.

## 16.6 Export caution rule
If medical profile export or presentation mode exists, the user must trigger it explicitly and the app should avoid misleading the user about who can see the resulting content.

## 16.7 Health-category review rule
If the product’s marketed scope or data processing causes the app to fall within health/medical app policy categories on a platform, that declaration and policy review becomes release-blocking.

---

# 17. Notes, planner, bookmarks, and other private support data

## 17.1 Local-first rule
Private support data should remain on device by default.

## 17.2 No hidden cloud mirror rule
Do not silently back up notes, planner items, or bookmarks to the server without an explicit approved feature and updated disclosures.

## 17.3 Export rule
Exports are explicit user actions.
The app must not pretend exports are safe once the data leaves app-controlled storage.

## 17.4 Sensitive-search rule
If local search or indexing is used for private support data, it must remain within the app’s local privacy boundary.

## 17.5 Sharing restraint rule
Do not add “share” affordances casually to private support data without privacy review.

---

# 18. Analytics, diagnostics, and observability privacy

## 18.1 Privacy-safe telemetry rule
Telemetry must remain privacy-light and aligned with file `17`.

## 18.2 Prohibited telemetry contents
Do not send the following into ordinary analytics:
- raw medical profile data,
- raw notes/bookmarks/planner content,
- precise location,
- join codes or secrets,
- tokens,
- purchase receipts,
- full emergency message templates populated with personal data,
- governed-content draft notes or reviewer-private text.

## 18.3 Diagnostic-redaction rule
Crash reports and diagnostics must redact or avoid sensitive values wherever possible.

## 18.4 Correlation-with-restraint rule
Correlation identifiers are useful for debugging, but they must not become a covert personal-data expansion mechanism.

## 18.5 Offline queue rule
Queued telemetry should respect retention limits and must not become an unbounded local cache of private user activity.

## 18.6 Support-and-debug rule
When support or QA needs evidence, prefer synthetic or redacted data.
Do not normalize requesting raw user-sensitive payloads.

---

# 19. API, backend, and integration security

## 19.1 Input-validation rule
All backend inputs must be validated server-side, even when the client already constrains the UI.

## 19.2 Safe-error-envelope rule
API error responses must not leak secrets, internal stack traces, or sensitive identifiers to end users.

## 19.3 Rate-limit and abuse-control rule
Protected endpoints and group-related flows should have rate limiting, misuse detection, and safe error behavior.

## 19.4 Idempotency rule
Sensitive retry-prone operations such as purchase validation and restore should use idempotent or replay-safe patterns as defined in file `14`.

## 19.5 Webhook verification rule
If external payment or service webhooks are used, verify signatures/authenticity before trusting payloads.

## 19.6 Auditability rule
Sensitive server-side actions should be logged in an audit-friendly way without overexposing raw personal data.

## 19.7 Dependency and patching rule
Server and build dependencies require regular review and timely patching for security issues relevant to the actual threat posture.

## 19.8 Admin-surface restraint rule
Avoid building broad internal admin surfaces early.
Each extra privileged surface increases attack and compliance burden.

---

# 20. Client/mobile hardening and platform security

## 20.1 OS-platform primitives first
Prefer official platform security primitives over custom cryptography or custom secret stores.

## 20.2 Root/jailbreak posture
Rooted or jailbroken devices are a risk signal, not a guarantee of compromise.
High-risk actions may be restricted or warned, but the product should avoid performative “security theater.”

## 20.3 Clipboard restraint rule
Do not silently read clipboard contents.
Copy actions for emergency cards or phrases must be user-triggered.

## 20.4 Screenshot-preview restraint rule
For especially sensitive screens, consider protecting app-switcher previews or fast redaction where platform support is practical.

## 20.5 Web content rule
If web views are used, they must stay narrow, intentional, and free from casual injection of untrusted arbitrary content into privileged app contexts.

## 20.6 Native-bridge hardening rule
Platform channels and native wrappers must validate input, fail safely, and not expose debug-only privileged paths in production builds.

## 20.7 Release-build hygiene rule
Production builds must disable or strongly restrict debug utilities, verbose logs, test endpoints, and development secrets.

---

# 21. Third-party SDK governance and app-store privacy compliance

## 21.1 SDK-minimization rule
Every added SDK increases risk.
Do not add an SDK unless it solves a real problem the first-party stack should not reasonably solve itself.

## 21.2 SDK review gate
Before adopting an SDK, review at minimum:
- what data it collects,
- what permissions it uses,
- whether data is shared onward,
- whether it adds tracking or profiling behavior,
- whether it supports required platform privacy disclosures,
- whether it is needed in production.

## 21.3 Apple SDK disclosure rule
If the app includes third-party SDKs that fall under Apple’s privacy-manifest and signature requirements, those requirements become mandatory for submission.

## 21.4 Google Play disclosure rule
Google Play Data safety disclosures must accurately reflect the app’s actual data collection, sharing, and security practices across the app versions distributed on Play.

## 21.5 SDK-owner accountability rule
The app team remains responsible for SDK behavior in shipped builds.
Do not treat vendor defaults as automatic compliance.

## 21.6 No stealth-tracking SDK rule
SDKs whose main effect is hidden behavioral profiling, ad-tech tracking, or opaque data resale are forbidden under the current product posture.

## 21.7 Inventory rule
Maintain a living SDK inventory with owner, purpose, data touched, store-disclosure implications, and removal path.

---

# 22. Deletion, retention, export, and user-rights posture

## 22.1 Storage-limitation rule
Do not keep personal data longer than its defined purpose, legal requirement, or incident/forensic need justifies.

## 22.2 Deletion-by-domain rule
Deletion behavior must clearly distinguish:
- local-only data deleted on the device,
- server-backed account data,
- data retained temporarily in backups,
- legally required financial/security records.

## 22.3 Local deletion rule
For device-local private support data such as:
- notes,
- bookmarks,
- planner items,
- saved anchors,
- medical profile,
- local ritual progress where user-clearing is supported,

deletion should occur immediately on device when the user chooses to clear it, subject only to local storage mechanics.

## 22.4 Server account deletion rule
The app must provide a clear path to request or initiate deletion of server-backed personal data consistent with applicable law and operational constraints.
If the product allows users to create an account in-app, the shipped experience must also satisfy relevant store-policy discoverability requirements, including an in-app deletion path and a public web deletion/request resource when the distribution platform requires it.

## 22.5 Purchase-record retention rule
Purchase validation and support records may need longer retention for restore, fraud prevention, accounting, or legal obligations.
Do not promise immediate deletion of records that lawfully must be retained.

## 22.6 Security-log retention rule
Security and audit logs should be retained only as long as needed for security operations, incident investigation, abuse prevention, and compliance evidence.

## 22.7 Suggested default review windows
Unless legal/compliance review sets stricter or longer periods:
- routine crash/diagnostic detail: short retention, target 30–90 days,
- pseudonymous product analytics: capped, target not beyond 13 months by default,
- security/audit logs: bounded and reviewed regularly, target around 180 days unless incident or legal hold requires longer,
- local restricted data: user-controlled and minimized,
- purchase/accounting records: governed by legal and financial obligations, not by ad hoc engineering preference.

## 22.8 Backup and legal-hold rule
Deletion flows must explain that backups or legal holds may delay complete purge from every storage layer.

## 22.9 Data-subject rights posture
Where applicable law grants rights such as access, correction, erasure, restriction, objection, or portability, the product and ops posture must support those requests in a practical and timely way.

## 22.10 Export rule
Any export of personal data should be explicit, scoped, and understandable.
Do not create broad export surfaces casually.

---

# 23. Legal copy, disclosures, and policy ownership

## 23.1 Canonical legal-copy surfaces
At minimum, the product needs owned truth for:
- privacy policy,
- terms or terms-lite surface if used,
- purchase and restore disclosures,
- emergency/medical disclaimers,
- location and group privacy disclosures,
- store-listing privacy disclosures,
- health/medical disclaimers if applicable,
- data-deletion/help instructions.

## 23.2 Ownership rule
Legal and compliance copy must have a named owner.
Engineers must not casually rewrite legal meanings in widgets or store listings.

## 23.3 One-truth rule
The privacy policy, app-store disclosures, permission rationale copy, and runtime behavior must stay aligned.

## 23.4 Medical/emergency disclaimer rule
The product must clearly distinguish:
- emergency assistance tools,
- practical communication aids,
- local profile storage,

from official emergency dispatch, medical diagnosis, or regulated clinical advice.

## 23.5 Group/location disclosure rule
If group coordination uses location-linked or freshness-linked signals, the user-facing disclosure must explain that clearly and honestly.

## 23.6 Disclosure update trigger rule
Any change in data collection, sharing, retention, third-party SDK behavior, permissions, or health/location scope requires legal-copy review before release.

---

# 24. Abuse prevention, fraud, and misuse controls

## 24.1 Abuse-prevention purpose
Security posture includes protecting the system from misuse, not only protecting data from external theft.

## 24.2 Main abuse classes
At minimum consider:
- fake or scripted account creation where relevant,
- group invite spam or brute-force join attempts,
- purchase/restore abuse,
- pack download abuse,
- API scraping,
- misuse of emergency or official-looking surfaces,
- content-governance bypass attempts,
- support-channel social engineering.

## 24.3 Rate-control rule
Apply practical rate limiting and misuse detection to sensitive joins, purchase validation, restore, and other protected endpoints.

## 24.4 No punitive UX rule
Abuse controls should not unnecessarily punish legitimate stressed users.
Use proportionate controls and graceful fallback where possible.

## 24.5 Store-fraud rule
Purchase state must come from trusted store/backend validation paths, not client optimism.

## 24.6 Social-engineering rule
Support and operations procedures must assume attackers may attempt to obtain account, restore, or sensitive data through persuasion rather than technical intrusion.

---

# 25. Compliance obligations matrix

## 25.1 Purpose
Compliance obligations vary by market and scope. This section defines the minimum posture the product must assume.

## 25.2 Platform and legal baseline
Before production release, confirm at minimum:

### A. Mobile security baseline
The security verification program should align with recognized mobile-security guidance such as OWASP MASVS and the broader OWASP mobile project.

### B. Apple platform privacy obligations
When distributing on the App Store:
- maintain accurate App Privacy disclosures,
- satisfy App Review privacy and data-use expectations,
- review required-reason API declarations against the actual release build and bundled code,
- include required privacy manifests and signatures for listed third-party SDKs where applicable.

### C. Google Play privacy obligations
When distributing on Google Play:
- maintain an accurate Data safety form,
- keep privacy policy and disclosures aligned with actual app behavior,
- if the app allows users to create an account, provide in-app account deletion access and a public web deletion/request resource consistent with the shipped data model and disclosure answers,
- satisfy location/background-location policy if the app ever requests that scope.

### D. Health/medical policy obligations
If the app’s marketed scope, permissions, or data flows cause it to fall under health/medical app categories or declarations on a platform, those declarations and policy reviews become mandatory before release.

### E. Data-protection law posture
If the app processes personal data of users in jurisdictions with applicable privacy laws, the product and ops posture must support lawful processing, transparency, security, storage limitation, and user-rights handling.

## 25.3 Current named frameworks to watch
At minimum, the compliance owner should explicitly track:
- GDPR / UK GDPR style obligations where applicable,
- Indonesia’s Personal Data Protection Law where applicable to the controller or market,
- Apple App Store privacy and review requirements,
- Google Play Data safety, account/data-deletion, and sensitive-permission requirements,
- Google API Services User Data Policy if the app later requests Google user data via Google APIs.

## 25.4 No false-certification rule
Do not claim compliance with frameworks such as HIPAA, medical-device regulation, or sector-specific certification unless the organization has actually satisfied those requirements.

---

# 26. Canonical risk register

## 26.1 Purpose
The risk register is a living control surface, not a document graveyard.

## 26.2 Rating model
Use practical ratings:
- **Likelihood:** Low / Medium / High
- **Impact:** Medium / High / Critical
- **Residual posture:** Accept / Mitigate / Transfer / Avoid

## 26.3 Initial risk register

| ID | Risk | Likelihood | Impact | Residual posture | Primary controls | Accountable owner |
|---|---|---:|---:|---|---|---|
| R-01 | Over-collection or retention of precise location creates hidden-tracking risk | Medium | Critical | Mitigate | foreground-first policy, no historical trail, no raw location analytics, disclosure review | Product + Mobile + Backend |
| R-02 | Group coordination drifts into misleading live tracking or passive surveillance | Medium | Critical | Mitigate | privacy-light product rules, stale-state honesty, no hidden background tracking, release proof | Product + Backend |
| R-03 | Local restricted data is exposed on a lost/shared device | Medium | High | Mitigate | app-private storage, secure storage, optional local protection, sensitive-screen restraint | Mobile |
| R-04 | Tokens or session material leak through logs, plaintext storage, or screenshots | Medium | Critical | Mitigate | Keychain/Keystore storage, log redaction, no token-in-URL, sign-out hygiene | Mobile + Backend |
| R-05 | Client invents or misrepresents entitlement truth | Medium | High | Mitigate | server-truth entitlements, safe cached-state messaging, restore validation, release tests | Backend + Mobile |
| R-06 | Pack or governed-content artifact tampering/corruption becomes active runtime truth | Low | Critical | Mitigate | checksum verification, immutable artifacts, last-known-good fallback, fail-closed activation | Backend + Mobile + Content |
| R-07 | Scholar-sensitive or safety-sensitive content ships without proper approval or provenance | Low | Critical | Mitigate | file `26` review gates, auditability, publication validation, dual control | Content/Governance |
| R-08 | SDK or dependency collects/discloses more than the app claims | Medium | High | Mitigate | SDK inventory, privacy-manifest review, Data safety/App Privacy review, vendor minimization | Engineering lead |
| R-09 | Privacy policy, store disclosures, deletion resources, or permission rationale drift away from actual behavior | Medium | High | Mitigate | disclosure owner, release checklist, deletion-resource verification, change-trigger review, compliance sign-off | Legal/Compliance + Product |
| R-10 | Support, incident, or analytics workflows expose sensitive values | Medium | High | Mitigate | redaction rules, synthetic evidence preference, access controls, retention limits | QA + Ops + Engineering |
| R-11 | Abuse of group joins, restore flows, or pack delivery harms service trust | Medium | High | Mitigate | rate limiting, abuse detection, idempotency, audit logs, minimal exposed identifiers | Backend |
| R-12 | Weak deletion/retention discipline keeps personal data longer than justified | Medium | High | Mitigate | retention review windows, deletion pathways, legal review, backup/hold documentation | Compliance + Backend |
| R-13 | Security or privacy incident response is slow or misclassified | Medium | Critical | Mitigate | severity matrix, runbook linkage to file `30`, rehearsal, accountable incident owner | Release owner + Ops |
| R-14 | AI-assisted implementation introduces insecure shortcuts or over-logging | High | High | Mitigate | AI-agent rules, code review, secret scanning, privacy review gates, test evidence | Engineering lead |

## 26.4 Risk-register maintenance rule
Each risk entry must remain reviewable, owned, and up to date.
A stale risk register is itself a risk.

---

# 27. Risk treatment and review cadence

## 27.1 Quarterly review minimum
Review the risk register at least quarterly and before major release milestones.

## 27.2 Event-driven review triggers
Review sooner when:
- a new data type is added,
- location scope changes,
- medical/emergency scope changes,
- new SDKs are added,
- new markets are entered,
- breach or near-miss occurs,
- app-store disclosures change,
- auth, purchase, or entitlement architecture changes,
- background execution scope expands,
- governed-content workflow changes materially.

## 27.3 Residual-risk honesty rule
Residual risk must be stated honestly.
“Mitigated” does not mean “gone.”

## 27.4 Waiver rule
Any accepted residual risk that meaningfully affects privacy, security, or compliance needs:
- rationale,
- owner,
- mitigation,
- expiry/review date,
- explicit sign-off.

---

# 28. Security/privacy testing and evidence requirements

## 28.1 Testing baseline
Files `27` and `28` define the broader test and release-proof systems.
This file defines the minimum security/privacy evidence those systems must include.

## 28.2 Required automated checks
At minimum include:
- secret scanning,
- dependency vulnerability review appropriate to the stack,
- auth/session tests,
- authorization/RLS tests,
- secure-storage tests where feasible,
- pack/content integrity checks,
- disclosure/config consistency checks where automation is practical,
- redaction tests for sensitive telemetry or logs where practical.

## 28.3 Required manual/security review areas
At minimum review:
- permission prompts and rationale timing,
- account/delete/export flows,
- group/location privacy behavior,
- medical profile protection and export behavior,
- purchase/restore truthfulness,
- local restricted-data exposure on physical devices,
- SDK data-flow changes,
- store/privacy disclosure alignment.

## 28.4 Penetration and adversarial testing posture
Before production or major scope expansion, conduct a proportionate security review or penetration assessment focused on the app’s real trust boundaries.

## 28.5 Release blockers
Security/privacy blockers include at minimum:
- token leakage,
- broken authorization,
- undisclosed material data collection/sharing,
- hidden tracking behavior,
- uncontrolled medical-profile exposure,
- integrity bypass for packs or governed content,
- absence of required disclosure or policy sign-off,
- inability to honor critical deletion/account-boundary expectations,
- severe incident-severity misclassification or missing operational owner.

---

# 29. Incident severity matrix and escalation triggers

## 29.1 Purpose
This matrix classifies security/privacy events by urgency and harm.
Execution details belong in file `30`.

## 29.2 Severity levels

### SEV-1 Critical
Use when there is confirmed or strongly suspected:
- unauthorized access to `P3` or `P4` data,
- token or secret compromise,
- authorization bypass affecting protected user data,
- pack/content integrity compromise that could mislead users materially,
- live exploit or active abuse causing broad user harm,
- store/privacy disclosure mismatch likely to cause immediate rejection or severe enforcement,
- incident with plausible life/safety implications due to trust-critical failure.

### SEV-2 High
Use when there is:
- significant but contained exposure of `P2`/`P3` data,
- serious privacy misconfiguration,
- major unauthorized action without broad compromise,
- substantial disclosure gap,
- meaningful abuse campaign,
- high-confidence near miss requiring urgent fix.

### SEV-3 Moderate
Use when there is:
- vulnerability or misconfiguration with limited current evidence of exploitation,
- contained issue affecting a narrow scope,
- moderate logging/disclosure or retention problem,
- SDK/privacy mismatch that is important but not immediately critical.

### SEV-4 Low
Use when there is:
- low-impact issue,
- minor policy/documentation inconsistency,
- hygiene weakness with no meaningful current exposure,
- improvement work not requiring urgent response.

## 29.3 Escalation rule
Any suspected SEV-1 or SEV-2 must trigger immediate human review.
Do not allow automation or AI summarization to downgrade urgency without accountable approval.

## 29.4 Breach-notification rule
If a personal-data breach occurs, follow applicable legal notification rules for the affected jurisdictions and platforms.
Where GDPR/UK GDPR applies, supervisory-authority notification may be required within 72 hours unless the breach is unlikely to result in risk.

## 29.5 Evidence-preservation rule
During investigation, preserve evidence in a way that supports forensics without casually spreading sensitive data to unnecessary systems or people.

---

# 30. Update triggers, anti-patterns, and summary

## 30.1 When this file must be updated
This file must be updated whenever any of the following changes:
- data classes or data flows,
- auth/session architecture,
- location scope or permission posture,
- medical/emergency data behavior,
- retention or deletion rules,
- app-store disclosure obligations,
- SDK inventory or vendor behavior,
- legal-copy ownership,
- risk ratings or major mitigations,
- incident severity definitions,
- compliance markets or legal assumptions.

If these truths change but this file is not updated, release quality, store compliance, and privacy honesty will drift quickly.

## 30.2 Anti-patterns forbidden by this document
The following are forbidden unless explicitly approved:
- collecting background location by default,
- storing tokens in plaintext preferences or logs,
- syncing medical profile silently,
- keeping historical location trails “just in case,”
- adding ad-tech or stealth-tracking SDKs,
- using real private user data in routine QA or demos,
- exporting sensitive data without explicit user action,
- shipping with inaccurate Data safety / App Privacy / privacy policy disclosures,
- treating local-only private data as fair game for analytics,
- letting AI-generated code add data collection without review,
- claiming legal or medical compliance that has not been achieved.

## 30.3 Summary
This file defines the canonical security, privacy, compliance, and risk posture for Pilgrims Mobile App.

It establishes:
- what data is sensitive,
- how data is classified,
- what may remain local only,
- how storage, tokens, secrets, and artifacts must be protected,
- how location, group, and medical privacy must stay constrained,
- how disclosures, deletion, retention, and user-rights posture must work,
- what compliance obligations must be tracked,
- what the main risks are and how they are mitigated,
- how incidents are classified by severity.

Its purpose is to ensure that Pilgrims Mobile App remains:
- trustworthy,
- privacy-light,
- secure by design,
- honest in its disclosures,
- resilient under AI-assisted implementation,
- and safe to operate across sensitive pilgrimage use cases.

