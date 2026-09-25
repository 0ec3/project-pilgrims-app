# 29 — SECURITY, PRIVACY, COMPLIANCE, AND RISK REGISTER

## Document status
- **Type:** Normative security, privacy, compliance, and risk-management specification
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, backend engineers, Flutter engineers, QA lead, release owner, content/governance contributors, operations contributors, legal/compliance reviewers, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical security posture, privacy boundaries, data-classification model, sensitive-data handling rules, compliance obligations, legal-copy ownership, retention and deletion rules, abuse-prevention posture, and living risk register for Pilgrims Mobile App.
- **Authority level:** This file is the canonical source of truth for security, privacy, compliance, and risk posture. If implementation, dashboards, release pressure, vendor defaults, SDK behavior, or feature wishes conflict with this file, this file wins unless a higher-authority document or approved decision record explicitly changes it.
- **Last-updated-by:** AI-assisted quality-first hardening pass (validated 2026-06-11)
- **Primary dependencies:** `01`, `03`, `04`, `06`, `07`, `09`, `12`, `13`, `14`, `15`, `17`, `20`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `30`, `31`, `CONTRACTS/group_presence_privacy_contract.yaml`, `CONTRACTS/content_pack_trust_chain_contract.yaml`, `CONTRACTS/advisory_source_registry.schema.yaml`, `CONTRACTS/entitlement_capability_policy.yaml`
- **Related files:** `05`, `11`, `18`, `19`, `21`

---

# 1. Purpose of this file

This file exists because Pilgrims Mobile App handles domains where trust failures can become safety failures, privacy failures, store-compliance failures, or long-tail business risk.

Security and privacy mistakes are especially dangerous because:
- the product is intentionally local-first and privacy-light, which means teams can easily re-centralize data without noticing,
- some features are used when the pilgrim is stressed, tired, elderly, lost, or unable to communicate clearly,
- group creation, group coordination, presence freshness, and saved-location recovery can drift into hidden tracking or social-graph behavior if not governed tightly,
- emergency and medical-profile behavior can accidentally collect or expose sensitive data,
- entitlement, restore, account, deletion, and export flows cross app/backend/store trust boundaries,
- downloadable packs and governed content introduce artifact authenticity, integrity, signing-key, rollback, and advisory freshness risk,
- AI agents can over-log, over-collect, or silently weaken controls while still producing “working” code,
- app-store disclosures and legal promises can drift away from actual implementation if they are not tied to engineering truth.

This file defines:
- what data is sensitive and how it must be classified,
- what the app is allowed and not allowed to collect,
- how secrets, signing keys, tokens, files, and local storage must be protected,
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
- session/token/secret/signing-key rules,
- deletion, retention, and user-rights posture,
- location/group/presence privacy constraints,
- third-party SDK governance,
- app-store privacy and platform policy obligations,
- abuse-prevention and fraud-consideration posture,
- legal-copy ownership for privacy/security disclosures,
- risk register and mitigation plan,
- incident severity matrix for security/privacy events.

## 2.2 Out of scope
This file does not replace:
- schema or RLS model in file `13`,
- API contracts in file `14`,
- offline pack lifecycle in file `15`,
- governed-content workflow in file `26`,
- testing matrix in file `27`,
- release evidence procedures in file `28`,
- deployment, hotfix, rollback, and incident runbooks in file `30`,
- full legal counsel review for every market.

This file defines the security and privacy contract those modules must obey.

---

# 3. Core security and privacy principles

## 3.1 Protect trust before convenience
If a feature becomes easier to ship by weakening privacy, security, correctness, or user honesty, the weaker design loses.

## 3.2 Local-first and privacy-light by default
Private support data should stay on the device by default unless server truth is genuinely necessary for the product promise.

## 3.3 Minimize data collection
Collect only the minimum data needed for a defined product purpose. Do not “collect now, decide later.”

## 3.3.1 Appearance preference privacy
Appearance (`system | light | dark`) is an ordinary local UI preference. It does not require server persistence, account linkage, Supporter entitlement, or sensitive telemetry. If analytics records a preference change, use the safe enum only through the existing settings preference event.

## 3.4 Separate operational truth from private support data
Protected shared state such as entitlements, group membership, group creation, and server-backed deletion/export status may be server-governed.
Private support data such as notes, ritual progress, medical profile, planner context, and saved anchors should remain local unless an approved decision changes that boundary.

