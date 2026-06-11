# 26 — CONTENT MODEL, SCHOLAR REVIEW, AND PUBLISHING WORKFLOW

## Document status
- **Type:** Normative content-governance and publishing contract
- **Priority:** Highest
- **Audience:** Founder, product lead, content lead, religious-governance contributors, scholar reviewers, localization contributors, backend engineers, Flutter engineers, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical content model, governance boundaries, sensitivity tiers, scholar-review requirements, provenance rules, validation pipeline, publishing workflow, signed artifact requirements, emergency correction path, and rollback behavior for governed content used by Pilgrims Mobile App.
- **Authority level:** This file is the canonical source of truth for governed content structure and publishing workflow. If implementation, tooling, runtime behavior, or review operations diverge from this file, this file wins unless a higher-level normative document or approved decision record explicitly changes it.
- **Last-updated-by:** AI-assisted quality-first hardening pass (validated 2026-06-11)
- **Primary dependencies:** `01`, `03`, `04`, `06`, `07`, `12`, `13`, `14`, `15`, `17`, `18`, `22`, `23`, `24`, `29`, `30`, `31`, `CONTRACTS/content_pack_trust_chain_contract.yaml`, `CONTRACTS/advisory_source_registry.schema.yaml`
- **Related files:** `05`, `11`, `27`, `28`

---

# 1. Purpose of this file

This file exists because the app depends on governed content in domains where incorrect wording, weak provenance, missing review, unsafe publishing operations, or unauthenticated artifacts could directly damage user trust and product correctness.

Without a canonical content-governance contract, teams and AI agents often create expensive failures:
- ritual meaning drifts into code or ad hoc copy edits,
- translations subtly change religious meaning,
- packs ship content that cannot be traced to approved sources,
- emergency fixes are made informally and become impossible to audit,
- runtime uses content that passed no schema or referential-integrity checks,
- rollback becomes unsafe because published artifacts were mutated in place,
- unsigned or tampered content becomes active runtime truth,
- content operations quietly invent a generic CMS and backend surface that the product architecture never approved.

This file defines:
- what counts as governed content,
- which content requires scholar review,
- which content requires other review types instead,
- how governed content is modeled,
- how provenance and approval records are attached,
- how validation and publication work,
- how immutable signed artifacts reach the app,
- how emergency correction and rollback must work,
- how AI agents may assist without becoming approval authorities.

---

# 2. Feature purpose and user value

## 2.1 Governance purpose
This governance module ensures that content used by the app remains:
- trustworthy,
- traceable,
- reviewable,
- local-first compatible,
- versioned,
- signed and activation-safe,
- rollback-safe,
- resilient to AI-assisted implementation drift.

## 2.2 User value statement
A pilgrim should not need to think about the publishing system directly.

The value to the pilgrim is that:
- ritual guidance feels reliable,
- remedy guidance is not improvised,
- translations feel respectful and understandable,
- phrasebook and emergency content are consistent,
- offline content continues to work safely,
- fixes happen in a controlled and honest way.

## 2.3 Operational value statement
Content contributors, reviewer agents, engineers, and release operators should be able to answer:
- What content families exist?
- Which changes require scholar review?
- Which published version is active?
- Which artifact is signed, compatible, and safe to activate?
- Where did this rule or wording come from?
- Which artifact is safe to roll back to?
- Can the app still function offline if publishing is delayed?

---

# 3. Scope and boundaries

## 3.1 In scope
This file includes:
- governed content families,
- content sensitivity classification,
- review-role requirements,
- scholar-review rules,
- localization and transliteration governance,
- provenance and approval metadata,
- validation requirements before approval and publication,
- publishing outputs and signed artifact rules,
- advisory source freshness rules,
- emergency correction workflow,
- rollback rules for governed content,
- runtime consumption boundaries for published content.

## 3.2 Out of scope
This file does **not** include:
- a full visual design for internal editorial tools,
- a promise that V1 ships a rich browser CMS,
- generalized cloud document management,
- open-ended AI generation of religious rulings,
- redefinition of runtime pack lifecycle already owned by file `15`,
- redefinition of API contracts already owned by file `14`,
- redefinition of feature-facing ritual UX already owned by file `18`,
- store subscription truth,
- general legal/compliance policy beyond content-governance implications.

## 3.3 Boundary with file `18`
File `18` defines feature-facing behavior for Rituals, RIC, remedies, citations, and governed religious-content behavior.
This file defines deeper content-governance machinery behind those behaviors.

