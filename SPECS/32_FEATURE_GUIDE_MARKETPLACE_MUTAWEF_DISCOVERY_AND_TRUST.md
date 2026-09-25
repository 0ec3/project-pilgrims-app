# 32 — FEATURE: GUIDE MARKETPLACE, MUTAWEF DISCOVERY, AND TRUST

## Document status
- **Type:** Normative feature-family specification
- **Priority:** Highest within its feature domain, subject to the authority hierarchy in files `01`, `04`, and `31`
- **Audience:** Founder, product lead, design lead, compliance/legal reviewer, content/religious-governance lead, Flutter engineers, backend engineers, QA, support/moderation contributors, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical product contract for the user-facing **Hire a Guide** feature, including the narrow marketplace exception, Mutawef provider eligibility, trust semantics, listings, discovery, direct-contact handoff, moderation, privacy, stale/offline behavior, religious-governance boundaries, tests, and release blockers.
- **Authority level:** This file is the canonical feature source of truth for Guide Marketplace behavior. It does not override product-wide safety, religious-correctness, privacy, offline, accessibility, or release invariants owned by higher-level specs and machine-readable contracts.
- **Last-updated-by:** Hire a Guide specification architecture pass (2026-09-26)
- **Primary dependencies:** `01`, `03`, `04`, `06`, `07`, `08`, `09`, `10`, `11`, `12`, `13`, `14`, `15`, `17`, `18`, `24`, `26`, `27`, `28`, `29`, `30`, `31`, `CONTRACTS/guide_marketplace_trust_contract.yaml`, `CONTRACTS/screen_feature_traceability.yaml`
- **Related files:** `20`, `22`, `25`

---

# 1. Purpose

Hire a Guide exists to help a pilgrim find a lawfully eligible human guide for narrowly defined Umrah accompaniment when the pilgrim wants human support beyond the app.

This feature is a controlled exception to the product's general marketplace exclusion. It must strengthen the core pilgrimage mission without turning PILGRIMS into a travel super-app, package marketplace, social network, booking platform, or payments intermediary.

The initial product posture is:

**Verified Discovery + Explicit Direct Contact**

PILGRIMS may help the pilgrim discover a provider, understand the provider's current trust evidence and advertised service, and explicitly hand off to an approved external contact channel.

PILGRIMS does not, in this V1 contract:
- accept or settle service payments,
- issue booking documents,
- hold escrow,
- own a service wallet,
- run generic chat,
- sell accommodation, transport, visas, flights, packages, tickets, or restaurants,
- guarantee provider conduct,
- convert provider advice into canonical religious guidance.

---

# 2. Current regulatory evidence and legal posture

## 2.1 Verification date
The regulatory facts in this section were re-checked on **2026-09-26** against current official Saudi sources.

## 2.2 Saudi Tour Guiding Regulation
The amended Saudi **Tour Guiding Regulation** published in Umm Al-Qura on 2026-09-11 states, among other things, that:
- tourist guiding may not be practiced without a current Ministry of Tourism licence;
- a licence may cover regional and/or specialized guiding categories;
- the licence records category and approved language information;
- a licensed guide dealing through electronic sites/platforms must display licence number, category, and licensed language information;
- a licensed guide must not provide services that require a separate travel-and-tourism-services licence or another licence;
- when contracting directly with a tourist, the guide has service, price, payment, cancellation, refund, booking-document, privacy, and related duties.

Official source:
- Umm Al-Qura, **لائحة الإرشاد السياحي**, 2026-09-11: https://www.uqn.gov.sa/decisions-and-regulations/4001829

## 2.3 Saudi Travel and Tourism Services Regulation
The amended **Travel and Tourism Services Regulation** published in Umm Al-Qura on 2026-09-11:
- defines travel/tourism services to include arranging tourism services;
- treats a website or equivalent electronic location as a possible travel/tourism-services facility;
- expressly includes **arranging tourist guiding services** within the licensed Travel Agency category;
- requires licensed facilities to deal with appropriately licensed/authorized providers and imposes consumer-rights, complaint, pricing, booking, privacy, and record obligations.

Official source:
- Umm Al-Qura, **لائحة خدمات السفر والسياحة**, 2026-09-11: https://www.uqn.gov.sa/decisions-and-regulations/4001822

## 2.4 Mutawef versus Tourist Guide
The official Nusuk Umrah product surface currently presents **Tour Guide** and **Mutawef During Umrah** as distinct service labels.

