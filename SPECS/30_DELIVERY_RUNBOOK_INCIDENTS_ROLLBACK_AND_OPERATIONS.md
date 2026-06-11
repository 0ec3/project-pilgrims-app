# 30 — DELIVERY RUNBOOK, INCIDENTS, ROLLBACK, AND OPERATIONS

## Document status
- **Type:** Normative delivery, release-operations, incident-response, rollback, and operational runbook specification
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, release owner, Flutter engineers, backend engineers, QA lead, content/governance contributors, operations contributors, support contributors, reviewer agents, release agents
- **Purpose:** Define the canonical operational workflow for preparing, shipping, monitoring, supporting, hotfixing, rolling back, and recovering Pilgrims Mobile App across mobile builds, server-backed contracts, governed content, packs, flags, privacy endpoints, and trust-critical incidents.
- **Authority level:** This file is the canonical source of truth for release execution and operational recovery. File `28` decides whether evidence is sufficient to ship. File `29` owns risk/security/privacy posture. This file owns how rollout, containment, rollback, incident response, and support handoff are executed.
- **Last-updated-by:** AI-assisted quality-first hardening pass (validated 2026-06-11)
- **Primary dependencies:** `01`, `03`, `04`, `05`, `06`, `09`, `14`, `15`, `17`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `31`, `CONTRACTS/content_pack_trust_chain_contract.yaml`, `CONTRACTS/release_gate_taxonomy.yaml`, `CONTRACTS/advisory_source_registry.schema.yaml`
- **Related files:** `11`, `18`, `19`, `20`, `21`, `22`

---

# 1. Purpose of this file

This file exists because a release can satisfy the proof bar in file `28` and still fail if the team does not know exactly how to ship, observe, react, and recover.

Delivery and operations mistakes are dangerous because:
- the product has a deliberately small but trust-critical online surface,
- many user flows are used under stress, low confidence, fatigue, or weak connectivity,
- governed content, packs, entitlements, privacy endpoints, flags, and activation pointers can change independently of app binaries,
- map, group, emergency, account, deletion/export, and pack behavior can fail in ways that require different containment paths,
- app-store release mechanics are slower and less reversible than backend or flag operations,
- signing-key compromise, unsigned artifact activation, stale advisory content, and privacy endpoint defects can become trust crises,
- AI-assisted implementation can create release artifacts quickly but still miss the operational meaning of a safe rollout.

This file defines:
- environment strategy,
- release execution workflow,
- deployment and staging model,
- feature-flag and runtime-selection rules,
- operational dashboards and health checks,
- rollback paths by failure domain,
- hotfix rules,
- incident command and escalation rules,
- support handoff expectations,
- post-incident learning and disaster-recovery posture.

---

# 2. Scope and boundaries

## 2.1 In scope
This file includes:
- environment strategy,
- build promotion and release workflow,
- staged rollout expectations,
- feature-flag and runtime-activation rules,
- post-release monitoring rules,
- rollback decision framework,
- signed rollback and activation pointer execution,
- key-compromise response posture,
- deletion/export incident response,
- advisory/content/pack incident response,
- hotfix process,
- operational ownership and escalation,
- support handoff rules,
- disaster-recovery summary,
- postmortem template and follow-up expectations.

## 2.2 Out of scope
This file does not replace:
- product scope and ethics rules in file `03`,
- architecture truth in files `06`, `14`, and `15`,
- governed-content review and publication rules in file `26`,
- test strategy and device coverage in file `27`,
- release-proof and sign-off requirements in file `28`,
- security/privacy policy and risk posture in file `29`.

## 2.3 Boundary with file `28`
File `28` answers: “Do we have enough evidence to ship this candidate?”
This file answers how release is executed and how incidents/rollbacks are handled after shipment begins.

## 2.4 Boundary with file `29`
File `29` defines security/privacy posture, risk register, and incident severity model.
This file defines how responders use that severity model, who must be paged, what immediate containment actions are expected, and how evidence is preserved.