## 3.5 No hidden tracking
The product must not drift into passive surveillance of pilgrims, especially for location, movement, group presence, or live-board freshness.

## 3.6 No hidden social graph
Group creation and sharing must not import contacts, auto-invite members, scrape address books, infer relationships, or build a social graph.

## 3.7 No silent downgrade of protections
Fallback behavior may reduce convenience, but it must not silently reduce confidentiality, integrity, authenticity, or disclosure accuracy.

## 3.8 Defense in depth
No single control is enough. Sensitive features should rely on layered controls such as access boundaries, secure storage, auditability, validation, signing, rate limits, and release proof.

## 3.9 Security and privacy are release quality
A release with critical privacy or security gaps is not “almost ready.” It is not ready.

## 3.10 Honest disclosure rule
Store disclosures, privacy notices, in-app copy, and runtime behavior must say the same thing.

## 3.11 Human accountability rule
AI agents may assist with implementation and review, but accountable humans remain responsible for security, privacy, legal approvals, and incident decisions.

---

# 4. Roles and accountability

## 4.1 Founder / accountable product owner
Owns high-level risk appetite, ethical boundaries, and final acceptance or rejection of critical risk waivers.

## 4.2 Engineering lead
Owns implementation of the security baseline across client, backend, delivery systems, and contract-enforcement tooling.

## 4.3 Backend owner
Owns service-side authorization, RLS assumptions, auditability, secret handling, API hardening, abuse controls, deletion/export endpoints, and server-backed retention behavior.

## 4.4 Flutter/mobile owner
Owns secure local storage posture, token handling on device, permission flows, local-only data protection, screenshot/preview leakage controls where used, and safe use of platform security primitives.

## 4.5 Content/governance owner
Owns access boundaries and review integrity for governed content, scholar-review records, provenance metadata, advisory source records, signing/activation readiness, and emergency correction auditability.

## 4.6 QA / release owner
Owns verification evidence for security/privacy release gates together with engineering and product.

## 4.7 Legal/compliance reviewer
Owns review of privacy policy, terms, disclaimers, app-store disclosures, breach-notification obligations, deletion/export claims, and market-specific compliance interpretation.

## 4.8 AI-agent boundary
AI agents may:
- generate draft security checklists,
- scaffold tests,
- flag suspicious code patterns,
- summarize diffs,
- propose mitigations.

AI agents must not:
- invent compliance approvals,
- fabricate legal language as final,
- self-authorize data collection,
- silently reduce privacy protections,
- alter risk severity or waiver status without human approval.

---

# 5. Threat model and trust boundaries

## 5.1 Primary threat families
The product must explicitly consider:
- unauthorized access to server-backed data,
- leakage of restricted local data on a lost/shared device,
- token/session theft,
- pack or content artifact tampering,
- signing-key compromise or rollback abuse,
- SDK or dependency over-collection,
- misleading privacy/store disclosures,
- abuse of group creation or join-code flows,
- hidden group tracking or location over-collection,
- over-logging of sensitive states,
- entitlement spoofing or downgrade confusion,
- deletion/export workflows leaking private data,
- stale or expired advisory content presented as current,
- AI-assisted implementation drift that bypasses security review.

## 5.2 Canonical trust boundaries
Important trust boundaries include:
- mobile device vs backend service,
- device-local private store vs server-backed protected state,
- authenticated user vs anonymous/guest use,
- group creator/leader/member/non-member,
- scholar/content reviewer systems vs public runtime,
- internal ops/logging systems vs user-facing APIs,
- app bundle/baseline content vs remotely delivered pack/content artifacts,
- signing-key custody vs artifact distribution,
- first-party code vs third-party SDK code.

## 5.3 High-sensitivity domains
The highest-sensitivity domains are:
- auth credentials and session tokens,
- precise or recent location in group/regroup contexts,
- medical profile data,
- purchase validation and entitlement proofs,
- deletion/export request records,
- signing keys and activation pointers,
- governed-content approval records and incident notes,
- private personal notes or exports,
- security and audit logs that can identify users or devices.

---

# 6. Canonical data-classification model

## 6.1 Classification levels
Use the following canonical levels:

### P0 — Public
Disclosure causes little or no harm, but integrity still matters.
Examples: app-store marketing copy, public help content, bundled non-sensitive UI assets, public pack catalog metadata.

### P1 — Internal
Not public by default, but low sensitivity.
Examples: internal spec notes, build metadata, non-sensitive release evidence summaries.