This distinction is product/regulatory evidence that the concepts must not be collapsed, but it is not by itself a legal authorization rule for independent paid Mutawef services.

Official source:
- Nusuk Umrah package/service surfaces: https://umrah.nusuk.sa/

## 2.5 Ministry of Hajj and Umrah context
Ministry of Hajj and Umrah materials govern licensed Umrah companies/establishments and services for Umrah performers, including official mechanisms for checking licensed Umrah companies.

These materials do not, from the evidence verified in this pass, establish a sufficiently clear public rule that an independently operating individual may provide paid Mutawef ritual accompaniment solely because they hold a Ministry of Tourism tourist-guide licence.

Official sources:
- Licensed Umrah companies inquiry: https://haj.gov.sa/
- Executive Regulations for Regulating Umrah Services: https://haj.gov.sa/s-core/-/media/Project/HAJJ/PDF/Document-Library/Executive-Regulations-for-Regulating-Umrah-Services.pdf

## 2.6 Saudi e-commerce/intermediary obligations
Saudi Ministry of Commerce materials for the E-Commerce Law and implementing regulation cover electronic service-provider disclosures, consumer contract information, misleading advertisements, consumer-data protection, complaints, and electronic platforms acting as intermediaries.

Official source:
- Ministry of Commerce E-Commerce Law portal: https://mc.gov.sa/ar/ecc/pages/default.aspx

## 2.7 Saudi PDPL
Saudi Data & AI Authority guidance for the Personal Data Protection Law requires, among other principles:
- lawfulness, fairness, and transparency,
- purpose limitation,
- data minimization,
- storage limitation,
- accuracy,
- integrity/confidentiality,
- accountability.

This feature therefore adopts the rule:

**Verify more; store less.**

Official source:
- SDAIA Personal Data Protection knowledge center: https://dgp.sdaia.gov.sa/

## 2.8 P0 unresolved legal blockers
The following are **unresolved and no-ship** until an accountable Saudi legal/compliance authority resolves them:

### LEGAL-GUIDE-001 — Platform facilitation classification
Determine whether PILGRIMS' proposed discovery, ranking/filtering, provider-profile presentation, contact-intent creation, and direct-contact handoff constitute **arranging tourist guiding services** or otherwise require a Saudi travel/tourism-services licence, authorization, local entity structure, website documentation, guarantee/insurance, or other operator obligations.

Do not infer that "no payment" or "no in-app booking" automatically places PILGRIMS outside the regulated activity.

### LEGAL-GUIDE-002 — Paid Mutawef eligibility/authority
Determine the authority and legal relationship required for paid Umrah ritual accompaniment described as Mutawef service, including:
- whether an individual may offer it independently,
- whether the individual must be employed by or contracted through a licensed Umrah/service provider,
- what Ministry of Hajj and Umrah or Nusuk authorization applies,
- whether a Ministry of Tourism tourist-guide licence is required, sufficient, supplementary, or unrelated for this service,
- which credential(s) PILGRIMS may lawfully verify and display.

No public badge may say **Verified Mutawef**, **Official Mutawef**, or equivalent until this authority model is resolved and documented.

### LEGAL-GUIDE-003 — Final disclosure/operator obligations
Before public release, legal/compliance review must finalize the exact disclosures and operator obligations triggered by the approved business model, including e-commerce/intermediary, tax, complaint/support, professional licence display, consumer terms, and record-retention duties.

These blockers must remain visible in files `05`, `28`, and `29`.

---

# 3. Canonical terminology

## 3.1 Hire a Guide
The user-facing English feature name.

## 3.2 Guide Marketplace
The canonical internal feature-family name for discovery/trust architecture. "Marketplace" here does not authorize general travel commerce.

## 3.3 Mutawef
Canonical English transliteration for the Umrah ritual-accompaniment role in this specification, aligned with current official Nusuk English usage.

Arabic localization may use **مطوف** where reviewed and appropriate.

Do not create competing canonical identifiers such as `mutawwif`, `muthowwif`, or `mutawif` in code/contracts/specs. Legal citations may preserve the spelling used by the source.

## 3.4 Tourist Guide
A person licensed for tourist guiding under the applicable Ministry of Tourism regulation. This is not automatically the same as a Mutawef and does not automatically establish fiqh/scholarly authority.

## 3.5 Religious credential
A separately defined and verified qualification relevant to religious knowledge. It must not be inferred from a tourism licence.

