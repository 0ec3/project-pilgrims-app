# 26 — CONTENT MODEL, SCHOLAR REVIEW, AND PUBLISHING WORKFLOW

## Document status
- **Type:** Normative content-governance and publishing contract
- **Priority:** Highest
- **Audience:** Founder, product lead, content lead, religious-governance contributors, scholar reviewers, localization contributors, backend engineers, Flutter engineers, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical content model, governance boundaries, sensitivity tiers, scholar-review requirements, provenance rules, validation pipeline, publishing workflow, emergency correction path, and rollback behavior for governed content used by Pilgrims Mobile App.
- **Authority level:** This file is the canonical source of truth for governed content structure and publishing workflow. If implementation, tooling, runtime behavior, or review operations diverge from this file, this file wins unless a higher-level normative document or approved decision record explicitly changes it.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `06-SYSTEM-ARCHITECTURE.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`, `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`, `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `17-ANALYTICS-OBSERVABILITY-AND-PERFORMANCE-BUDGETS.md`, `18-FEATURE-RITUALS-RIC-AND-RELIGIOUS-CONTENT.md`, `22-FEATURE-PHRASEBOOK-EMERGENCY-SAFETY-AND-ASSISTIVE-TOOLS.md`, `23-FEATURE-OFFLINE-PACKS-AUDIO-AND-CONTENT-DISTRIBUTION.md`, `24-FEATURE-ACCOUNT-SUBSCRIPTIONS-ENTITLEMENTS-AND-SETTINGS.md`
- **Related files:** `05`, `11`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This file exists because the app depends on governed content in domains where incorrect wording, weak provenance, missing review, or unsafe publishing operations could directly damage user trust and product correctness.

Without a canonical content-governance contract, teams and AI agents often create several expensive failures:
- ritual meaning drifts into code or ad hoc copy edits,
- translations subtly change religious meaning,
- packs ship content that cannot be traced to approved sources,
- emergency fixes are made informally and become impossible to audit,
- runtime uses content that passed no schema or referential-integrity checks,
- rollback becomes unsafe because published artifacts were mutated in place,
- content operations quietly invent a generic CMS and backend surface that the product architecture never approved.

This file prevents those failures by defining:
- what counts as governed content,
- which content requires scholar review,
- which content requires other review types instead,
- how governed content is modeled,
- how provenance and approval records are attached,
- how validation and publication work,
- how immutable artifacts reach the app,
- how emergency correction and rollback must work,
- how AI agents may assist without becoming approval authorities.

---

# 2. Feature purpose and user value

## 2.1 Governance purpose
This governance module exists to ensure that content used by the app remains:
- trustworthy,
- traceable,
- reviewable,
- local-first compatible,
- versioned,
- rollback-safe,
- and resilient to AI-assisted implementation drift.

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
Content contributors, reviewer agents, engineers, and release operators should be able to answer questions like:
- What content families exist?
- Which changes require scholar review?
- Which published version is active?
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
- localization and transliteration governance as they affect governed content,
- provenance and approval metadata,
- validation requirements before approval and publication,
- publishing outputs and artifact rules,
- emergency correction workflow,
- rollback rules for governed content,
- runtime consumption boundaries for published content.

## 3.2 Out of scope
This file does **not** include:
- a full visual design for internal editorial tools,
- a promise that v1 ships a rich browser CMS,
- generalized cloud document management,
- open-ended AI generation of religious rulings,
- redefinition of runtime pack lifecycle already owned by file `15`,
- redefinition of API contracts already owned by file `14`,
- redefinition of feature-facing ritual UX already owned by file `18`,
- store subscription truth,
- general legal/compliance policy beyond content-governance implications.

## 3.3 Boundary with file `18`
File `18` defines the feature-facing contract for Rituals, RIC, remedies, citations, and governed religious-content behavior.

This file defines the deeper content-governance machinery behind those behaviors, including:
- authoring structure,
- scholar approval,
- provenance storage,
- draft/review/approved/published workflow,
- emergency correction,
- rollback safety.

## 3.4 Boundary with file `22`
File `22` defines user-facing behavior for Phrasebook, Emergency, Safety, and assistive tools.

This file governs the content operations behind those assets, including:
- source-of-truth rules,
- locale completeness,
- verification-date expectations for emergency numbers or official handoff helpers,
- publishing and rollback behavior.

## 3.5 Boundary with file `14`
This file must **not** invent a large generic live content API.

Current runtime publication surfaces remain intentionally small:
- app-bundled last-known-good content,
- downloadable artifacts discoverable through approved pack/manifest mechanisms,
- limited configuration/flags surfaces where already documented.

If future product direction requires a dedicated content metadata API, file `14` must be updated together with this file.

## 3.6 Boundary with file `15`
File `15` owns:
- offline capability tiers,
- manifest caching,
- pack immutability,
- local inventory,
- storage and integrity verification.

This file defines which governed content becomes publishable artifacts and what trust metadata those artifacts must carry.

## 3.7 Boundary with file `12`
File `12` remains the canonical source for:
- copy tone,
- supported languages,
- localization architecture,
- RTL behavior,
- accessibility communication rules.

This file applies those principles specifically to governed content and review workflow.

---

# 4. Product rules that govern this module

## 4.1 Governed-content rule
Any content that influences ritual correctness, remedy meaning, religious classification, or user-facing religious confidence must come from governed content, not widget code or casual copy edits.

## 4.2 No unsupervised AI-authority rule
AI may assist drafting, linting, translation scaffolding, or structured transformation, but AI must not become the approval authority for religious meaning, remedy logic, or publication.

## 4.3 Immutable-publication rule
A published artifact is immutable.
If meaning, wording, structure, or approval-relevant metadata changes, publish a new version instead of mutating the existing artifact in place.

## 4.4 Traceability rule
Every governed item that matters for correctness or trust must be traceable to:
- an origin source or source note,
- a review activity,
- a responsible human role,
- and a published version.

## 4.5 Offline-first publication rule
The publishing system must support the product’s offline-first promise.
This means essential ritual value cannot depend on a fragile live publishing service during ordinary runtime.

## 4.6 No hidden review bypass rule
There must be no hidden path where code, admin actions, or build scripts can publish scholar-sensitive content without the required review metadata.

## 4.7 No paywall-on-correctness rule
This workflow must preserve the product rule that correctness-related ritual guidance and remedy meaning are not gated behind supporter monetization.

## 4.8 Honest-correction rule
If a content issue is discovered, correction must be controlled and honest.
The system must not silently pretend a problematic version never existed.

## 4.9 Umrah-first content rule
Published defaults must remain Umrah-first unless season, scope, and approved publication inputs explicitly permit Hajj-specific exposure.

## 4.10 Small-online-surface rule
The content workflow must respect the existing architecture choice that the app does not rely on a giant always-live content backend for essential religious runtime.

---

# 5. Canonical terminology for this module

## 5.1 Governed content
Structured content whose meaning, correctness, presentation, or trustworthiness is controlled through this workflow.

## 5.2 Content family
A stable domain grouping of governed content such as ritual steps, remedy rules, citations, phrasebook phrases, emergency cards, or safety banners.

## 5.3 Content artifact
An immutable publishable output derived from reviewed source content and validation pipelines.

## 5.4 Provenance record
The metadata that explains where a governed content item came from, who changed it, what activity reviewed it, and which version became active.

## 5.5 Review record
A structured record that captures a reviewer role, decision, timestamp, and summary of why a change was approved or returned for changes.

## 5.6 Scholar-sensitive content
Governed content that changes religious meaning, ritual correctness, remedy guidance, classification, or scholarly interpretation and therefore requires scholar review.

## 5.7 Publication candidate
A validated, review-complete content set that is ready to be packaged into an immutable artifact.

## 5.8 Emergency correction
A controlled intervention used when a published content issue has material trust, correctness, or safety impact and must be mitigated quickly.

## 5.9 Last-known-good content
The most recent validated and trusted published artifact that the app can safely continue using locally.

## 5.10 Superseded version
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
Responsible for validation pipelines, artifact generation, manifest integration, integrity checks, and safe runtime loading.

## 6.8 AI-agent role boundary
AI agents may:
- generate structured draft suggestions,
- scaffold locale files,
- normalize schemas,
- generate diff summaries,
- help produce validation reports.

AI agents must not:
- self-approve scholar-sensitive meaning,
- invent source provenance,
- fabricate reviewer identities,
- publish content directly without a human-owned approval path.

---

# 7. Governed content family model

## 7.1 Core governed content families
The system should treat at least the following as governed content families where relevant:
- ritual definitions,
- path definitions,
- step definitions,
- madhhab-aware rule sets,
- remedy definitions,
- citation references,
- ritual explanatory detail,
- phrasebook categories and phrases,
- emergency cards,
- emergency numbers and official-handoff notes,
- safety/advisory banners where they are content-driven,
- transliteration resources where meaning or usability depends on them,
- audio reference manifests tied to governed text.

## 7.2 Family ownership rule
Every governed family must have a clear owner and must not drift into anonymous “misc content” buckets.

## 7.3 Shared-vs-feature rule
Shared content families may exist, but feature-specific families should remain grouped by product domain where practical.

## 7.4 Content-family stability rule
Stable family identifiers must not be renamed casually because they affect analytics, artifact naming, fixtures, tests, and rollback history.

---

# 8. Content sensitivity tiers and required review

## 8.1 Tier A — scholar-sensitive correctness content
Tier A includes content that affects:
- ritual correctness,
- remedy outcomes,
- pillar / wajib / sunnah interpretation,
- scholar-linked warnings,
- citation-linked religious conclusions,
- hypothetical resolver outcomes that affect next-step guidance.

### Required review
- content/editor review,
- scholar review,
- validation pipeline pass,
- publication approval by designated publisher/release owner.

## 8.2 Tier B — religious-supportive explanatory content
Tier B includes:
- plain-language explanation that supports governed ritual meaning,
- translated or simplified explanation tied to approved religious meaning,
- transliteration or pronunciation helpers attached to religious content.

### Required review
- content/editor review,
- scholar review where meaning could drift,
- localization review where language variants exist,
- validation pipeline pass.

## 8.3 Tier C — operational assistive content
Tier C includes:
- phrasebook phrases,
- emergency cards,
- emergency numbers,
- official-service handoff notes,
- safety banner copy,
- assistive templates.

### Required review
- content/editor review,
- localization review where localized,
- operational verification where official or time-sensitive claims are made,
- scholar review only when the content makes religious claims rather than practical assistance claims.

## 8.4 Tier D — structured non-sensitive support content
Tier D includes structured content that ships through the same pipeline but does not change religious meaning or operational trust claims.

### Required review
- standard content review,
- localization review where needed,
- validation pipeline pass.

## 8.5 Escalation rule
If there is uncertainty about whether content is Tier A/B/C, classify upward to the safer review path until a documented decision says otherwise.

---

# 9. Source-of-truth and authoring model

## 9.1 V1 source-of-truth rule
For v1, the canonical source of truth for governed content should be a controlled repository or equivalent structured source system with version history, code review, validation automation, and recoverable diffs.

## 9.2 No rich-CMS assumption rule
This spec does **not** require a complex live CMS for v1.
A repository-driven workflow is the default safe assumption unless a later approved decision adds a CMS and updates related files.

## 9.3 Authoring format rule
Governed content should be authored in structured machine-validated formats such as JSON, YAML, or equivalent schema-governed assets.
Freeform documents may support review discussion but must not become the runtime source of truth.

## 9.4 Human-readable organization rule
Structured source layout should remain human-auditable and domain-oriented.

### Representative layout
```text
content/
  rituals/
    umrah/
      paths.json
      steps.json
      rules_hanafi.json
      rules_shafii.json
      remedies.json
      citations.json
      strings/
        en.json
        ar.json
        id.json
      transliteration/
        en.json
        id.json
  phrasebook/
    categories.json
    phrases_base.json
    phrases_ar.json
    phrases_en.json
    phrases_id.json
    ranking_rules.json
  emergency/
    cards.json
    numbers.json
    sms_templates.json
  safety/
    banners.json