### P2 — Confidential
Unauthorized disclosure is meaningful and must be controlled.
Examples: account profile data, group membership data, entitlement snapshots, non-public pack manifests, pseudonymous analytics.

### P3 — Restricted
Unauthorized disclosure or alteration can materially harm users or trust.
Examples: recent/precise location data, medical profile data, purchase validation records, deletion/export request data, private notes/bookmarks/planner data if exported or server-backed by exception, governed review records, detailed audit logs tied to a person or device.

### P4 — Highly Restricted
Exposure or misuse could create severe security or privacy harm.
Examples: refresh tokens, service-account secrets, signing keys, encryption keys, secret rotation material, incident forensics containing raw sensitive payloads, combined restricted identity plus sensitive context datasets.

## 6.2 Default classification rule
If a data element is unclear, classify upward until a documented decision says otherwise.

## 6.3 Handling summary
- P0: broadly distributable, integrity still protected.
- P1: protect from casual public exposure.
- P2: access controlled, redacted from ordinary logs.
- P3: strict access control, minimized retention, encrypted in transit and at rest where applicable, limited export, strong auditability.
- P4: strongest storage and access controls, no routine exposure to app runtime except through tightly controlled interfaces, access logged and reviewed.

---

# 7. Domain-specific security/privacy rules

## 7.1 Identity and account
- Auth tokens are P4.
- Profile metadata is P2 by default.
- Account deletion/export endpoints require auth, authorization, rate limits, redacted logs, and clear status semantics.

## 7.2 Entitlements and purchase
- Entitlement snapshot is P2.
- Purchase receipts/store validation proof are P3.
- Raw receipt payloads must not be logged casually.
- Client may not invent entitlement truth.
- `CONTRACTS/entitlement_capability_policy.yaml` defines never-gate behavior and must be enforced in tests.

## 7.3 Groups and presence
- Group membership is P2.
- Group check-ins and regroup pins are P2 unless they include restricted context.
- Precise/recent location is P3.
- Group creation must not import contacts or create social graph data.
- Join code abuse must be rate limited and monitored.
- Presence/freshness state must follow `CONTRACTS/group_presence_privacy_contract.yaml`.
- Ordinary check-ins must not contain precise GPS coordinates.
- Expired/revoked state must not appear as live certainty.

## 7.4 Location and map data
- Location sharing must be explicit, task-linked, foreground-first, and least-precise by default.
- Background location is out of scope unless future specs explicitly approve it.
- Analytics must not contain raw precise location.

## 7.5 Medical profile
- Medical profile remains local-only by default.
- Reveal/export behavior should require deliberate user action and stronger local protection.
- The UI must not imply medical profile data is stored on the server unless an approved future feature changes that.

## 7.6 Notes, planner, bookmarks, wallet
- These are local-first by default.
- No hidden sync/upload.
- If exported, treat export output as sensitive user-controlled data.

## 7.7 Packs, content, and advisories
- Pack/content artifacts must follow `CONTRACTS/content_pack_trust_chain_contract.yaml`.
- Manifest signature, artifact signature, checksum, key validity, compatibility, and last-known-good preservation are security requirements.
- Signing keys are P4 and require strong custody/rotation practices.
- Safety advisories and emergency numbers must follow `CONTRACTS/advisory_source_registry.schema.yaml`.
- Expired publish-blocking advisories must not activate.

## 7.8 Analytics and logs
Analytics and logs must not include:
- raw tokens,
- raw receipts,
- medical contents,
- precise hidden location,
- join codes,
- raw check-in text,
- deletion/export payload contents,
- private notes.

---

# 8. Retention, deletion, and user-rights posture

## 8.1 Local-only data
Local-only data deletion is controlled by user action and app uninstall semantics subject to platform behavior.
The UI must distinguish local deletion from server-backed deletion.

## 8.2 Server-backed account deletion
If the app offers account creation or maintains server-backed personal data, it must provide a clear in-app deletion/request path and any required public web handoff.

## 8.3 Retention honesty
Deletion copy must not promise immediate deletion for data that must be retained for purchase restore, accounting, fraud prevention, security logs, backup delay, legal hold, or compliance evidence.

## 8.4 Export posture
Export must be explicit, scoped, authorized, and redacted where required.
Do not create broad casual exports of local medical or private-support data without deliberate user action.

## 8.5 Group presence retention
Presence/freshness events must be TTL-bound and bounded-retention. They must not quietly become long-term movement or behavior history.

---

# 9. Abuse-prevention posture