## 3.6 PILGRIMS verification
A claim that PILGRIMS verified a specific fact against defined evidence at a defined time. It is never a general guarantee of character, scholarship, legality beyond the verified scope, or future conduct.

## 3.7 Credential freshness
The time-bounded state of a credential based on source, verification time, expiry, revocation status, and any required re-check interval.

---

# 4. Product fit and scope boundary

## 4.1 Narrow exception rule
Guide Marketplace is accepted only as a pilgrimage-specific exception serving the existing Umrah-first mission.

It does not remove the product-wide exclusion on:
- hotels,
- flights,
- travel-package comparison,
- generic tours,
- ride booking,
- restaurants,
- visa sales,
- ticketing,
- general concierge commerce,
- broad tourism marketplace behavior.

## 4.2 V1 in scope
V1 may include:
- provider application,
- credential/eligibility review,
- provider profile,
- narrowly defined Mutawef service listing,
- browse/search/filter,
- profile/detail,
- service area,
- languages,
- group-size capability,
- clear advertised pricing structure,
- current trust-signal presentation,
- explicit contact handoff,
- reports,
- listing/provider moderation,
- suspension,
- expiry,
- revocation,
- re-verification,
- audit history,
- privacy-safe operational analytics.

## 4.3 V1 out of scope
V1 does not include:
- in-app booking settlement,
- in-app payments,
- escrow,
- payment wallet,
- generic messaging/chat,
- automatic calls/messages,
- reviews/ratings,
- transaction-verified review claims,
- visa services,
- accommodation sales,
- transport arrangement or sales,
- flight/ticketing,
- package travel,
- broad tourism products,
- sponsored placement,
- lead fees,
- provider subscription,
- transaction commission.

Any later addition requires explicit scope/change control and applicable licensing review.

---

# 5. User segments and personas

## 5.1 Pilgrim segments
High-value users include:
- independent/backpacker Umrah pilgrims,
- first-time pilgrims,
- pilgrims without an agency Mutawef,
- small families/private groups seeking human ritual accompaniment,
- pilgrims who want human support in addition to the app.

## 5.2 Provider persona
A normal authenticated PILGRIMS user may apply to become a provider.

Provider capability is not an auth role toggle and is not a Supporter entitlement.

The provider must pass server-trusted eligibility and verification rules before becoming publicly discoverable.

---

# 6. Information architecture

## 6.1 Primary entry
Default entry:

**Tools → Hire a Guide**

## 6.2 Home
Home may show a low-priority contextual entry when relevant, but it must remain below:
1. current ritual/recovery,
2. emergency,
3. Save My Gate/orientation recovery,
4. urgent group coordination.

## 6.3 Simple Mode
Hire a Guide is not part of the default Simple Mode urgent set.

## 6.4 Primary navigation
No sixth primary tab is created.

The canonical primary navigation remains:
1. Home
2. Rituals
3. Map
4. Group
5. Tools

---

# 7. Canonical pilgrim journey

1. Pilgrim opens **Hire a Guide** from Tools or an approved low-priority contextual entry.
2. Marketplace root loads current network-trusted data or explicitly marked cached data.
3. Pilgrim searches/browses and filters.
4. Pilgrim opens a guide profile.
5. Profile clearly separates:
   - identity/profile information,
   - service listing,
   - applicable current credentials,
   - what PILGRIMS verified,
   - what PILGRIMS did not verify.
6. Pilgrim reads service scope, service area, language, group-size capability, pricing structure, inclusions/exclusions, and contact posture.
7. Pilgrim taps **Contact Guide**.
8. The app shows approved contact choices and a privacy/hand-off explanation where needed.
9. Pilgrim explicitly chooses a channel.
10. The operating system/external app opens.
11. PILGRIMS does not auto-message, retain conversation bodies, or imply that an external agreement is a PILGRIMS booking.

---

# 8. Canonical provider journey

1. User authenticates through the existing account system.
2. User starts provider application.
3. User supplies only the minimum required provider/eligibility information.
4. Required evidence is verified through approved sources/processes.
5. Application moves through governed server-trusted states.
6. Provider receives an approved/rejected/status outcome.
7. Eligible provider may create/edit allowed profile fields and draft listings.
8. Listing undergoes required review.
9. Listing becomes discoverable only while all applicable eligibility/trust conditions are current.
10. Provider may update ordinary profile/listing content but may not change verification/moderation fields.
11. Expiry, suspension, revocation, or legal-scope disablement removes public eligibility promptly.