## 3.4 Boundary with file `22`
File `22` defines user-facing behavior for Phrasebook, Emergency, Safety, and assistive tools.
This file governs content operations behind those assets, including source-of-truth rules, verification-date expectations, advisory freshness, publishing, and rollback behavior.

## 3.5 Boundary with file `14`
This file must **not** invent a large generic live content API.
Runtime publication surfaces remain intentionally small:
- app-bundled last-known-good content,
- downloadable signed artifacts discoverable through approved pack/manifest mechanisms,
- limited configuration/flags surfaces where already documented.

If future product direction requires a dedicated content metadata API, file `14` must be updated together with this file.

## 3.6 Boundary with file `15`
File `15` owns offline tiers, manifest caching, pack lifecycle, storage, and runtime pack verification.
This file defines which governed content becomes publishable artifacts and what trust/review metadata those artifacts must carry.

## 3.7 Boundary with machine-readable contracts
Governed content publishing must align with:
- `CONTRACTS/content_pack_trust_chain_contract.yaml`,
- `CONTRACTS/advisory_source_registry.schema.yaml`.

---

# 4. Product rules that govern this module

## 4.1 Governed-content rule
Any content that influences ritual correctness, remedy meaning, religious classification, emergency/safety trust, or user-facing religious confidence must come from governed content, not widget code or casual copy edits.

## 4.2 No unsupervised AI-authority rule
AI may assist drafting, linting, translation scaffolding, or structured transformation, but AI must not become the approval authority for religious meaning, remedy logic, safety-critical content, or publication.

## 4.3 Immutable-publication rule
A published artifact is immutable.
If meaning, wording, structure, review metadata, trust metadata, or approval-relevant metadata changes, publish a new version instead of mutating the existing artifact in place.

## 4.4 Traceability rule
Every governed item that matters for correctness or trust must be traceable to:
- an origin source or source note,
- a review activity,
- a responsible human role,
- a published version,
- a signed artifact or bundled baseline identifier.

## 4.5 Offline-first publication rule
The publishing system must support the product’s offline-first promise.
Essential ritual value cannot depend on a fragile live publishing service during ordinary runtime.

## 4.6 No hidden review bypass rule
There must be no hidden path where code, admin actions, build scripts, flags, or pack activation pointers can publish scholar-sensitive or safety-sensitive content without required review metadata.

## 4.7 No paywall-on-correctness rule
This workflow must preserve the product rule that correctness-related ritual guidance and remedy meaning are not gated behind Supporter monetization.

## 4.8 Honest-correction rule
If a content issue is discovered, correction must be controlled and honest. The system must not silently pretend a problematic version never existed.

## 4.9 Umrah-first content rule
Published defaults must remain Umrah-first unless season, scope, and approved publication inputs explicitly permit Hajj-specific exposure.

## 4.10 Small-online-surface rule
The content workflow must respect the architecture choice that the app does not rely on a giant always-live content backend for essential religious runtime.

## 4.11 Signed-activation rule
Remote governed artifacts and activation pointers require publisher-authenticity controls before runtime activation.
Checksum-only verification is not sufficient for quality-first release.

---

# 5. Canonical terminology

## 5.1 Governed content
Structured content whose meaning, correctness, presentation, or trustworthiness is controlled through this workflow.

## 5.2 Content family
A stable domain grouping of governed content such as ritual steps, remedy rules, citations, phrasebook phrases, emergency cards, or safety banners.

## 5.3 Content artifact
An immutable publishable output derived from reviewed source content and validation pipelines.

## 5.4 Signed artifact
A content artifact carrying checksum, artifact signature, signing key identity, signing timestamp, schema/app compatibility metadata, and provenance/review references.

## 5.5 Provenance record
Metadata that explains where a governed content item came from, who changed it, what activity reviewed it, and which version became active.

## 5.6 Review record
A structured record that captures a reviewer role, decision, timestamp, and summary of why a change was approved or returned for changes.

## 5.7 Scholar-sensitive content
Governed content that changes religious meaning, ritual correctness, remedy guidance, classification, or scholarly interpretation and therefore requires scholar review.

## 5.8 Publication candidate
A validated, review-complete content set that is ready to be packaged into an immutable artifact.

## 5.9 Emergency correction
A controlled intervention used when a published content issue has material trust, correctness, or safety impact and must be mitigated quickly.

## 5.10 Last-known-good content
The most recent validated, signed, trusted published artifact that the app can safely continue using locally.

## 5.11 Superseded version
An older published version replaced by a newer published version without implying that the older version was invalid or unsafe.

---

# 6. Governance roles and responsibilities

## 6.1 Content owner
Responsible for content scope, structure, scheduling, and operational correctness of the content workflow.