## 9.1 Group creation abuse
Group creation must have:
- authenticated user requirement,
- strict rate limits,
- idempotency protections,
- abuse monitoring,
- no contact import,
- no auto-invite behavior.

## 9.2 Join-code brute forcing
Join-by-code must have:
- client validation,
- server validation,
- per-user/per-IP or equivalent abuse controls,
- safe error messages that do not leak more than necessary,
- monitoring for repeated failures.

## 9.3 Purchase/restore abuse
Purchase/restore must have:
- store validation,
- idempotency,
- raw receipt redaction,
- fraud-monitoring posture.

## 9.4 Pack/content distribution abuse
Pack/content delivery must reject tampered artifacts, revoked keys, unsigned activation, and rollback attempts outside approved controls.

---

# 10. Compliance and disclosure posture

## 10.1 Store privacy disclosures
Store privacy labels and app disclosures must match actual behavior for:
- account/profile data,
- purchases,
- diagnostics,
- group data,
- location permissions,
- local-only medical/profile/notes/planner boundaries,
- deletion/export handling.

## 10.2 Permission copy
Permission prompts must be task-linked and honest. Do not request background location by default.

## 10.3 Legal copy ownership
Privacy policy, deletion instructions, medical/emergency disclaimers, and store disclosure claims require legal/compliance review before production release.

---

# 11. Risk register

| ID | Risk | Severity | Controls |
|---|---|---:|---|
| R-01 | Hidden tracking through group/location features | Critical | Foreground-first rule, presence privacy contract, no background tracking, no raw precise analytics |
| R-02 | Group creation becomes social graph/contact import | High | No contact import, no auto-invite, explicit share-code only, release evidence |
| R-03 | Join-code brute force or group abuse | High | Auth requirement, rate limits, monitoring, idempotency, safe errors |
| R-04 | Group data exposed by RLS/auth bug | Critical | RLS tests, active membership checks, leader-only write tests, no-waiver zone |
| R-05 | Medical profile leakage | Critical | Local-only default, stronger local protection, deliberate reveal/export |
| R-06 | Entitlement spoofing or paywall drift | High | Server-truth entitlements, capability policy contract, never-gate tests |
| R-07 | Artifact tampering or unsigned content activation | Critical | Manifest/artifact signatures, key validity, last-known-good, release gates |
| R-08 | Signing-key compromise | Critical | P4 key handling, rotation, revocation, incident runbook, activation freeze |
| R-09 | Stale/expired emergency advisory shown as current | High | Advisory registry, expiry validation, stale/fallback behavior, publication block |
| R-10 | Deletion/export false claims or leakage | High | Auth endpoints, retention summary, redacted logs, legal review, status UX |
| R-11 | SDK/dependency over-collection | High | SDK review, telemetry allowlist, disclosure review, release gate |
| R-12 | Over-logging sensitive data | High | Redaction rules, log review, forbidden analytics values, QA/security evidence |
| R-13 | Store disclosure drift | High | Disclosure checklist, legal/compliance owner, release evidence |
| R-14 | AI-assisted privacy/security drift | High | AI-agent checklist, contract validation, human approval for risk changes |

---

# 12. Incident severity model

## 12.1 SEV-1 Critical
Examples:
- hidden tracking active in production,
- medical data exposed,
- group RLS/auth exposure,
- signing key compromise with active artifact risk,
- ritual/emergency correctness trust failure affecting users.

Required posture:
- immediate incident commander,
- containment before convenience,
- production freeze for related systems,
- user/support/legal escalation as appropriate,
- post-incident review.

## 12.2 SEV-2 High
Examples:
- deletion/export endpoint defect without confirmed leakage,
- advisory expiry failure affecting limited users,
- purchase/entitlement trust issue,
- pack signature verification regression caught after rollout begins.

## 12.3 SEV-3 Medium
Examples:
- non-sensitive disclosure mismatch,
- recoverable auth/account flow defect,
- low-risk SDK telemetry concern.

## 12.4 SEV-4 Low
Examples:
- minor copy inconsistency with no privacy/security impact.

---

# 13. Release security/privacy gates

A release affecting protected data, group/privacy behavior, entitlements, packs/content, advisory content, deletion/export, or permissions must include:
- impacted data classifications,
- affected contracts,
- RLS/auth proof,
- log/analytics redaction proof,
- permission copy review,
- privacy disclosure review where applicable,
- no-waiver-zone check from file `28`,
- incident/rollback readiness from file `30`.

---