---

# 9. Provider lifecycle

Canonical provider states:
- `DRAFT`
- `SUBMITTED`
- `UNDER_REVIEW`
- `VERIFIED`
- `REJECTED`
- `SUSPENDED`
- `EXPIRED`
- `REVOKED`

## 9.1 Allowed transition intent
Typical transitions:
- `DRAFT -> SUBMITTED`
- `SUBMITTED -> UNDER_REVIEW`
- `UNDER_REVIEW -> VERIFIED | REJECTED`
- `VERIFIED -> UNDER_REVIEW` for re-verification
- `VERIFIED -> SUSPENDED | EXPIRED | REVOKED`
- `SUSPENDED -> UNDER_REVIEW | REVOKED`
- `EXPIRED -> UNDER_REVIEW`

The exact transition table is mirrored by `CONTRACTS/guide_marketplace_trust_contract.yaml`.

## 9.2 Trusted state rule
Only trusted service/admin moderation paths may set:
- verification outcome,
- credential verification,
- suspension,
- expiry determination,
- revocation,
- public eligibility.

Provider clients must never self-authorize these states.

---

# 10. Trust model

## 10.1 No generic verified boolean
The public and internal model must not reduce trust to `is_verified=true`.

## 10.2 Candidate trust signals
A profile may expose only trust signals whose meaning is precisely defined and substantiated, such as:
- **Identity Matched**
- **Profile Reviewed**
- **Tour Guide Licence Verified** — only where applicable to the advertised service and verified against the competent authority
- **Religious Credential Verified** — only after a separate credential schema/source is approved
- **Umrah Service Authorization Verified** — only after LEGAL-GUIDE-002 resolves the applicable authority model

## 10.3 Required verification metadata
Every trust signal must be able to answer internally:
- verified what,
- source/authority,
- evidence type,
- verification method,
- verified at,
- expiry/re-check due,
- current state,
- verifier/service actor,
- revocation/suspension signal if applicable.

## 10.4 Public badge copy
Public badge copy must describe the exact verified fact.

Forbidden by default:
- `PILGRIMS Certified Scholar`
- `Official Ministry Guide`
- `Guaranteed Mutawef`
- `100% trustworthy`
- `Verified Mutawef` while LEGAL-GUIDE-002 is unresolved

## 10.5 Paid influence
Payment to PILGRIMS must never strengthen a trust badge, credential status, verification state, or search trust ranking.

---

# 11. Religious-trust boundary

## 11.1 Governed app truth remains separate
PILGRIMS Ritual/RIC/remedy content remains governed by files `18` and `26`.

Advice from a guide must not become:
- canonical RIC output,
- governed remedy truth,
- canonical ritual state,
- product-generated religious ruling,
- scholar-board-approved content,
- training/evidence used to silently rewrite governed ritual logic.

## 11.2 Tourism credential is not fiqh authority
A tourism licence must not be represented as scholarly or fiqh authority.

## 11.3 Religious credential is independent
If PILGRIMS later verifies a religious qualification, it must have:
- an explicit credential type,
- an accountable authority/source,
- a verification method,
- freshness/expiry semantics where applicable,
- public copy that does not overclaim.

---

# 12. Listing model

V1 listings are narrowly limited to the approved service type for this feature.

## 12.1 Intended initial service type
`UMRAH_RITUAL_ACCOMPANIMENT`

This service type is **not releasable** until LEGAL-GUIDE-002 resolves its applicable legal/authorization model.

## 12.2 Minimum listing fields
Conceptual listing fields:
- `listing_id`
- `provider_id`
- `service_type`
- localized title
- localized service description
- service area
- languages
- group-size capability
- price amount
- currency
- pricing unit
- applicable fees
- inclusions
- exclusions
- availability summary
- trust/eligibility requirements
- listing status
- created/updated timestamps
- moderation status/revision

## 12.3 Pricing
Where the service is advertised through an electronic platform, pricing presentation must meet applicable legal requirements and must not be misleading.

PILGRIMS should prefer structured price disclosure over vague "contact for price" behavior where a public price is legally required.

V1 does not collect payment.

## 12.4 Prohibited listing scope
A listing may not silently include or offer:
- visa processing,
- accommodation,
- transport arrangement,
- airline/rail/bus ticketing,
- packages,
- unrelated tours,
- restaurant booking,
- other separately regulated travel/tourism services,

unless future approved scope and licensing explicitly allow it.

---

# 13. Public discoverability invariant