## 2.5 Boundary with file `26`
File `26` defines governed-content publication, emergency correction, and rollback semantics for content.
This file defines how those operations are executed in a live incident and how content rollback fits into overall operations.

## 2.6 Boundary with file `15`
File `15` defines pack states, trust-chain verification, cache behavior, last-known-good behavior, and pack lifecycle.
This file defines how pack incidents are triaged, when manifest-level containment is preferred, when delivery is paused, and how signed rollback is executed.

---

# 3. Product rules that govern delivery and operations

## 3.1 Safety-over-speed rule
When a release tradeoff exists between speed and trust, trust wins.

## 3.2 Smallest-safe-change rule
Contain incidents using the smallest operational change that safely protects users:
- disable risky exposure before shipping a new binary when possible,
- freeze or repoint a signed activation pointer before inventing live patches,
- preserve last-known-good content or pack state,
- prefer scoped rollback over broad panic reversions.

## 3.3 No “ship and pray” rule
A release is not complete when store submission is done. It remains active operational work until monitoring confirms expected stability.

## 3.4 Binary-rollback realism rule
Do not design the operations model around an assumption of instant binary rollback. Store-mediated binaries are slower to reverse than flags, config selection, content pointers, manifest controls, or backend containment.

## 3.5 Last-known-good rule
For content, packs, entitlements, flags, and runtime-dependent surfaces, the system must preserve a last-known-good fallback path where architecture allows.

## 3.6 No silent-risk acceptance rule
If a risk remains after release, it must be named, owned, monitored, and either time-bounded or fixed.

## 3.7 One incident commander rule
During a live incident, one accountable human must own coordination.

## 3.8 Honest-user-communication rule
If a problem materially affects trust, correctness, privacy, or access, user-facing communication must be accurate, calm, and not falsely reassuring.

## 3.9 No undocumented production change rule
Operational changes to flags, manifests, rollout percentages, signing keys, advisory activation, or content activation must be auditable.

## 3.10 Umrah-first operational rule
Release and incident decisions must not quietly widen scope into Hajj or broader seasonality without approved product and operational readiness.

## 3.11 No unsigned activation rule
Operations must not activate unsigned remote governed content, unsigned pack artifacts, or unsigned rollback pointers.

---

# 4. Canonical terminology

## 4.1 Build promotion
Controlled movement of a build from development/testing toward beta and production readiness.

## 4.2 Release candidate
A build and configuration state that has passed verification and is eligible for controlled rollout.

## 4.3 Rollout
Staged exposure through store distribution, flags, manifests, content activation, or equivalent operational mechanisms.

## 4.4 Rollback
Any controlled action that restores a safer previous state.
Rollback may refer to:
- binary rollout halt,
- flag rollback,
- manifest pointer rollback,
- governed-content rollback,
- pack exposure rollback,
- entitlement/config rollback,
- advisory activation rollback,
- or a replacement hotfix that restores safe behavior.

## 4.5 Containment
The fastest safe action that limits user harm while fuller diagnosis or a lasting fix is still in progress.

## 4.6 Operational freeze
A temporary rule that blocks non-essential production changes while release or incident work is ongoing.

## 4.7 Activation pointer
A controlled pointer selecting a signed content, advisory, config, or pack/manifest state for runtime use.

## 4.8 Last-known-good state
The most recent previously trusted build/config/content/pack/advisory state that remains safe to reference operationally.

---

# 5. Operational roles and ownership

## 5.1 Founder / accountable product owner
Owns high-level release risk acceptance for major milestones and final acceptance of critical operational waivers where allowed by file `28`.

## 5.2 Release owner
Owns release checklist, go-live execution, rollout pacing, and coordination with QA, engineering, product, and support.

## 5.3 Mobile owner
Owns mobile binary build integrity, store submission readiness, platform-specific rollout actions, and app-side diagnostics.

## 5.4 Backend owner
Owns backend contract readiness, production service health, config/flag service health, account/privacy endpoints, auditability, and server-side rollback actions.

## 5.5 Content/governance owner
Owns governed-content activation, advisory activation, emergency correction, content rollback, signing/manifest readiness, and review traceability.