```

Actual directory names may vary, but the contracts in this file remain canonical.

## 9.5 Build-derived artifact rule
Runtime artifacts must be generated from reviewed source content rather than being hand-edited binary outputs.

## 9.6 Review-diff rule
The authoring system must allow reviewers to inspect meaningful diffs at content-object level, not only opaque generated files.

---

# 10. Canonical content artifact model

## 10.1 Artifact purpose
A content artifact is the immutable unit that runtime trusts after review and publication.

## 10.2 Required artifact metadata
Every published content artifact should expose at minimum:
- `artifact_id`
- `content_family`
- `content_version`
- `schema_version`
- `generated_at`
- `locale_set`
- `season_scope`
- `checksum_sha256`
- `review_record_refs[]`
- `provenance_bundle_ref`
- `min_app_version?`
- `pack_id?` when distributed through packs

## 10.3 Versioning rule
Versioning must be explicit and stable.

Recommended posture:
- `content_family` identifies the domain,
- `content_version` increments per family,
- `artifact_id` uniquely identifies the immutable output.

## 10.4 Schema-version rule
Artifact schema version and content version are different concepts.
A schema change must not be hidden as a normal content edit.

## 10.5 Family-specific packaging rule
Different governed families may publish separately, but cross-family dependencies must still validate before publication.

## 10.6 Immutability rule
Once published, an artifact must never be edited in place.
Correction requires a new artifact version and an updated publication pointer or rollout decision.

---

# 11. Canonical governed item requirements

## 11.1 Stable-id rule
Every governed item must have a stable id that survives wording changes.

## 11.2 Separation-of-concerns rule
Governed items should separate:
- structural meaning,
- localized presentation,
- optional transliteration,
- citation relationships,
- audio references,
- provenance metadata.

## 11.3 Locale strategy rule
Where practical, structural objects should remain locale-agnostic and point to localized content payloads or keyed locale resources.
If a family intentionally stores locale maps inline, that choice must still validate predictably.

## 11.4 Applicability rule
Governed items should declare only the scope they genuinely support, such as:
- mode,
- path,
- season,
- madhhab,
- locale,
- entitlement-relevant enrichment where allowed.

## 11.5 Referential-integrity rule
Any reference to:
- step ids,
- remedy ids,
- citation ids,
- locale records,
- transliteration records,
- audio assets,
- related pack ids,

must resolve successfully before publication.

## 11.6 No UI-hardcode rule
Religious rules, remedy mappings, and other governed meanings must not be duplicated as hardcoded widget logic.

---

# 12. Localization, Arabic, and transliteration governance

## 12.1 Meaning-preservation rule
Localization of governed content must preserve approved meaning, not merely produce natural-sounding paraphrase.

## 12.2 Arabic distinction rule
Where the product presents Arabic source text, translated meaning, and transliteration, those must remain structurally distinct.
They are not interchangeable fields.

## 12.3 Transliteration review rule
Transliteration must be intentionally reviewed for usability and consistency.
It must not be generated casually and published without human review.

## 12.4 Locale completeness rule
Publication must fail when a required locale for the target artifact is missing critical fields.

## 12.5 Partial-locale rule
A content family may intentionally ship with a smaller locale set only when the artifact metadata declares that scope honestly and the user-facing product behavior remains aligned with supported-language promises.

## 12.6 RTL safety rule
Governed content containing mixed Arabic and Latin data must be tested for bidi safety before publication.

## 12.7 Simplification rule
Shorter copy is allowed only when it preserves approved meaning.
Especially for Tier A/B content, simplification must not change religious meaning.

---

# 13. Provenance and approval metadata model

## 13.1 Purpose
Provenance exists so the system can explain where a governed item came from, what activity changed it, and which humans approved it.

## 13.2 Minimum provenance elements
Every governed publication candidate should be able to trace:
- the content entity,
- the authoring or editing activity,
- the responsible human role,
- the required review activity,
- the resulting approved version.

## 13.3 Minimum item-level provenance fields
Recommended minimum item-level metadata:
- `id`
- `source_refs[]`
- `change_note`
- `edited_by`
- `edited_at`
- `review_required`
- `review_record_refs[]`

## 13.4 Minimum publication-level provenance fields
Recommended minimum publication metadata:
- `artifact_id`
- `content_family`
- `content_version`
- `candidate_commit_or_source_ref`
- `validation_report_ref`
- `review_record_refs[]`
- `published_by`
- `published_at`

## 13.5 Source-reference rule
Source references may be concise and structured, but they must be honest and recoverable.
The system must not claim provenance it cannot substantiate.

## 13.6 Review-record rule
A review record must capture at minimum:
- reviewer role,
- reviewer identity or accountable reviewer reference,
- decision,
- timestamp,
- short notes or rationale,
- content scope reviewed.

## 13.7 No fake-approval rule
Placeholder or synthetic approval records are forbidden.

---

# 14. Canonical content lifecycle

## 14.1 Lifecycle rule
The canonical authoring lifecycle remains:
1. `Draft`
2. `Review`
3. `Approved`
4. `Published`

## 14.2 Draft
Content is being authored or revised.
It is not yet eligible for publication.

## 14.3 Review
Content is frozen enough for structured review.
Required validations should already pass before entering formal review where practical.

## 14.4 Approved
The required human reviews have completed successfully for the defined scope and version.
Approval alone does not mean the content is already available to app runtime.

## 14.5 Published
The approved content has been packaged into an immutable artifact and made active through an approved release path.

## 14.6 Superseded-version rule
Older published versions may later become superseded by newer published versions, but supersession does not rewrite the canonical lifecycle.

## 14.7 Change-scope rule
A meaningful change to approved or published governed content returns the changed material to Draft/Review for the new version.

---

# 15. Review workflow

## 15.1 Standard workflow
The default workflow should be:
1. author/edit structured source,
2. run local and CI validation,
3. enter Review,
4. complete required human reviews,
5. mark Approved,
6. generate publication candidate,
7. publish immutable artifact,
8. activate through the approved distribution path.

## 15.2 Review-entry rule
Content should not enter formal review if basic schema and referential-integrity validation are already known to fail.

## 15.3 Scope-lock rule
The exact reviewed scope must be clear.
Reviewers should not be approving an undefined moving target.

## 15.4 Diff-summary rule
Every formal review should include a short human-readable summary of what changed and why.

## 15.5 Batch-size rule
Large mixed-content batches increase review risk.
Prefer smaller coherent publication candidates when practical, especially for scholar-sensitive content.

---

# 16. Scholar review workflow

## 16.1 Scholar-review trigger rule
Scholar review is mandatory whenever a change affects:
- ritual step meaning,
- remedy meaning,
- classification such as pillar/wajib/sunnah,
- resolver outcome logic,
- religious warnings,
- citation-linked religious claims,
- translated or simplified wording that could change religious meaning.

## 16.2 Scholar-review input rule
Scholar reviewers must review the structured meaning-bearing content, not only polished UI screenshots.

## 16.3 Scholar-review output rule
The review output must result in one of:
- approved for the defined scope,
- changes requested,
- rejected for publication in current form.

## 16.4 Dual-control rule for Tier A publication
Tier A publication requires at minimum:
- one accountable scholar review record,
- one accountable non-scholar publication owner approval,
- successful validation evidence.

## 16.5 Localization implication rule
If scholar-sensitive content is localized, the localization that could alter meaning must be included in scholar-review scope or in an explicitly linked follow-up review path that preserves meaning.

## 16.6 No UI-only approval rule
It is not enough for a scholar reviewer to approve how a screen “looks.”
Approval must relate to the meaning-bearing governed content.

## 16.7 Review-trace rule
Scholar approval must be attached to the exact version or publication candidate that will be packaged.

---

# 17. Validation and quality gates before publication

## 17.1 Required validation classes
At minimum, governed content publication should validate:
- schema correctness,
- referential integrity,
- enum validity,
- locale completeness for required locales,
- bidi-safe handling where applicable,
- transliteration structure where applicable,
- citation reference validity,
- pack/audio reference validity where applicable,
- season-scope and Umrah-first leakage rules,
- artifact metadata completeness,
- required review-record presence for the target sensitivity tier.

## 17.2 Ritual-specific validation
Tier A ritual content must additionally validate:
- step graph integrity,
- path membership integrity,
- rule coverage for supported scenarios,
- remedy reference coverage,
- no Hajj-only leakage into Umrah-first default artifacts where not allowed,
- no missing citation references where content expects them.

## 17.3 Emergency/assistive validation
Phrasebook and emergency content must validate:
- locale coverage,
- category/phrase reference integrity,
- template placeholder integrity,
- phone/official-handoff metadata shape,
- absence of unsupported official claims in fields reserved for verification notes.

## 17.4 Validation-report rule
Every publication candidate must produce a structured validation report that can be attached to the publication provenance bundle.

## 17.5 Fail-closed rule
If required validation fails, publication must stop.
The system must not silently downgrade mandatory checks.

---

# 18. Publishing model and distribution paths

## 18.1 Publishing outputs
Governed content may reach runtime through these approved paths:
- bundled baseline content shipped with the app,
- immutable content artifacts distributed through existing pack/manifest mechanisms where approved,
- tightly constrained flags/config pointers that select between already-published safe artifacts or safe content states.

## 18.2 No generic live-rules API rule
The app must not depend on a large live API that streams ritual logic or scholar-sensitive meaning on demand unless the architecture is explicitly changed in file `14` and related files.

## 18.3 Baseline bundled-content rule
Essential last-known-good governed content for core ritual value should ship with the app or otherwise remain available locally in a way consistent with the offline-first contract.

## 18.4 Pack-distributed artifact rule
Optional larger governed artifacts may be distributed as content packs or mixed-content packs when that remains aligned with files `15` and `23`.

## 18.5 Manifest-addressability rule
If a governed artifact is distributed remotely, discovery should happen through existing approved manifest-driven mechanisms rather than hardcoded URLs.

## 18.6 Activation rule
Publishing and activation are related but distinct.
An artifact may be published yet not immediately activated for all users if rollout policy says otherwise.

## 18.7 Minimum activation metadata
Activation decisions should be able to state:
- which artifact version is active,
- which family it belongs to,
- which season or scope it applies to,
- whether it supersedes a prior active version.

---

# 19. Runtime loading and offline consumption rules

## 19.1 Runtime trust rule
Runtime may only load governed content that passed publication through this workflow or bundled last-known-good equivalents.

## 19.2 Local-first rule
The app should prefer the latest valid local artifact available and continue functioning offline with it.

## 19.3 Last-good fallback rule
If a newly downloaded governed artifact is invalid, corrupted, or incompatible, runtime must fall back to the last-known-good valid artifact rather than improvising behavior.

## 19.4 No half-published rule
Partially downloaded or partially validated governed artifacts must not appear as active runtime truth.

## 19.5 Truthfulness rule
If runtime is using stale but previously published governed content, the system may surface freshness context where it matters, but must not imply live certainty it does not have.

## 19.6 App-update compatibility rule
If a content artifact requires a newer app version, runtime must reject it safely and preserve the previously valid artifact.

---

# 20. Emergency correction and rollback workflow

## 20.1 Trigger conditions
Emergency correction may be triggered by issues such as:
- incorrect ritual remedy meaning,
- incorrect classification that affects correctness,
- broken or missing critical governed content,
- harmful translation drift in scholar-sensitive content,
- materially wrong emergency or official-handoff content,
- artifact corruption affecting runtime correctness.

## 20.2 First action rule
The first action is to protect users, not to protect process appearance.
Possible immediate actions include:
- halt rollout,
- disable risky exposure through approved flags if possible,
- repoint to a last-known-good artifact,
- publish a corrected new artifact,
- hide unsupported seasonal entry points.

## 20.3 No in-place mutation rule
Emergency correction must still respect immutable-publication rules.
Do not patch a published artifact in place.

## 20.4 Rollback preference rule
If a known safe prior published version exists, rollback to it is preferred over leaving users on a disputed version while a fix is being prepared.

## 20.5 Emergency-review rule
Emergency correction for Tier A content still requires accountable human approval.
The process may be faster, but it may not become unowned.

## 20.6 Incident documentation rule
Every emergency correction must produce a concise incident record including:
- affected family and versions,
- user impact summary,
- mitigation path,
- final corrective action,
- follow-up actions to prevent recurrence.

## 20.7 Post-incident rule
If emergency correction revealed a workflow weakness, update this file or related files rather than treating the event as a one-off anomaly.

---

# 21. Security, privacy, and trust boundaries

## 21.1 Minimal exposure rule
The mobile client should consume only the runtime-facing content artifacts and trust metadata it actually needs.
Editorial notes, reviewer-private discussion, and internal commentary must not leak into the app.

## 21.2 Service-only governance rule
If governance records are stored in backend systems, they should remain service-only by default and outside general end-user API exposure.

## 21.3 Approval-integrity rule
Only authorized roles may create or finalize approval records.

## 21.4 Auditability rule
Publication, rollback, and emergency-correction operations must be recoverable through operational logs or audit records.

## 21.5 No fabricated officiality rule
Emergency or handoff content must not claim official verification or authority status beyond what governance records can support.

---

# 22. API, backend, and storage boundaries

## 22.1 Runtime-consumption posture
The client runtime should receive published artifacts, manifest metadata, or safe selection flags rather than raw editorial workflow objects.

## 22.2 Service-boundary rule
Editorial workflow systems may exist behind service boundaries, but they must not quietly enlarge the public app API surface without synchronized contract updates.

## 22.3 Local persistence posture
On-device runtime may cache:
- last-known-good governed artifacts,
- artifact metadata,
- relevant manifest snapshots,
- validation outcomes needed for safe activation,
- selected freshness metadata where useful.

## 22.4 No duplicate-truth rule
The app must not create an independent second truth for governed content outside the published artifacts and approved local fallback cache.

## 22.5 Artifact-storage rule
Downloaded governed artifacts must use the same integrity and app-private storage posture required by files `15` and `23`.

---

# 23. Analytics, observability, and audit requirements

## 23.1 Product-analytics restraint rule
User-facing analytics must remain privacy-light and should not log sensitive religious inputs or freeform content text.

## 23.2 Runtime observability priorities
The system should capture high-signal operational events such as:
- content artifact load success/failure,
- content schema mismatch,
- missing required references,
- stale-content fallback activation,
- content version mismatch warnings,
- emergency rollback activation,
- invalid publication candidate rejection.

## 23.3 Recommended operational fields
Operational logs or observability events should include where relevant:
- `content_family`
- `content_version`
- `artifact_id`
- `schema_version`
- `result`
- `failure_code`
- `source_of_activation`
- `fallback_used`
- `network_state`
- `locale`

## 23.4 Audit-log rule
Publication and rollback actions must be auditable even if they are not all emitted as product analytics events.

## 23.5 Redaction rule
Operational traces must not leak reviewer-private notes, sensitive user data, or internal-only source documents to ordinary analytics pipelines.

---

# 24. Testing and validation requirements

## 24.1 Required automated coverage
Automated checks must cover at minimum:
- schema validation,
- referential integrity,
- locale completeness for required locales,
- transliteration-field integrity where applicable,
- step-graph validity for ritual content,
- season-scope leakage checks,
- pack/audio reference integrity,
- artifact immutability assumptions,
- last-known-good fallback behavior,
- content-version compatibility checks.

## 24.2 Required manual review validation
Manual validation must cover at minimum:
- scholar-sensitive meaning changes,
- simplified wording that could change meaning,
- Arabic and transliteration presentation quality,
- phrasebook and emergency-content trustworthiness,
- rollback rehearsal for a governed artifact,
- emergency-correction drill for at least one high-severity scenario.

## 24.3 Device/runtime validation
On representative devices, verify:
- bundled baseline content loads correctly,
- downloaded governed artifacts activate correctly,
- stale-content fallback behaves honestly offline,
- invalid artifact does not replace last-known-good,
- app kill/relaunch preserves safe content activation state.

## 24.4 Fake-success warning
A clean publication dashboard is not enough evidence.
The workflow is not trustworthy unless runtime fallback, rollback, offline continuity, and review integrity are also proven.

---

# 25. Definition of done for this module

This module is not ready unless all of the following are true:
- governed content families are clearly classified,
- Tier A/B/C review requirements are explicit,
- scholar-sensitive content cannot bypass required approval,
- provenance metadata is recoverable,
- validation gates are fail-closed,
- published artifacts are immutable,
- offline runtime can continue using last-known-good governed content,
- emergency correction and rollback are operationally defined,
- phrasebook/emergency/ritual content paths stay aligned with files `18`, `22`, and `23`,
- AI-agent assistance is bounded and cannot self-authorize publication.

---

# 26. Cross-file dependency rules

## 26.1 If governed ritual structure changes
Update:
- this file,
- file `18`,
- file `12` where copy/localization structure changes,
- file `15` or `23` if artifact distribution assumptions change,
- file `27` and `28` where verification requirements change.

## 26.2 If lifecycle states or canonical content terms change
Update:
- this file,
- file `04`,
- file `05` if roadmap/module implications change,
- any affected API, analytics, or test fixtures.

## 26.3 If publication paths or APIs change
Update:
- this file,
- file `14`,
- file `15`,
- file `23`,
- file `30` if operational runbooks change.

## 26.4 If supported governed locales change
Update:
- this file,
- file `12`,
- affected feature-family files,
- test matrices and release evidence requirements.

## 26.5 If emergency correction posture changes
Update:
- this file,
- file `28`,
- file `29`,
- file `30`.

---

# 27. Anti-patterns forbidden by this document

The following are forbidden unless explicitly approved.

## 27.1 Hardcoding religious meaning in widgets or scattered business logic
Forbidden.

## 27.2 Letting AI-generated religious wording publish without accountable human review
Forbidden.

## 27.3 Mutating published artifacts in place
Forbidden.

## 27.4 Publishing scholar-sensitive content without scholar review metadata
Forbidden.

## 27.5 Using a generic live content API for essential ritual runtime without architecture approval
Forbidden.

## 27.6 Treating transliteration as optional decoration with no quality review
Forbidden.

## 27.7 Shipping locale-incomplete governed content as if full language support exists
Forbidden.

## 27.8 Claiming official verification for emergency or handoff content without evidence
Forbidden.

## 27.9 Rolling forward or rolling back content without an auditable record
Forbidden.

## 27.10 Replacing last-known-good content with an invalid or partially validated artifact
Forbidden.

---

# 28. Implementation priorities

## 28.1 Phase 1 priorities
Implement first:
- governed content family classification,
- source-of-truth repository structure,
- schema and referential-integrity validation,
- Tier A scholar-review gating,
- immutable artifact generation,
- last-known-good runtime fallback.

## 28.2 Phase 2 priorities
Then add:
- stronger locale/transliteration validation,
- operational review dashboards or tooling,
- explicit publication candidate summaries,
- emergency-correction drills,
- better provenance bundle export for audits.

## 28.3 Phase 3 priorities
Then refine:
- tooling ergonomics for editors and scholars,
- more granular rollout controls for governed artifacts,
- richer diff visualization for structured content,
- more automated regression fixtures for ritual rule changes.

---

# 29. When this file must be updated

This file must be updated whenever any of the following changes:
- governed content families,
- content sensitivity tiers,
- required review roles,
- scholar-review posture,
- publication artifact structure,
- runtime content distribution path,
- provenance metadata requirements,
- emergency correction or rollback workflow,
- AI-agent permissions in content operations,
- release evidence requirements for governed content.

If these truths change but this file is not updated, ritual correctness, assistive-content trust, offline safety, and rollback reliability will drift quickly.

---

# 30. Summary

This file defines the canonical content-governance contract for Pilgrims Mobile App.

It establishes:
- what governed content is,
- which content requires scholar review,
- how content families are modeled,
- how provenance and approval records work,
- how validation gates prevent unsafe publication,
- how immutable artifacts are published,
- how runtime safely consumes last-known-good governed content,
- how emergency correction and rollback must work,
- how AI agents may assist without becoming authorities.

Its purpose is to ensure that governed content in Pilgrims Mobile App remains:
- trustworthy,
- traceable,
- respectful,
- offline-compatible,
- rollback-safe,
- and safe for long-term AI-assisted implementation.