A listing is publicly discoverable only when all of the following are true:
- provider state is `VERIFIED`,
- listing is approved/active,
- every mandatory credential/authorization for the service type is current,
- no required credential is expired, revoked, suspended, or unverifiable,
- no provider/listing suspension is active,
- the service type is enabled for the jurisdiction,
- all P0 legal release gates for that service model are resolved,
- freshness policy permits a current public trust claim.

A provider or listing losing eligibility must not remain publicly active due to client cache, delayed UI refresh, or provider self-edit.

---

# 14. Browse, search, filter, and ranking

V1 may support:
- text search over public profile/listing fields,
- language filter,
- service area filter,
- group-size filter,
- structured price range/filter,
- currently eligible credential/trust filters where precise and non-misleading.

Ranking must not:
- imply a stronger legal/religious verification than evidence supports,
- convert payment into trustworthiness,
- use undisclosed sponsorship,
- use sensitive personal data,
- use private report contents as a user-visible score,
- claim service quality that PILGRIMS cannot substantiate.

---

# 15. Guide profile/detail

Guide detail must clearly separate:
1. provider identity/profile,
2. advertised service,
3. current credential/trust evidence,
4. pricing/inclusions/exclusions,
5. service-area/language/group-size information,
6. explicit contact action,
7. report action,
8. PILGRIMS scope disclaimer where needed.

Credential details shown publicly must be the minimum needed for transparency and compliance.

Restricted evidence documents are never public.

---

# 16. Contact handoff

## 16.1 V1 model
**Contact Guide → approved channel choices → explicit user choice → external handoff**

Approved channel types may include:
- WhatsApp,
- phone,
- email,
- other explicitly approved external method.

## 16.2 Privacy requirements
The app must:
- never silently reveal pilgrim phone/email,
- never auto-message,
- never import contacts,
- never create a friend/social graph,
- never retain external conversation bodies,
- share only data the pilgrim knowingly chooses to send,
- avoid exposing raw provider contact details broadly where a server-resolved handoff materially reduces scraping/abuse.

## 16.3 Server-resolved handoff posture
The preferred architecture is a server-trusted contact-intent flow that:
- verifies the listing/provider is currently eligible,
- records minimal anti-abuse/audit metadata,
- returns the currently approved contact channel/target or handoff payload,
- does not create a booking,
- does not create payment state,
- does not imply PILGRIMS is party to the external service contract unless the legal model later changes.

---

# 17. Reports, moderation, and support

A trusted discovery product requires operating capability, not badges alone.

## 17.1 Required capabilities
The specification requires:
- application review,
- credential review,
- listing review,
- provider/listing reports,
- urgent delisting,
- suspension,
- expiry propagation,
- revocation,
- re-verification,
- support escalation,
- abuse/fraud handling,
- auditable moderation events,
- re-review/appeal path where policy allows.

## 17.2 Candidate report categories
Candidate categories include:
- credential concern,
- misleading listing,
- fraud/scam,
- unauthorized service,
- religious misconduct or misrepresentation,
- harassment/inappropriate behavior,
- unsafe behavior,
- service/no-show concern,
- other.

Final taxonomy must be reviewed for legal/support implications before implementation.

## 17.3 Defamation/privacy caution
Reports are restricted trust-and-safety data.
Report bodies must not become public profile content or ordinary analytics.

---

# 18. Ratings and reviews

Ratings/reviews are **deferred in V1**.

They are not required for initial trustworthiness because:
- PILGRIMS does not mediate or prove the service transaction,
- "verified review" provenance would otherwise be ambiguous,
- free-text UGC creates moderation/appeal/platform-policy burden,
- legal credential verification and service-quality opinion must remain distinct.

Any future review system must define:
- provenance,
- moderation,
- report/appeal,
- anti-fraud controls,
- whether the underlying service was actually platform-verifiable,
- Apple/Google UGC obligations,
- separation from credential/legal verification.

---

# 19. Monetization boundary

Initial pilgrim access is free:
- browse: free,
- search/filter: free,
- trust/credential information: free,
- guide profile: free,
- contact guide: free,
- report guide: free.

Guide Marketplace is not gated by Supporter.

Future provider monetization is separate from pilgrim Supporter and is out of scope for this pass.

No paid placement may appear as stronger verification.

---

# 20. Account and authorization boundary

## 20.1 Identity
Existing `auth.users` remains the identity source.

No second authentication system is introduced.