## 5.6 QA owner
Owns release evidence traceability, shipped-candidate identity confirmation, and post-release verification on exposed tracks.

## 5.7 Security/privacy owner
Owns security/privacy incident classification, disclosure/legal escalation coordination, and containment review for protected data or trust-boundary failures.

## 5.8 Support owner
Owns support briefings, issue intake triage, known-issue communication, and escalation of user-reported signals into the incident process.

## 5.9 Incident commander
Owns cross-function coordination, time-stamped decision logging, containment sequencing, and post-incident follow-up.

## 5.10 AI-agent boundary
AI agents may help draft checklists, summarize telemetry, assemble evidence, and propose rollback steps.
AI agents must not perform privileged production actions autonomously, self-approve rollout increases, silently expire incidents, downgrade severity, or alter manifests/activation pointers without accountable human execution.

---

# 6. Operational environments

Required environment tiers:
1. local development,
2. shared integration/test,
3. staging/release-candidate,
4. production,
5. beta-distribution layer,
6. governed-content publication environment,
7. signing/key-management environment or equivalent protected workflow.

## 6.1 Production rule
Non-essential production changes should be minimized during active rollout and incident response.

## 6.2 Staging rule
Staging must be close enough to production to reveal operational issues while protecting production data and users.

## 6.3 Signing environment rule
Signing keys and activation controls are highly restricted. Production signing or key rotation must be auditable and must not be casually accessible to implementation agents or ordinary runtime systems.

---

# 7. Release execution workflow

## 7.1 Pre-rollout checklist
Before production exposure:
- file `28` evidence bundle approved,
- release candidate identity recorded,
- flags/config snapshot captured,
- manifest/content/advisory activation pointers recorded,
- rollback/containment plan confirmed,
- dashboards ready,
- support brief prepared for user-visible changes,
- incident commander escalation path known.

## 7.2 Staged rollout checkpoints
At each rollout increase, check:
- crash-free sessions,
- startup failures,
- API error rates,
- entitlement/purchase/restore errors,
- group creation/join/check-in errors,
- pack manifest/install/signature failures,
- advisory/content activation failures,
- privacy/deletion/export endpoint failures,
- user reports and support intake,
- performance and battery regressions.

## 7.3 Rollout halt triggers
Immediately halt or freeze rollout if:
- no-waiver-zone failure appears,
- hidden tracking or privacy leak is suspected,
- group RLS/auth exposure is suspected,
- pack/content signature bypass or signing-key compromise is suspected,
- emergency/ritual correctness issue appears,
- deletion/export false claim affects users,
- crash/startup failure exceeds release threshold.

---

# 8. Control surfaces

Operational control surfaces include:
- mobile binary rollout,
- backend deploy,
- flags/config,
- pack manifest,
- governed-content activation pointer,
- advisory activation pointer,
- entitlement/config truth,
- signing key revocation/rotation controls,
- support/status communication.

## 8.1 Safe default rule
Unknown or failed control-plane state should bias toward baseline safe behavior, last-known-good, or feature disablement for optional risky surfaces.

## 8.2 Mixed-truth rule
Do not create mixed truth where mobile binary, API contract, manifest, and content pointer disagree. If a mixed state is unavoidable during rollout, it must be explicitly documented and monitored.

---

# 9. Rollback and containment by failure domain

## 9.1 Binary failure
Actions:
- halt rollout,
- use store phased-release controls where available,
- disable risky optional flags if compatible,
- prepare hotfix if needed,
- support brief for affected users.

## 9.2 Backend/API failure
Actions:
- rollback deploy where safe,
- disable affected optional feature flags,
- preserve local/offline fallback,
- monitor error rates and data consistency,
- avoid schema-destructive emergency changes.

## 9.3 Group coordination failure
Actions:
- disable optional Live Board first if realtime/freshness is affected,
- preserve baseline read/regroup text where safe,
- freeze group creation if abuse/RLS risk appears,
- increase join/create rate-limit protection if abuse suspected,
- never present stale or failed writes as live success.