# 14. Definition of done

Security/privacy posture is release-ready when:
- data classes are assigned,
- collection is minimized,
- local-only boundaries are preserved,
- RLS/auth tests cover server-backed trust domains,
- group presence privacy contract is honored,
- entitlement capability policy is honored,
- content/pack trust-chain controls are enforced,
- advisory freshness metadata is enforced,
- deletion/export UX and endpoints are honest,
- disclosures match implementation,
- risk register has no unresolved unwaivable critical failure,
- incident runbooks exist for major failure domains.

---

# 15. AI-agent checklist

Before editing security, privacy, account, group, pack/content, telemetry, or disclosure-affecting code, an AI agent must:
1. Read files `13`, `14`, `15`, `20`, `24`, `26`, `28`, `29`, `30`, and `31`.
2. Read affected files in `CONTRACTS/`.
3. Classify data involved.
4. Check local-only vs server-backed ownership.
5. Check RLS/auth implications.
6. Check redaction and analytics constraints.
7. Check deletion/export/disclosure impact.
8. Never add hidden tracking, contact import, unsigned artifact activation, or broad private-data upload without approved spec changes.

# Guide Marketplace security, privacy, compliance, and risk amendment

Guide Marketplace adds a trust-sensitive provider domain. Its governing principle is:

**Verify more; store less.**

## Data classification
Treat the following as restricted/high-sensitivity operational data:
- raw identity evidence,
- raw credential/licence evidence,
- non-public credential references,
- report bodies,
- internal moderation notes,
- private provider contact targets,
- security/fraud signals.

Public trust metadata must be a minimal approved projection of a verified fact, not the underlying evidence.

## Privacy requirements
- apply purpose limitation and data minimization to every provider/application field;
- prefer authoritative source verification and retained result metadata over permanent document copies;
- if document retention is unavoidable, define encryption, scoped access, retention/deletion, audit, breach response, and lawful processing basis before implementation;
- do not put raw contact values or verification documents into analytics/logs;
- do not silently disclose pilgrim contact information during external handoff;
- do not retain external conversation bodies;
- public browse/search responses should minimize scraping value.

## Risk-register additions
The following risks require explicit owners/controls before release:
- **GUIDE-R01 Forged credential** — false document/source manipulation.
- **GUIDE-R02 Expired/revoked credential** — stale eligibility remains public.
- **GUIDE-R03 Wrong authority model** — PILGRIMS verifies the wrong credential for the advertised service.
- **GUIDE-R04 Platform licensing exposure** — PILGRIMS operates a regulated arranging/intermediary activity without required authorization.
- **GUIDE-R05 Misleading trust badge** — public copy overstates what was verified.
- **GUIDE-R06 Unauthorized travel services** — listing drifts into visa/accommodation/transport/package/ticketing or other separately regulated activity.
- **GUIDE-R07 Religious misrepresentation** — tourism/provider trust presented as scholarly/fiqh authority or misleading religious claim.
- **GUIDE-R08 Off-platform payment scam** — provider/user payment occurs externally and user assumes PILGRIMS protection.
- **GUIDE-R09 Harassment/personal safety** — contact handoff enables abusive conduct.
- **GUIDE-R10 Contact scraping/enumeration** — provider private contact targets harvested at scale.
- **GUIDE-R11 Verification-evidence leakage** — identity/licence documents exposed to public, logs, analytics, or unauthorized staff.
- **GUIDE-R12 Report abuse/defamation** — reporting mechanism used maliciously or report content leaked.
- **GUIDE-R13 Fake review/ranking pressure** — future review/sponsorship behavior falsely influences trust; V1 mitigates by deferring reviews/sponsored placement.
- **GUIDE-R14 Stale verification** — cached or delayed state shown as current.
- **GUIDE-R15 Moderation/support failure** — harmful provider cannot be investigated/delisted promptly.
- **GUIDE-R16 Suspension/expiry propagation failure** — one surface remains active after ineligibility.
- **GUIDE-R17 Provider account takeover** — attacker edits contact/listing content or attempts fraud.
- **GUIDE-R18 Contact/report automation abuse** — mass requests, spam, or denial of service.

## Compliance blockers
`LEGAL-GUIDE-001`, `LEGAL-GUIDE-002`, and final applicable operator/disclosure obligations are open compliance risks and must remain blocker-level until resolved by accountable Saudi legal/compliance review.

Do not downgrade these risks because the V1 design omits payment or in-app booking.

---

End of file.