## 20.2 Provider state
Provider state is a server-trusted domain object associated with the authenticated user, not a client role toggle.

## 20.3 Pilgrim account posture
Ordinary pilgrims remain able to use local-first core value without account creation.

Authentication is required only when Guide Marketplace needs a protected server-backed action, such as:
- provider application,
- provider profile/listing management,
- report submission where policy requires authenticated abuse controls,
- optional minimal contact intent where abuse/privacy policy requires auth.

Public browse/detail may remain unauthenticated if legal/security review permits it.

---

# 21. Conceptual server-side data model

File `13` owns relational truth. This section defines the feature-domain concepts that file `13` must model before implementation.

## 21.1 `guide_provider_profiles`
Purpose:
- provider application identity link,
- approved public profile fields,
- provider lifecycle state,
- moderation/public eligibility references.

Ownership:
- linked 1:1 to existing authenticated identity for provider self-service fields,
- verification/moderation fields service-managed.

## 21.2 `guide_credentials`
Purpose:
- record credential type/source,
- masked/public metadata,
- verification state,
- issue/expiry/re-check dates where applicable,
- authority/source,
- evidence disposition.

Raw evidence should not be retained by default after verification when unnecessary.

## 21.3 `guide_listings`
Purpose:
- narrowly defined service listing,
- pricing/language/area/group-size/inclusion/exclusion data,
- listing lifecycle/moderation state.

## 21.4 `guide_contact_channels`
Purpose:
- approved provider contact targets,
- visibility/control metadata,
- server-resolved handoff support.

Raw contact values must not be exposed in general browse/search payloads by default.

## 21.5 `guide_verification_events`
Purpose:
- append-oriented audit record for verification/moderation state changes.

Providers cannot mutate this history.

## 21.6 `guide_reports`
Purpose:
- restricted user/provider safety and trust reports,
- status/triage references,
- minimal reporter metadata needed for abuse controls.

## 21.7 `guide_contact_intents`
Optional minimal audit/abuse object recording an explicit contact request without storing conversation content.

If a contact-intent row provides no meaningful compliance/abuse value after legal review, do not create it merely for analytics.

## 21.8 Explicitly absent in V1
Do not add V1 domain tables for:
- bookings,
- payments,
- transactions,
- escrow,
- disputes,
- chat messages,
- reviews.

---

# 22. RLS and authorization invariants

File `13` remains authoritative.

At minimum:
- a provider may edit only their allowed self-service profile/listing fields;
- a provider cannot self-set verification, credential validity, suspension, revocation, or public eligibility;
- public/pilgrim reads return only publicly eligible profiles/listings and explicitly public trust metadata;
- restricted credential evidence is never public;
- report body/details are restricted to authorized trust-and-safety/support roles and the minimum reporter-facing status needed by policy;
- verification event history is service-managed and immutable to ordinary users/providers;
- suspended, expired, revoked, legally disabled, or otherwise ineligible provider/listing content cannot remain public due to RLS/query mistakes;
- service-role operations remain auditable;
- Flutter visibility is never the security boundary.

---

# 23. Minimal API contract

File `14` owns endpoint truth. The smallest intended surface is:

Public/current reads:
- `GET /v1/guides`
- `GET /v1/guides/{guide_id}`

Authenticated provider/application:
- `POST /v1/guides/applications`
- `GET /v1/guides/me/application`
- `PATCH /v1/guides/me/profile`
- `POST /v1/guides/me/listings`
- `PATCH /v1/guides/me/listings/{listing_id}`

Trust/safety/contact:
- `POST /v1/guides/{guide_id}/contact-intent`
- `POST /v1/guides/{guide_id}/reports`

Privileged verification/moderation endpoints are not ordinary mobile-provider actions and must not permit self-verification.

All writes require explicit auth/authorization rules, rate limits, abuse controls, auditability, and idempotency where retries could duplicate a trusted operation.

---

# 24. Offline and stale behavior

Guide Marketplace does not alter the product's essential offline promise.

## 24.1 Network-trusted
The following are online-required trusted operations:
- provider application submit,
- credential verification refresh,
- listing publish/update when server-trusted,
- report submission,
- contact-intent resolution,
- authoritative provider/application status.

## 24.2 Optional cached browse
Cached guide browse/detail may be offered as a convenience only if:
- clearly marked as cached/stale when freshness is insufficient,
- it does not present an old credential as currently verified,
- contact handoff re-checks current eligibility online before resolving,
- expired/revoked/suspended status cannot be hidden by an indefinite cache.