## 6.2 Content editor
Responsible for drafting or editing structured content within approved scope.
They may prepare religious content, but they do not approve scholar-sensitive meaning by themselves.

## 6.3 Scholar reviewer
Responsible for reviewing scholar-sensitive content before approval.
This role must remain human and explicitly accountable.

## 6.4 Localization reviewer
Responsible for checking translation quality, transliteration consistency, and meaning preservation across supported languages.

## 6.5 Publisher or release owner
Responsible for initiating publication only after validation and required approvals are complete.
This role may package and publish artifacts but must not bypass required approvals.

## 6.6 Incident owner
Responsible for coordinating emergency correction, mitigation, rollback, and post-incident documentation when a published content issue is discovered.

## 6.7 Engineer or tooling owner
Responsible for validation pipelines, artifact generation, manifest integration, signing, key-rotation support, and safe runtime loading.

## 6.8 AI-agent role boundary
AI agents may:
- generate structured draft suggestions,
- scaffold locale files,
- normalize schemas,
- generate diff summaries,
- run validation tooling,
- identify missing metadata.

AI agents must not:
- approve scholar-sensitive meaning,
- publish directly without required human roles,
- bypass review gates,
- invent religious rulings or remedy logic.

---

# 7. Governed content families

Governed content families include:
- ritual steps,
- ritual path selection content,
- RIC diagnostic questions,
- RIC result classifications,
- remedy guidance,
- citations and source notes,
- phrasebook phrases,
- emergency cards,
- medical support copy templates,
- safety advisories and safety tips,
- app-bundled baseline guidance.

Each family must define:
- owner,
- sensitivity tier,
- required review roles,
- locale expectations,
- schema version,
- publication strategy,
- rollback behavior.

---

# 8. Sensitivity tiers

## 8.1 Tier A — Scholar-sensitive correctness content
Requires scholar review before publication.
Examples:
- ritual steps,
- RIC classification,
- remedy meaning,
- religious citations where interpretation matters.

## 8.2 Tier B — Meaning-preserving localization content
Requires localization review and content-owner approval; scholar review is required if translation changes or risks changing religious meaning.

## 8.3 Tier C — Safety-sensitive practical content
Requires content-owner and safety/operations review.
Examples:
- emergency numbers,
- safety advisories,
- official handoff notes,
- medical support prompt copy.

## 8.4 Tier D — General helper content
Requires standard editorial review and schema validation.

---

# 9. Review workflow

## 9.1 Draft
Content begins as structured source data, not widget code.

## 9.2 Validation
Before review, validation must check:
- schema validity,
- required fields,
- references,
- locale completeness where required,
- broken links or missing sources,
- unsupported season/path/madhhab combinations,
- advisory freshness metadata where applicable.

## 9.3 Review
Required reviewer roles depend on sensitivity tier.

## 9.4 Approval
Approval records must capture:
- reviewer identity/role,
- decision,
- timestamp,
- scope of approval,
- notes or caveats,
- source/provenance references.

## 9.5 Publication
Only approved candidates can be packaged into immutable artifacts.

## 9.6 Activation
Publication and activation are separate. A signed artifact may be published but not yet active for all users.

---

# 10. Required artifact metadata

Every published governed content artifact must expose at minimum:
- `artifact_id`,
- `content_family`,
- `content_version`,
- `schema_version`,
- `generated_at`,
- `locale_set`,
- `season_scope`,
- `checksum_sha256`,
- `artifact_signature`,
- `manifest_signature` when remotely distributed,
- `signing_key_id`,
- `signing_algorithm`,
- `signed_at`,
- `review_record_refs[]`,
- `provenance_bundle_ref`,
- `min_app_version?`,
- `max_app_version?`,
- `last_known_good_eligible`,
- `pack_id?` when distributed through packs.

## 10.1 Metadata rule
Artifact metadata must align with `CONTRACTS/content_pack_trust_chain_contract.yaml`.

## 10.2 Versioning rule
Versioning must be explicit and stable.

Recommended posture:
- `content_family` identifies the domain,
- `content_version` increments per family,
- `artifact_id` uniquely identifies the immutable output.

## 10.3 Schema-version rule
Artifact schema version and content version are different concepts.
A schema change must not be hidden as a normal content edit.

## 10.4 Family-specific packaging rule
Different governed families may publish separately, but cross-family dependencies must still validate before publication.

## 10.5 Immutability rule
Once published, an artifact must never be edited in place.
Correction requires a new artifact version and an updated publication pointer or rollout decision.

---

# 11. Advisory source registry