## 9.4 Account/privacy failure
Actions:
- freeze deletion/export request entry only if processing would be unsafe,
- preserve existing request status truth,
- stop misleading copy through config/content where possible,
- escalate to security/privacy owner and legal/compliance reviewer,
- preserve audit evidence.

## 9.5 Pack or manifest failure
Actions:
- freeze manifest rollout,
- remove or disable faulty candidate entries,
- preserve last-known-good installed packs,
- reject unsigned/revoked-key artifacts,
- publish signed rollback pointer only if approved,
- monitor install/signature failure rates.

## 9.6 Governed-content failure
Actions:
- freeze content activation,
- route to last-known-good signed artifact where safe,
- initiate emergency correction under file `26`,
- preserve review/provenance/audit history,
- communicate honestly if user trust is affected.

## 9.7 Advisory freshness failure
Actions:
- freeze or hide expired publish-blocking advisory,
- switch to safe fallback copy where approved,
- verify source registry metadata,
- escalate to content/governance and safety owner.

## 9.8 Signing-key compromise
Actions:
- declare SEV-1 unless evidence proves no runtime exposure,
- freeze artifact/content/manifest activation,
- revoke compromised key id,
- move to documented recovery key path,
- publish only signed recovery/rollback pointers using trusted key material,
- preserve forensic evidence,
- update incident record and release evidence before reactivation.

---

# 10. Incident response workflow

## 10.1 Incident declaration
Declare an incident when a production or beta issue materially affects correctness, safety, privacy, availability, artifact authenticity, or user trust.

## 10.2 First 30 minutes
The incident commander must:
- assign severity using file `29`,
- identify affected domain and control surfaces,
- choose immediate containment,
- freeze non-essential changes if needed,
- start a time-stamped decision log,
- notify required owners.

## 10.3 Evidence preservation
Preserve:
- build/config/manifest/content/advisory pointer state,
- logs with sensitive values redacted,
- telemetry snapshots,
- support reports,
- release evidence references,
- signing/key-revocation records where applicable.

## 10.4 User/support communication
If user-facing impact exists, support copy must explain:
- what users may experience,
- what still works,
- what they should do now,
- what not to rely on,
- whether data/privacy/safety is affected if known.

Do not overclaim certainty before investigation.

---

# 11. Hotfix rules

## 11.1 Hotfix eligibility
Hotfix is appropriate when containment is insufficient and user impact is time-sensitive.

## 11.2 Hotfix evidence
A hotfix still requires targeted file `28` evidence for affected risk class. Urgency changes scope of evidence, not the need for trustworthy proof.

## 11.3 No broad refactor in hotfix
Hotfixes must be minimal and targeted.

---

# 12. Support handoff

Support must receive:
- release summary,
- known issues,
- affected platforms/versions,
- current mitigation,
- user-facing copy,
- escalation path,
- what support should not promise.

For privacy/deletion/export incidents, support must not promise deletion timing, legal outcomes, or unsupported export scope beyond approved copy.

---

# 13. Post-incident review

Postmortem must include:
- timeline,
- affected users/scope,
- root cause,
- detection gap,
- containment action,
- rollback/hotfix action,
- contract/spec gap if any,
- release evidence gap if any,
- follow-up owners and dates,
- disclosure/support actions.

---

# 14. Definition of done

Delivery and operations are ready when:
- release execution has a checklist,
- rollout checkpoints exist,
- control surfaces are named,
- rollback paths exist by failure domain,
- signed rollback/key-compromise procedures exist,
- privacy/deletion/export incident handling is defined,
- support handoff is defined,
- evidence preservation is defined,
- operations align with files `28` and `29`.

---

# 15. AI-agent checklist

Before editing release/operations/runbook content or tooling, an AI agent must:
1. Read files `28`, `29`, `30`, and `31`.
2. Read affected contract artifacts.
3. Confirm the failure domain.
4. Confirm control surfaces and last-known-good behavior.
5. Never propose unsigned activation, silent severity downgrade, or undocumented production change.
6. Preserve human accountability for production actions.

---

End of file.