## 24.3 No hidden write queue
Trusted writes must fail honestly while offline.
Do not queue application, listing publication, report, or contact-intent writes in a way that later surprises the user.

## 24.4 Core app independence
Rituals/RIC, Emergency, Phrasebook, Save My Gate, and other essential local-first value remain usable without Guide Marketplace.

---

# 25. Privacy and data minimization

## 25.1 Verify more, store less
For credential verification:
- prefer authoritative API/source checks over document retention,
- store the resulting verified fact and source metadata rather than a permanent identity-document copy where lawful and sufficient,
- if temporary evidence upload is unavoidable, define encryption, access, retention, deletion, and audit controls before implementation.

## 25.2 Sensitive/restricted verification material
Credential evidence, government identity evidence, report bodies, and internal moderation notes are restricted data and must never be public or ordinary analytics.

## 25.3 Contact privacy
Public browse must not unnecessarily expose raw phone/WhatsApp/email values.

## 25.4 Purpose limitation
Every collected field must map to:
- provider eligibility,
- legal disclosure,
- public listing,
- contact handoff,
- trust/safety moderation,
- audit/compliance,
- or another approved purpose.

Do not collect "maybe useful later" data.

---

# 26. Analytics

Use a privacy-safe `guide_*` namespace.

Candidate events:
- `guide_marketplace_view`
- `guide_search`
- `guide_profile_view`
- `guide_contact_intent`
- `guide_application_start`
- `guide_application_submit`
- `guide_application_result`
- `guide_listing_publish`
- `guide_report_submit`
- `guide_verification_state_change`

Never include in ordinary analytics:
- government ID,
- raw licence/credential number,
- credential document content,
- phone number,
- WhatsApp number,
- email,
- private conversation content,
- report body,
- precise private location,
- religious question/advice content.

Verification-state analytics must use non-sensitive normalized state/type identifiers only.

---

# 27. Copy and trust-language rules

Copy must:
- say exactly what PILGRIMS verified,
- show freshness/expiry where relevant,
- distinguish tourist guide licensing from Mutawef eligibility and religious credentials,
- avoid "official", "guaranteed", "certified scholar", or equivalent overclaiming,
- explain that contact moves outside PILGRIMS,
- avoid implying PILGRIMS has booked, paid for, or guaranteed the service.

Regulatory terms must remain faithful to the authority's terminology even when the product uses "Hire a Guide" for user comprehension.

---

# 28. Localization, RTL, and accessibility

The feature must support the app's required locales and RTL architecture.

At minimum:
- all trust status is understandable without color alone,
- badge/status semantics are announced to screen readers,
- credential names and expiry/freshness are readable at large text,
- filter controls are keyboard/screen-reader accessible where applicable,
- long provider names and Arabic/Indonesian/English service text wrap safely,
- contact/report actions remain obvious at large text,
- Light and Dark appearances have equivalent trust/status clarity,
- no badge relies on decorative glow or icon-only meaning.

---

# 29. Canonical screens

The feature owns five canonical screens:
- `guide_marketplace_root`
- `guide_profile_detail`
- `guide_registration_flow`
- `guide_verification_status`
- `guide_listing_editor`

Search/filter is integrated into `guide_marketplace_root` unless future evidence requires a separate screen.

Reporting and contact selection may use sheet/modal/flow surfaces; they are not separate canonical screens in V1.

File `11` and `CONTRACTS/screen_feature_traceability.yaml` must remain in one-to-one sync.

---

# 30. Required screen states

## 30.1 Marketplace root
Must support:
- loading,
- current content,
- empty/no-result,
- filter state,
- network error,
- cached/stale browse,
- feature legally/operationally unavailable.

## 30.2 Profile detail
Must support:
- current eligible profile,
- stale cached profile,
- provider no longer eligible,
- listing unavailable,
- contact unavailable/offline,
- report entry,
- trust detail explanation.

## 30.3 Registration
Must support:
- auth gate,
- draft,
- validation errors,
- submit,
- network failure,
- legal/credential program unavailable.

## 30.4 Verification status
Must support:
- submitted,
- under review,
- verified,
- rejected,
- suspended,
- expired,
- revoked,
- re-verification required,
- stale/unavailable protected status.

## 30.5 Listing editor
Must support:
- draft,
- validation errors,
- pending review,
- active,
- changes requiring re-review,
- suspended/unavailable,
- trusted-write offline failure.

---