Safety advisories, emergency numbers, official handoff notes, and region-sensitive safety tips must use metadata compatible with `CONTRACTS/advisory_source_registry.schema.yaml`.

Required registry fields include:
- jurisdiction,
- locale,
- advisory type,
- source id/name,
- source authority type,
- verification timestamp,
- expiry timestamp,
- owner,
- severity,
- offline fallback copy,
- stale behavior,
- whether expiry blocks publication.

Expired advisory sources marked `publish_blocking_if_expired=true` must fail publication validation.

Safety advisories must never block ritual or recovery tasks.

---

# 12. Runtime consumption rules

## 12.1 Approved runtime paths
Governed content may reach runtime through:
- bundled baseline content shipped with the app,
- immutable signed content artifacts distributed through existing pack/manifest mechanisms,
- tightly constrained flags/config pointers that select between already-published safe artifacts or safe content states.

## 12.2 No generic live-rules API rule
The app must not depend on a large live API that streams ritual logic or scholar-sensitive meaning on demand unless the architecture is explicitly changed in file `14` and related files.

## 12.3 Baseline bundled-content rule
Essential last-known-good governed content for core ritual value should ship with the app or otherwise remain available locally in a way consistent with the offline-first contract.

## 12.4 Pack-distributed artifact rule
Optional larger governed artifacts may be distributed as content packs or mixed-content packs when aligned with files `15` and `23`.

## 12.5 Manifest-addressability rule
If a governed artifact is distributed remotely, discovery must happen through existing approved manifest-driven mechanisms rather than hardcoded URLs.

## 12.6 Activation rule
Publishing and activation are related but distinct.
An artifact may be published yet not immediately activated for all users if rollout policy says otherwise.

## 12.7 Signed activation pointer rule
Activation pointers must be signed or protected by an equivalent approved control plane. The client must not activate unsigned remote artifacts as current trusted content.

---

# 13. Emergency correction and rollback

## 13.1 Emergency correction trigger
Emergency correction is used when a published content issue materially affects:
- religious correctness,
- safety or emergency guidance,
- misleading remedy behavior,
- severe localization meaning,
- trust in published content.

## 13.2 Correction behavior
Corrections must:
- preserve audit history,
- publish a new artifact version,
- avoid mutating old artifacts,
- include reviewer/approver records appropriate to urgency,
- document the reason for correction,
- update activation pointers safely.

## 13.3 Rollback behavior
Rollback may point users to a previous last-known-good artifact only when:
- the target artifact is signed and compatible,
- its review/provenance records remain valid,
- rollback reason is documented,
- activation pointer change is auditable,
- release/incident owner approves.

## 13.4 No silent rewrite rule
Do not overwrite prior content in place or erase published history.

---

# 14. Testing and release evidence

## 14.1 Required validation coverage
Validation must cover:
- schema correctness,
- reference integrity,
- required review metadata,
- missing provenance,
- locale completeness,
- advisory freshness/expiry,
- artifact checksum,
- artifact signature,
- manifest signature where applicable,
- compatibility fields,
- last-known-good fallback.

## 14.2 Release evidence
Release evidence must include:
- content family changed,
- sensitivity tier,
- reviewer roles and approvals,
- validation output,
- artifact id/version,
- signing key id,
- activation pointer state,
- rollback candidate,
- device/runtime proof for changed high-risk content where applicable.

## 14.3 No fake proof rule
Structured validation is not scholar sign-off.
A screenshot is not runtime compatibility proof.
Checksum success is not publisher-authenticity proof.

---

# 15. Definition of done

Governed content publishing is ready when:
- content families are modeled,
- sensitivity tiers are assigned,
- required review roles are enforced,
- provenance and review records are complete,
- artifacts are immutable,
- artifacts are signed where remotely distributed,
- activation pointers are protected,
- advisory sources have freshness metadata,
- runtime uses last-known-good fallback safely,
- emergency correction and rollback are auditable,
- release evidence satisfies file `28`.

---

# 16. AI-agent checklist

Before editing content-related code or content data, an AI agent must:
1. Read files `12`, `15`, `18`, `22`, `23`, `26`, `28`, `29`, `30`, and `31`.
2. Read `CONTRACTS/content_pack_trust_chain_contract.yaml`.
3. Read `CONTRACTS/advisory_source_registry.schema.yaml` when safety/advisory content is affected.
4. Identify content family and sensitivity tier.
5. Confirm review requirements.
6. Never approve scholar-sensitive meaning.
7. Never publish or activate unsigned remote governed artifacts.
8. Update validation, fixtures, and release evidence together.

---

End of file.