# 31. Security and abuse cases

Design and verification must cover:
- forged credentials,
- expired credentials,
- revoked credentials,
- wrong licensing authority modeled by PILGRIMS,
- PILGRIMS itself operating a licensable activity without authorization,
- misleading trust badges,
- unauthorized travel-service offerings,
- false scholar/religious claims,
- religious misinformation,
- off-platform payment scam,
- harassment/personal safety,
- contact scraping,
- verification-document leakage,
- report abuse/defamation,
- fake-review pressure,
- ranking manipulation,
- stale verification state,
- moderation/support failure,
- suspension/expiry propagation failure,
- provider-account takeover,
- mass scraping/enumeration,
- automated report/contact abuse.

---

# 32. Testing requirements

Before implementation can be released, evidence must cover:
- provider application,
- verification success,
- rejection,
- credential expiry,
- credential revocation,
- suspension,
- public listing hiding after ineligibility,
- provider cannot self-verify,
- public cannot read restricted evidence,
- RLS isolation,
- stale browse/detail behavior,
- no stale "currently verified" claim,
- offline trusted-write failure,
- explicit contact consent,
- contact re-check of current eligibility,
- report rate limits/abuse controls,
- moderator suspension/urgent delisting,
- privacy/logging redaction,
- large text,
- screen reader,
- Arabic RTL,
- Light/Dark,
- real physical devices,
- weak-network behavior,
- fraud/abuse scenarios,
- required regulatory disclosure presence.

---

# 33. Release classification and no-ship conditions

Guide Marketplace trust, credential, moderation, privacy, and public eligibility behavior is **RC3** under the existing release taxonomy.

The feature is **no-ship** while any of the following is unresolved:
- LEGAL-GUIDE-001,
- LEGAL-GUIDE-002,
- legally required disclosure/operator duties not implemented,
- public trust badge has ambiguous authority,
- provider can self-verify,
- restricted credential evidence can leak publicly,
- stale/expired/revoked provider can remain publicly eligible,
- moderation/suspension/delisting operations are not staffed/tested,
- RLS/auth proof is missing,
- contact handoff can occur without explicit user action,
- regulatory or privacy review identifies a known non-compliance condition.

No waiver may override known legal non-compliance, religious correctness, critical privacy, or authorization boundaries.

---

# 34. Operational requirements

Operations must be able to:
- disable marketplace discovery,
- disable a service type,
- delist a provider/listing urgently,
- suspend provider contact handoff,
- revoke a trust signal,
- force re-verification,
- respond to credential-authority outage,
- investigate fraud/abuse reports,
- preserve audit evidence,
- communicate honestly with users,
- re-enable only after current eligibility is re-established.

Optional feature containment must not disable Rituals/RIC, Emergency, Phrasebook, Save My Gate, or baseline Group recovery.

---

# 35. Anti-patterns

Forbidden:
- generic `is_verified` as the only trust model,
- provider self-verification,
- client-only public-eligibility enforcement,
- "Verified Mutawef" before authority model resolution,
- tourism licence represented as scholarly authority,
- raw credential documents exposed to ordinary staff/users/analytics,
- hidden collection of pilgrim contact information,
- automatic WhatsApp/SMS/email,
- in-app chat added "for convenience" without scope change,
- bookings/payments/escrow added implicitly,
- paid trust badges,
- sponsored ranking disguised as trust,
- stale credential displayed as current,
- guide advice written back into governed RIC truth,
- sixth primary navigation tab,
- Simple Mode urgent shortcut by default.

---

# 36. Definition of done

Specification readiness requires:
- this file and change-control decision are accepted,
- product scope exception is explicit,
- terminology is stable,
- data/RLS concepts are defined,
- API surface is defined,
- five canonical screens are traceable,
- analytics/redaction policy is defined,
- trust contract validates,
- test/release/operations requirements are defined,
- unresolved legal blockers are explicit.

Implementation readiness additionally requires LEGAL-GUIDE-001 and LEGAL-GUIDE-002 to be resolved by accountable legal/compliance review and the resulting licensing/disclosure model to be reflected across files `03`, `13`, `14`, `28`, `29`, `30`, this file, and the trust contract before application/backend implementation begins.

---

# 37. Current status

**Specification architecture:** designed.

**Public implementation readiness:** blocked pending LEGAL-GUIDE-001 and LEGAL-GUIDE-002.

**Flutter/backend/database implementation:** intentionally not performed in this change.

---

End of file.
